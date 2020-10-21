# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 17:08:39 2020

@author: alexo
"""

# Programe qui load les data et qui lance l'apprentissage 
# une fois l'apprentissage terminé il est sauvegardé et peut etre utilisé 

import pickle
import tkinter 
import tensorflow as tf 
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

tf.executing_eagerly()

nb_sequences = 1000 #il faut savoir combien on a mis de séquences dans la liste pour que la fonction marche 
"""Lecture et creation de la liste data"""

def lecture(depickled,nb_sequences):
    data = list()
    for  i in range(nb_sequences):
        data_load = depickled.load()
        data.append(data_load)
    return(data)
        
# Chargement
with open("data_test", 'rb') as file:
    depickler = pickle.Unpickler(file)
    data = lecture(depickler,nb_sequences)

depickler = None    

file.close()

nb_tours = len(data[0])

input_train= list()
output_train=list()
input_val = list()
output_val = list()
input_test= list()
output_test = list()

for i in range(int(nb_sequences*0.6)):
    input_train.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][0])[0:100,0:100]),(100,100,1)))
    output_train.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][1])[0:100,0:100]),(100,100,1)))

for i in range(int(nb_sequences*0.6),int(nb_sequences*0.8)):
    input_val.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][0])[0:100,0:100]),(100,100,1)))
    output_val.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][1])[0:100,0:100]),(100,100,1)))
    
for i in range(int(nb_sequences*0.8),nb_sequences):
    input_test.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][0])[0:100,0:100]),(100,100,1)))
    output_test.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][1])[0:100,0:100]),(100,100,1)))
  
    
input_train = tf.convert_to_tensor(input_train)
output_train = tf.convert_to_tensor(output_train)
input_val = tf.convert_to_tensor(input_val)
output_val = tf.convert_to_tensor(output_val)
input_test = tf.convert_to_tensor(input_test)
output_test = tf.convert_to_tensor(output_test)
########################################################
# TEST

def sigmoid(x):
    return(1/(1+tf.math.exp(-(x-0.5))))



data_test = []
data_test_target = []

for  i in range(400):
    data_test.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][0])[0:100,0:100]),(100,100,1)))
    data_test_target.append(tf.reshape(tf.convert_to_tensor(np.asarray(data[i][1])[1:99,1:99]),(98,98,1)))
data_test = tf.convert_to_tensor(data_test) 
data_test_target = tf.convert_to_tensor(data_test_target) 


model = keras.models.Sequential()
model.add(keras.layers.Conv2D(8,(3,3),activation='relu',input_shape=(100,100,1),padding='same'))
model.add(keras.layers.Conv2D(4,(1,1),activation='relu'))
model.add(keras.layers.Conv2D(1,(1,1)))
model.add(keras.layers.Activation(sigmoid))

model.summary()


model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=['accuracy'])

history = model.fit(input_train, output_train, epochs=100,validation_data=(input_val,output_val))


d = tf.reshape(input_test[0],(1,100,100,1))
verif_pred = model.predict(d)
verif_pred = tf.make_tensor_proto(verif_pred)
verif_pred = tf.make_ndarray(verif_pred)
verif_pred = verif_pred.reshape(100,100)



verif_target = output_test[0]
verif_target = tf.make_tensor_proto(verif_target)
verif_target = tf.make_ndarray(verif_target)
verif_target = verif_target.reshape(100,100)


model.save('model_jeu_vie')


loss,acc = model.evaluate(input_test,  output_test, verbose=2)
print("Restored model, accuracy: {:5.2f}%".format(100*acc))








