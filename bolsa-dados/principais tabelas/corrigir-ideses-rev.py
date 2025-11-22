import pandas as pd

# Caminho do arquivo original
input_file = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\idese-rev-2013.csv'
output_file = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\idese_reformatado.csv'

# Carregar o arquivo CSV com encoding 'latin-1'
df = pd.read_csv(input_file, delimiter=';', encoding='latin-1')

# Ajustar os nomes das colunas
# Removendo prefixo 'Idese (Rev.2013)\' e '\Ãndice' se existirem
df.columns = [col.replace('Idese (Rev.2013)\\', '').replace('\\Ãndice', '') for col in df.columns]

# Converter o nome das colunas para utf-8
df.columns = [col.encode('latin-1').decode('utf-8') for col in df.columns]

# Transformar o dataframe de formato largo para formato longo
df_long = df.melt(id_vars=['Municípios', 'Código'], var_name='Índice', value_name='Valor')

# Extrair o ano da coluna 'Índice'
df_long['Ano'] = df_long['Índice'].str.extract(r'(\\(\d{4}))')[1]
df_long['Índice'] = df_long['Índice'].str.replace(r'\\\d{4}', '', regex=True)

# Converter ano para numérico
df_long['Ano'] = pd.to_numeric(df_long['Ano'])

# Converter valores para numérico, tratando possíveis vírgulas
if df_long['Valor'].dtype == 'object':
    df_long['Valor'] = df_long['Valor'].str.replace('.', '').str.replace(',', '.').astype(float)

# Pivotar os dados para que cada índice vire uma coluna
df_pivot = df_long.pivot_table(index=['Municípios', 'Código', 'Ano'], columns='Índice', values='Valor').reset_index()

# Ajustando nomes de colunas após pivotagem
df_pivot.columns.name = None  # Removendo nome do índice

# Salvar o DataFrame final
df_pivot.to_csv(output_file, index=False, sep=';', encoding='latin-1', decimal=',')

print("Arquivo salvo com sucesso em:", output_file)
