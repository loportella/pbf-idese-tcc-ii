import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.metrics import MeanAbsolutePercentageError

def create_dataset(data, look_back=1):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), 0])
        y.append(data[i + look_back, 0])
    return np.array(X), np.array(y)

def predict_next_quarters(df, periods=2, look_back=1):
    # Normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(df['Valor'].values.reshape(-1, 1))

    # Prepare the data for LSTM
    X, y = create_dataset(dataset, look_back)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(look_back, 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=[MeanAbsolutePercentageError()])

    # Train the model
    history = model.fit(X, y, epochs=100, batch_size=1, verbose=2)

    # Predict the next periods
    predictions = []
    last_data = dataset[-look_back:]
    for _ in range(periods):
        prediction = model.predict(last_data.reshape(1, look_back, 1))
        predictions.append(prediction[0, 0])
        last_data = np.append(last_data[1:], prediction)

    # Inverse transform the predictions
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    # Create a DataFrame for the predictions
    future_dates = pd.date_range(start=df.index[-1], periods=periods + 1, freq='Q')[1:]
    predictions_df = pd.DataFrame({'Data': future_dates, 'Valor': predictions.flatten()})

    return predictions_df, history, model, X, y

df = pd.read_csv(r'/content/sample_data/Taxa de inadimplência por região - MEI - Sul.csv', sep=';', skiprows=1, names=['Data', 'Valor'])
df['Valor'] = df['Valor'].str.replace(',', '.').astype(float)

# Definir a coluna 'Data' como índice do DataFrame
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
df.set_index('Data', inplace=True)

# Example usage
predictions_df, history, model, X, y = predict_next_quarters(df)
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

# Plotar o gráfico de perda do treinamento
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'])
plt.title('Perda do Treinamento')
plt.xlabel('Época')
plt.ylabel('Perda')
plt.grid(True)
plt.show()

# Calcular e mostrar a taxa de acurácia do modelo
mape = model.evaluate(X, y, verbose=0)[1]
print(f'Taxa de Acurácia (MAPE): {100 - mape:.2f}%')