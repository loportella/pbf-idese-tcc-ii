# Bibliotecas
import pandas as pd # Data Manipulation library
import numpy as np # Fast Numeric Computing library
import matplotlib.pyplot as plt # Plot library
import statsmodels.api as sm
from google.colab import drive
drive.mount('/content/drive')

# Abrir a tabela .csv
df = pd.read_csv(r'/content/drive/My Drive/TCC/dados/idese-bf_2013-2020.csv', sep=';', encoding='latin1')

df.columns =  ['id','ano','total_pago','media_paga', 'total_beneficiarios', 'media_beneficiarios', 'BE', 'BE/en-fund', 'BE/en.fund-Ano.Fi', 'BE/en.fund-An.INI',
                 'BE/en.med', 'BE/esc.adult.','BE/pre-escola','BR','BR-apropri.renda','BR-ger.renda','BS','BS-cond.ger.sau.','BS-cond.ger.sau.OB.p/caus.evit.'
                 ,'BS-cond.ger.sau.OB.p/caus.m.def.','BS-long.','BS-Sau.mat-inf.','BS-Sau.mat-inf.con.p.nat','BS-mat.inf.mort-5a','idese','populacao' ]

# Blocos de analise
b_renda = ['BR','BR-apropri.renda','BR-ger.renda']
b_educacao = ['BE', 'BE/en-fund', 'BE/en.fund-Ano.Fi', 'BE/en.fund-An.INI',
                 'BE/en.med', 'BE/esc.adult.','BE/pre-escola']
b_saude = ['BS','BS-cond.ger.sau.','BS-cond.ger.sau.OB.p/caus.evit.' ,'BS-cond.ger.sau.OB.p/caus.m.def.','BS-long.','BS-Sau.mat-inf.','BS-Sau.mat-inf.con.p.nat','BS-mat.inf.mort-5a']
idese = ['idese']
populacao = 'populacao'

# ESCOLHENDO A CIDADE ANALISADA PELO CÓDIGO IBGE
bage = df[df['id'] == 4301602]
uruguaiana = df[df['id'] == 4322400]
portoalegre = df[df['id'] == 4314902]
santamaria = df[df['id'] == 4316907]
hulhanegra = df[df['id'] == 4309654]
alpestre = df[df['id'] == 4300505]

# pasta_arquivos = '/content/drive/My Drive/TCC/dados/'
pasta_arquivos = '/content/sample_data/'

# Nomes dos arquivos
arquivotxt = 'rl_sumarios_beneficiarios_idese_bage.txt'
imagem = 'rl_beneficiarios_x_idese_bage.png'

# Variáveis
dependent_vars = idese
independent = ['total_beneficiarios']
# independent = ['total_pago']
data = bage[ independent + dependent_vars]

# Preparar os dados
X = sm.add_constant(data[independent])  # Adiciona um termo constante ao preditor

# Ajustar o modelo de regressão linear para cada variável dependente

with open(pasta_arquivos + arquivotxt, 'w') as f:
    y = data[dependent_vars]
    model = sm.OLS(y, X).fit()
    prediction = model.predict(X)
    f.write(f"Sumário de: {dependent_vars} X {independent}:\n")
    f.write(model.summary().as_text())
    f.write("\n\n")
print(f"Sumário de: {dependent_vars} X {independent}:\n")
print(model.summary())

# Plotar os resultados
plt.style.use('dark_background')
plt.figure(figsize=(10, 6))
plt.scatter(data[independent], data[dependent_vars], color='red', label='Dados Reais')
plt.plot(data[independent], prediction, color='blue', label='Linha de Regressão')
plt.xlabel(f'{independent[0]}')
plt.ylabel('IDese')
plt.title(f'Regressão Linear - IDese X {independent[0]} (Bagé)')
plt.legend()
plt.savefig(pasta_arquivos + imagem)
plt.show()
