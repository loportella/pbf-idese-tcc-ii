import pandas as pd

# Caminho do arquivo CSV
caminho_arquivo = r'C:/Users/loren/OneDrive/Área de Trabalho/bolsa-dados/_idese-bf-13a20.csv' 
# Carregar a tabela CSV em um DataFrame
df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')

# Filtrar os dados para os anos de 2013 a 2020
df_filtrado = df[df['ano'].between(2013, 2020)]

# Obter a lista única de valores da coluna 'id'
ids_unicos = df_filtrado['id'].unique()

# Verificar quantos valores da lista única da coluna 'id' contêm os valores completos de 2013 a 2020
ids_completos = [id_ for id_ in ids_unicos if set(range(2013, 2021)).issubset(df_filtrado[df_filtrado['id'] == id_]['ano'].unique())]

print(f"Quantidade de valores da lista única da coluna 'id' que contêm os valores completos de 2013 a 2020: {len(ids_completos)}")
# Obter os ids que não estão na lista de 'ids_completos'
ids_incompletos = [id_ for id_ in ids_unicos if id_ not in ids_completos]

# Eliminar todas as linhas que não possuem registros de 2013 a 2020
df_final = df_filtrado[df_filtrado['id'].isin(ids_completos)]

print(len(df_final))

# Salvar o DataFrame resultante em um novo arquivo CSV
caminho_arquivo_saida = r'C:/Users/loren/OneDrive/Área de Trabalho/bolsa-dados/idese_total_2013-2020.csv'
df_final.to_csv(caminho_arquivo_saida, sep=';', encoding='latin1', index=False)