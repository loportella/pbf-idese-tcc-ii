import pandas as pd
import requests

def tabela_pbf():
    input1 = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\pbf-2007-2021.csv'

    df = pd.read_csv(input1, delimiter=',', encoding='latin1')
    columns_to_remove = ['Unidade Territorial', 'UF', 'Famílias PBF (a partir de Mar/2023)', 'Valor repassado às famílias PBF (a partir de Mar/2023)', 'Valor do Benefício médio (a partir de Mar/2023)']
    df = df.drop(columns=columns_to_remove)
    df = df.rename(columns={
        'Código': 'id',
        'Referência': 'Ano',
        'Famílias PBF (até Out/2021)': 'totalBeneficiarios',
        'Valor repassado às famílias PBF (até Out/2021)': 'valorTotalRepassado',
        'Valor do Benefício médio (até Out/2021)': 'valorMedioRepassado'
    })

    df = df.sort_values(by=['id', 'Ano'])
    output = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\out_pbf-2007-2021.csv'
    df.to_csv(output, index=False, encoding='latin1', sep=';')

def tabela_idese_pbf():
    input1 = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\out_pbf-2007-2021.csv'
    input2 = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\_IDESE_COMPLETO-2007-2021.csv'

    df1 = pd.read_csv(input1, delimiter=';', encoding='latin1')
    df2 = pd.read_csv(input2, delimiter=';', encoding='latin1')
    df1 = df1.drop(columns=['id', 'Ano'])
    df2.columns = df2.columns.str.replace(r'\\Índice', '', regex=True)

    merged_df = pd.concat([df1, df2], axis=1)
    merged_df = merged_df.sort_values(by=['id', 'Ano'])
    first_column = merged_df.pop('Municípios')
    merged_df.insert(0, 'Municípios', first_column)
    id_column = merged_df.pop('id')
    merged_df.insert(1, 'id', id_column)
    ano_column = merged_df.pop('Ano')
    merged_df.insert(2, 'Ano', ano_column)
    merged_df['id'] = merged_df['id'].astype(str).str[:-1].astype(int)

    output = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\_out_idese_pbf.csv'
    merged_df.to_csv(output, index=False, encoding='latin1', sep=';')

def tabela_populacao():
    input1 = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\populacao-popvis.csv'
    input2 = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\_out_idese_pbf.csv'

    df = pd.read_csv(input1, delimiter=',', encoding='latin1', usecols=['CodIBGE','Ano','Total','Classe'])
    df2= pd.read_csv(input2, delimiter=';', encoding='latin1')
    df = df[df['Classe'] == 'Total']
    df = df[(df['Ano'] >= 2007) & (df['Ano'] <= 2021)]
    df = df.drop(columns=['Classe'])
    df.columns = ['id_', 'Ano_', 'Populacao']
    
    merged_df = pd.merge(df2, df, left_on=['id', 'Ano'], right_on=['id_', 'Ano_'], how='left')
    merged_df = merged_df.drop(columns=['id_', 'Ano_'])
    merged_df['totalBeneficiarios'] = merged_df['totalBeneficiarios'].fillna(0).astype(int)
    
    print("Tabela final construída com sucesso!")
    columns_to_convert = merged_df.columns
    for column in merged_df.columns:
        if merged_df.columns.get_loc(column) >= merged_df.columns.get_loc('Ano'):
            if merged_df[column].dtype == 'object':
                merged_df[column] = merged_df[column].str.replace(',', '.').astype(float, errors='ignore')
    output = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\_TABELA_FINAL.csv'
    merged_df.to_csv(output, index=False, encoding='latin1', sep=';')

def adicionar_micro_meso():
    input = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\_TABELA_FINAL.csv'
    df= pd.read_csv(input, delimiter=';', encoding='latin1')
    municipios = obter_municipios()
    municipios_df = pd.DataFrame(municipios)
    
    
    merged_df = pd.merge(df, municipios_df, left_on='id', right_on='id_municipio', how='left')
    # merged_df = merged_df.drop(columns=['id_municipio'])
    
    a = merged_df.pop('id_microrregiao') if 'id_microrregiao' in merged_df.columns else None
    b = merged_df.pop('nome_microrregiao') if 'nome_microrregiao' in merged_df.columns else None
    c = merged_df.pop('id_mesorregiao') if 'id_mesorregiao' in merged_df.columns else None
    d = merged_df.pop('nome_mesorregiao') if 'nome_mesorregiao' in merged_df.columns else None
    merged_df.insert(2, 'id_microrregiao', a)
    merged_df.insert(3, 'nome_microrregiao', b)
    merged_df.insert(4, 'id_mesorregiao', c)
    merged_df.insert(5, 'nome_mesorregiao', d)
    merged_df.pop('valorMedioRepassado') if 'valorMedioRepassado' in merged_df.columns else None
    merged_df = merged_df.drop(columns=['id_municipio'])

    print(merged_df["totalBeneficiarios"].dtype)
    output = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\_TABELA_FINAL.csv'
    merged_df.to_csv(output, index=False, encoding='latin1', sep=';')

def obter_municipios():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/43/municipios"
    response = requests.get(url)

    if response.status_code == 200:
        municipios = response.json()
        return [
            {
                "id_municipio": municipio['id'],
                "id_microrregiao": municipio['microrregiao']['id'],
                "nome_microrregiao": municipio['microrregiao']['nome'],
                "id_mesorregiao": municipio['microrregiao']['mesorregiao']['id'],
                "nome_mesorregiao": municipio['microrregiao']['mesorregiao']['nome']
                
            }
            for municipio in municipios
        ]
        
    else:
        print(f"Erro ao acessar a API do IBGE: {response.status_code}")
        return []

if __name__ == '__main__':
    # tabela_pbf()
    # tabela_idese_pbf()
    tabela_populacao()
    adicionar_micro_meso()
