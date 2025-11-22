import pandas as pd

# Caminho do arquivo CSV
# caminho_arquivo = 'C:/Users/loren/OneDrive/Área de Trabalho/bolsa-dados/completo_bf.csv'
caminho_arquivo = 'C:/Users/loren/OneDrive/Área de Trabalho/bolsa-dados/completo_nbf.csv'

# Leitura do arquivo CSV
df = pd.read_csv(caminho_arquivo, sep=',', encoding='latin1')

# Exibir as primeiras linhas do DataFrame
print(df.head())
# Converter a coluna 'ano_mes_referencia' para datetime
df['ano_mes_referencia'] = pd.to_datetime(df['ano_mes_referencia'])

# Extrair o ano da coluna 'ano_mes_referencia'
df['ano'] = df['ano_mes_referencia'].dt.year
# Agrupar por 'id_municipio' e 'ano' e calcular a soma das colunas 'valor_pago' e 'total_beneficiarios' e a média de 'valor_pago' e 'total_beneficiarios'
df_agrupado = df.groupby(['id_municipio', 'ano']).agg({
    'valor_pago': ['sum', 'mean'],
    'total_beneficiarios': ['sum', 'mean']
}).reset_index()

# Flatten the MultiIndex columns
df_agrupado.columns = ['_'.join(col).strip() if type(col) is tuple else col for col in df_agrupado.columns]
df_agrupado.rename(columns={
    'id_municipio_': 'id_municipio',
    'ano_': 'ano',
    'valor_pago_sum': 'total_pago',
    'valor_pago_mean': 'media_pago',
    'total_beneficiarios_sum': 'total_beneficiarios',
    'total_beneficiarios_mean': 'media_beneficiarios'
}, inplace=True)

# Renomear as colunas
df_agrupado.rename(columns={
    'id_municipio': 'id',
    'valor_pago': 'total_pago',
    'total_beneficiarios': 'total_beneficiarios'
}, inplace=True)

# Exibir o DataFrame resultante
print(df_agrupado.columns)
print(df_agrupado.head())

# Caminho para salvar o arquivo CSV
caminho_saida = 'C:/Users/loren/OneDrive/Área de Trabalho/bolsa-dados/agrupado_nbf.csv'
# Salvar o DataFrame resultante em um arquivo CSV
df_agrupado.to_csv(caminho_saida, index=False, sep=',', encoding='latin1')