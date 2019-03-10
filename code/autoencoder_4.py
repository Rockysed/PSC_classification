# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 15:25:46 2018

loss = 0.3586

@author: 754672
"""

from keras.layers import Input, Dense, Dropout
from keras.models import Model
from sklearn.preprocessing import MinMaxScaler
from keras.models import model_from_json
from sklearn.model_selection import train_test_split
import pickle
import h5py

#load data

new_file = h5py.File("../data/mipas_blabeled_reinhold_features/rf_mipas_complete", "r")

#load features

btd_complete = new_file["btd_complete"][:]

#close file

new_file.close()

#load scaler 
filename = "new_min_max_scaler.pckl"
scaler = pickle.load(open(filename, 'rb'))

#data

f_train, f_test = train_test_split(btd_complete, test_size=0.33, random_state=42)
f_train = scaler.transform(f_train)
f_test = scaler.transform(f_test)

#layers

input_rf = Input(shape=(10011,))

encoded = Dropout(0.1)(input_rf)

encoded = Dense(500, activation='relu')(encoded)

encoded = Dropout(0.1)(encoded)

encoded = Dense(200, activation='relu')(encoded)

encoded = Dense(100, activation='relu')(encoded)

encoded = Dense(50, activation='relu')(encoded)

encoded = Dropout(0.1)(encoded)

encoded = Dense(20, activation='relu')(encoded)

decoded = Dense(20, activation='relu')(encoded)

decoded = Dense(50, activation='relu')(decoded)

decoded = Dense(100, activation='relu')(decoded)

decoded = Dense(200, activation='relu')(decoded)

decoded = Dropout(0.1)(decoded)

decoded = Dense(500, activation='relu')(encoded)

decoded = Dense(10011, activation='sigmoid')(decoded)

autoencoder = Model(input_rf, decoded)

#compile model

#autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

autoencoder.compile(optimizer='adadelta', loss='mean_squared_error')

#run

autoencoder.fit(f_train, f_train,
                epochs=500,
                batch_size=256,
                shuffle=True,
                validation_data=(f_test, f_test))

#define encoder model

encoder = Model(input_rf, encoded)

#predict encoded features

encoded_rf = encoder.predict(f_test)

#save model 
# serialize model to JSON
encoder_json = encoder.to_json()

with open("Neural_net_weights/new/new_encoder_2.json", "w") as json_file:
    json_file.write(encoder_json)

# serialize weights to HDF5

encoder.save_weights("Neural_net_weights/new/new_model_encoder_2.h5")

print("Saved model to disk")
"""
#save model 
# serialize model to JSON
autoencoder_2_json = autoencoder.to_json()

with open("autoencoder_2.json", "w") as json_file:
    json_file.write(autoencoder_2_json)

# serialize weights to HDF5

autoencoder.save_weights("model_autoencoder_2.h5")

print("Saved model to disk")

#load model

# load json and create model

json_file = open('autoencoder_2.json', 'r')

loaded_model_json = json_file.read()

json_file.close()

loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights("weights_autoencoder_2.h5")

print("Loaded model from disk")


#plotting results
plt.plot(autoencoder.history.history['loss'])
plt.plot(autoencoder.history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
"""