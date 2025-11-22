import pandas as pd
import matplotlib.pyplot as plt
from google.colab import drive
drive.mount('/content/drive')

if __name__ == "__main__":
    # Abrir a tabela .csv
    df = pd.read_csv(
        r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\testes/Falsificacao.csv',
        sep=';',names=['ano', 'estado', 'tipo', 'valor', 'quantidade']
    )
    
    # Filtrar os dados para Minas Gerais, valor 50,00 e ano até 2022
    # df_ = df[(df['estado'] == 'MINAS GERAIS') & (df['valor'] == '100,00') & (df['ano'] <= 2022)]
    df = df[ (df['valor'] == '10,00') & (df['ano'] <= 2022)]
    
    # Limpar e converter a coluna 'quantidade'
    df['quantidade'] = (
        df['quantidade']
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
        .astype(int)
    )
    
    # Criar o gráfico para cada classe da coluna "valor"
    for valor in df['valor'].unique():
        df_grouped = df.groupby('ano')['quantidade'].sum().reset_index()
        plt.plot(df_grouped['ano'], df_grouped['quantidade'], label=f"R${valor}")

    # Adicionar legenda com título
    plt.legend(title='Notas')
    plt.title('Evolução da Quantidade de Notas Falsificadas por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade')
    plt.grid(True)  # Adicionar grid para melhor visualização
    plt.show()