import pandas as pd

# Carregar as tabelas CSV
tabela1 = pd.read_csv(r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\agrupado_bf.csv', sep=',', encoding='latin1')
tabela2 = pd.read_csv(r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\idese_organizado.csv',sep=',',encoding='latin1')

# Remover as linhas com ano=2021
tabela1 = tabela1[tabela1['ano'] != 2021]
tabela2 = tabela2[tabela2['ANO'] != 2021]

# Mesclar as tabelas com base nas colunas 'id' e 'ano'
tabela_unida = pd.merge(tabela1, tabela2, how='left', left_on=['id', 'ano'], right_on=['COD', 'ANO'])

# Preencher valores NaN com zero
tabela_unida[['total_pago', 'media_pago', 'total_beneficiarios', 'media_beneficiarios']] = tabela_unida[['total_pago', 'media_pago', 'total_beneficiarios', 'media_beneficiarios']].fillna(0)

# Selecionar as colunas desejadas
tabela_final = tabela_unida[['id', 'ano', 'total_pago', 'media_pago', 'total_beneficiarios', 'media_beneficiarios'] + list(tabela2.columns)]

# Salvar a nova tabela em um arquivo CSV
tabela_final.to_csv(r'C:\Users\loren\OneDrive\Área de Trabalho\tabela_unida.csv', index=False, sep=',', encoding='latin1')