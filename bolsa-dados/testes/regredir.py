import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt


def predict_next_quarters(df, periods=2):
    # Prepare the data for linear regression
    df['Data'] = np.arange(len(df))
    X = df['Data'].values.reshape(-1, 1)
    y = df['Valor'].values

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict the next periods
    future_quarters = np.arange(len(df), len(df) + periods).reshape(-1, 1)
    predictions = model.predict(future_quarters)

    # Create a DataFrame for the predictions
    future_dates = pd.date_range(start=df.index[-1], periods=periods + 1, freq='Q')[1:]
    predictions_df = pd.DataFrame({'Data': future_dates, 'Valor': predictions})

    return predictions_df

df = pd.read_csv(r'C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados\testes\Taxa de inadimplência por região - MEI - Sul.csv', sep=';', skiprows=1, names=['Data', 'Valor'])
df['Valor'] = df['Valor'].str.replace(',', '.').astype(float)

# Definir a coluna 'Data' como índice do DataFrame
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
df.set_index('Data', inplace=True)

# Example usage
predictions_df = predict_next_quarters(df)
df = pd.concat([df, predictions_df.set_index('Data')])

print("Valores previstos para os próximos trimestres:")
print(predictions_df)

# Plotar o gráfico de taxa porcentagem no tempo
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['Valor'], marker='o', linestyle='-')
plt.title('Taxa Porcentagem no Tempo')
plt.xlabel('Data')
plt.ylabel('Taxa Porcentagem')
plt.xticks(rotation=45)  # Adicionar espaçamento nas legendas do eixo x
plt.grid(True)
plt.show()