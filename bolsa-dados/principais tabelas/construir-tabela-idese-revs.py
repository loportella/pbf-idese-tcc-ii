import pandas as pd

input1 = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\_idese-rev2013.csv'
input2 = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\_idese-rev2020.csv'

df1 = pd.read_csv(input1, delimiter=';', encoding='latin-1')
df2 = pd.read_csv(input2, delimiter=';', encoding='latin-1')
# Garantir que os nomes estejam na codificação correta para mostrar acentuações em português
for df in [df1, df2]:
    df.columns = [col.encode('latin-1').decode('utf-8') for col in df.columns]
    df['Municípios'] = df['Municípios'].str.encode('latin-1').str.decode('utf-8').str.encode('latin-1').str.decode('utf-8')
    

merged_df = pd.concat([df1, df2], ignore_index=True)
merged_df = merged_df.sort_values(by=['Código', 'Ano'])
# Renomear a coluna "Código" para "id"
merged_df = merged_df.rename(columns={"Código": "id"})

# Remover vírgulas e pontos dos valores da coluna "id" e convertê-los para inteiros
merged_df['id'] = merged_df['id'].astype(str).str.replace(',', '').str.replace('.', '').astype('Float64').astype(int)
# Remover linhas duplicadas com o mesmo valor nas colunas "Código" e "Ano"
merged_df = merged_df.drop_duplicates(subset=['id', 'Ano'], keep='first')

output = r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\principais tabelas\merged_idese.csv'
merged_df.to_csv(output, index=False, encoding='latin-1', sep=';')
