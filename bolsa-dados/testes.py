import keras # Neural Network Library
from keras import layers # Layers to a neural network
from keras import optimizers # optimizers
from keras import models # Models
import pandas as pd # Data Manipulation library
import numpy as np # Fast Numeric Computing library
import tensorflow as tf # Optimizers
import matplotlib.pyplot as plt # Plot library
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from google.colab import drive
drive.mount('/content/drive')
# Load your DataFrame here
df = pd.read_csv('/content/drive/My Drive/your_dataset.csv')

# Drop columns 3 and 5
df = df.drop(df.columns[[3, 5]], axis=1)
# Rename the columns of the DataFrame
df.columns = ['col1', 'col2', 'col3', 'col4', 'col5']
# Assuming train_data is a numpy array, you need to define it first
train_data = df.values
train_y = train_data[0, 1]