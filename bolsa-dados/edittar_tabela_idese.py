import pandas as pd

# Leitura do arquivo CSV
df=pd.read_csv(r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\base_idese.csv', sep=',', encoding='latin1')
df=df.drop(columns=['Unnamed: 0'])

df = df[df['TIPO_UNID'] == 'Municípios']

# Mostrar todos os valores que aparecem na coluna "CATEGORIA"
categorias = df['CATEGORIA'].unique()

# Ordenar o DataFrame usando a coluna 'COD'
df = df.sort_values(by='COD')

df = df.drop(columns=['TIPO_UNID', 'NOME'])

# Gerar uma nova coluna para cada 'categoria' com as iniciais das palavras da categoria
for categoria in categorias:
    # iniciais = ''.join([palavra[0] for palavra in categoria.split()])
    df[categoria] = 0.00

# Pivot the DataFrame to have 'COD', 'ANO' as indices and 'CATEGORIA' as columns
df_pivot = df.pivot_table(index=['COD', 'ANO'], columns='CATEGORIA', values='VALOR', fill_value=0)

# Reset the index to turn 'COD' and 'ANO' back into columns
df_pivot = df_pivot.reset_index()

# Merge the pivoted DataFrame back with the original DataFrame to include all columns
df_final = pd.merge(df[['COD', 'ANO']].drop_duplicates(), df_pivot, on=['COD', 'ANO'], how='left')

# Ordenar 'df_final' por 'COD' e 'ANO'
df_final = df_final.sort_values(by=['COD', 'ANO'])
# Remover as colunas 'VALOR' e 'CATEGORIA' do DataFrame final
df_final = df_final.drop(columns=['VALOR', 'CATEGORIA'], errors='ignore')
print(df_final.head())


# Salvar 'df_final' em um arquivo CSV
# df_final.to_csv(r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\idese_organizado.csv', index=False, encoding='latin1')