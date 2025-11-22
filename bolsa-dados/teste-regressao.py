import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Gerar dados sintéticos com relação positiva
np.random.seed(42)  # Para reprodutibilidade
x = np.linspace(0, 10, 50)  # Variável independente
y = 2 * x + 1 + np.random.normal(scale=2, size=50)  # Variável dependente com ruído

# Ajustar o modelo de regressão linear
modelo = LinearRegression()
modelo.fit(x.reshape(-1, 1), y)  # Reformatar x para 2D

# Coeficientes da reta
coef_angular = modelo.coef_[0]
coef_linear = modelo.intercept_

# Previsões para traçar a linha de regressão
x_vals = np.array([min(x), max(x)])
y_vals = coef_angular * x_vals + coef_linear

# Configurar o gráfico
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Dados observados')
plt.plot(x_vals, y_vals, color='red', linewidth=2, label='Linha de regressão')

# Adicionar elementos ao gráfico
plt.title('Relação Positiva entre X e Y', fontsize=14)
plt.xlabel('Variável X', fontsize=12)
plt.ylabel('Variável Y', fontsize=12)
plt.grid(alpha=0.3)
plt.legend()

# Mostrar equação no gráfico
eq_text = f'y = {coef_angular:.2f}x + {coef_linear:.2f}'
plt.text(0.5, 25, eq_text, fontsize=12, color='red')

plt.show()