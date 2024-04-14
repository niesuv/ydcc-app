from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

df = pd.read_csv("data.csv")
train, test=train_test_split(df,test_size=0.3, random_state=29)


feature_train_df = train.select_dtypes(include=['float64', 'int64'])
feature_test_df = test.select_dtypes(include=['float64', 'int64'])

#Scalling numerical attributes
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

# extract numerical attributes and scale it to have zero mean and unit variance
cols = feature_train_df.columns
sc_feature_train = scaler.fit_transform(feature_train_df)
sc_feature_test = scaler.fit_transform(feature_test_df)
# sc_test = scaler.fit_transform(test.select_dtypes(include=['float64']))

# turn the result back to a dataframe
sc_feature_train_df = pd.DataFrame(sc_feature_train, columns = cols)
sc_feature_test_df = pd.DataFrame(sc_feature_test, columns = cols)

# importing one hot encoder from sklearn
from sklearn.preprocessing import OneHotEncoder

# creating one hot encoder object
onehotencoder = OneHotEncoder()

trainDep = train['Label'].values.reshape(-1,1)
trainDep = onehotencoder.fit_transform(trainDep).toarray()
testDep = test['Label'].values.reshape(-1,1)
testDep = onehotencoder.fit_transform(testDep).toarray()

train_X=sc_feature_train_df
train_y=trainDep[:,0]

test_X=sc_feature_test_df
test_y=testDep[:,0]

from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler
import pickle as pk
# Assuming train_X and test_X are your feature matrices, and train_y and test_y are your target vectors

# Standardize the data (important before applying PCA)
scaler = StandardScaler()
train_X_scaled = scaler.fit_transform(train_X)
test_X_scaled = scaler.transform(test_X)

# Apply PCA
num_components = 12  # Adjust the number of components according to your needs
pca = PCA(n_components=num_components)

# Fit and transform the training data
train_X_pca = pca.fit_transform(train_X_scaled)

# Transform the testing data (using the same PCA transformation)
test_X_pca = pca.transform(test_X_scaled)

# Select all features using SelectKBest with the f_classif scoring function
feature_selector = SelectKBest(score_func=f_classif, k='all')

# Fit and transform the training data
train_X_selected = feature_selector.fit_transform(train_X_pca, train_y)

# Transform the testing data (using the same feature selection)
test_X_selected = feature_selector.transform(test_X_pca)
pk.dump(pca, open("pca.pkl","wb"))
import tensorflow as tf
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv1D, MaxPooling1D
from tensorflow.keras.optimizers import AdamW
# Assuming train_X_selected and test_X_selected are your selected features after PCA and feature selection

# Specify the number of selected features
num_selected_features = train_X_selected.shape[1]

# Reshape the data for 1D CNN (assuming you have time series-like data)
train_X_selected = train_X_selected.reshape(train_X_selected.shape[0], num_selected_features, 1)
test_X_selected = test_X_selected.reshape(test_X_selected.shape[0], num_selected_features, 1)

# Create a simple CNN model
model = Sequential()

# Convolutional layers
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(num_selected_features, 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))

# Flatten layer to connect convolutional layers to dense layers
model.add(Flatten())

# Dense layers
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))

# Additional hidden layers
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(4, activation='relu'))

model.add(Dense(1, activation='sigmoid'))  # Assuming binary classification, adjust for your task

# Compile the model
model.compile(optimizer=AdamW(), loss='binary_crossentropy', metrics=['accuracy'])
model.summary()
# # Train the model
history = model.fit(train_X_selected, train_y, epochs=5, batch_size=128, validation_split=0.2)

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(test_X_selected, test_y)
print(f'Test Accuracy: {test_accuracy}')

model.save("cnn.h5")