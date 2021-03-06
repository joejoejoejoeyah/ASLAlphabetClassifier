# -*- coding: utf-8 -*-
"""ASL_sign_classifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zUyZO91ILHvfRlRx1H9UNEY3LC9FjKjR

*Authors*: Jacob Gately, Joe Tudor, Matthew Kolessar Wright

*Last Edited*: Nov-27-20

Project Notebook for CS470 Deep Learning Project. Steps through our deep learning model that takes a dataset of images and learns to classify American Sign Language alphabet characters and a few special symbols. 




**Libraries**
"""

import os
import numpy as np
import cv2
from matplotlib import pyplot as plt
from copy import deepcopy
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from keras.layers import Conv2D, Dense, Dropout, Flatten
import zipfile

"""**Loading ASL Alphabet Data From Kaggle**\
Found here: https://www.kaggle.com/grassknoted/asl-alphabet
"""

!pip install -q kaggle

from google.colab import files
files.upload()

!mkdir ~/.kaggle
!cp kaggle.json ~/.kaggle/

!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d grassknoted/asl-alphabet

"""**Extracting ASL data**"""

with zipfile.ZipFile("../content/asl-alphabet.zip", 'r') as zip_ref:
    zip_ref.extractall("")

"""**Moving Files to Training and Testing Folders**"""

labels = ['A', 'B' , 'C' , 'D' , 'del', 'E' , 'F' , 'G' , 'H', 'I', 'J', 'K', 
          'L' ,'M' , 'N', 'nothing', 'O', 'P' , 'Q' , 'R' , 'S' , 'space' , 
          'T' ,'U' , 'V', 'W', 'X' , 'Y' , 'Z']

fileName = ""
basePath = "asl_alphabet_train/asl_alphabet_train/"
uniquePath = ""
fullName = ""
newPath = ""

os.mkdir("asl_final_train"); 
os.mkdir("asl_final_test");

for label in labels:  #Iterate over every label
  for x in range (3000):  #Iterate over every image 
    fileName = label + str(x+1) + ".jpg";
    uniquePath = '/' + label + '/';
    fullName = os.path.basename(basePath + uniquePath + fileName)
    if x >= 2100:
      newFullPath = os.path.join("asl_final_test", fullName);
    else:
      newFullPath = os.path.join("asl_final_train", fullName);
    os.rename(basePath + uniquePath + fileName, newFullPath)

"""**Creating Labels and Image Data**"""

trainDataDir = "asl_final_train"

testDataDir = "asl_final_test"


train_images = []
train_labels = []
label = ""

for image in os.listdir(trainDataDir):
    array = cv2.imread(os.path.join(trainDataDir,image), cv2.IMREAD_COLOR)
    array = cv2.resize(array, (64, 64))
    train_images.append(array)  #Add image to training data
    if image[0] == 'd':
      label = "del";
    elif image[0] == 'n':
      label = "nothing";
    elif image[0] == 's':
      label = "space";
    else:
      label = image[0];
    label = labels.index(label);  
    train_labels.append(label) #Add label to training labels



test_images = []
test_labels = []
label = ""

for image in os.listdir(testDataDir):
    array = cv2.imread(os.path.join(testDataDir,image), cv2.IMREAD_COLOR)
    array = cv2.resize(array, (64, 64))
    test_images.append(array)  #Add image to testing data
    if image[0] == 'd':
      label = "del";
    elif image[0] == 'n':
      label = "nothing";
    elif image[0] == 's':
      label = "space";
    else:
      label = image[0]; 
    label = labels.index(label);   
    test_labels.append(label) #Add label to training labels

#Convert to valid format
train_images = np.array(train_images);
train_labels = np.array(train_labels);
test_images = np.array(test_images);
test_labels = np.array(test_labels);

"""**Displaying Shape of datasets and size**\
*Distinct labels coorespond to indext of character labels array.*
"""

print("Shape of the training dataset, number or images and resolution:", train_images.shape)
print("Shape of the testing dataset, number or images and resolution:", test_images.shape)
print("All distinct training labels:", np.unique(train_labels))

"""**We plot some of the testing images and their labels to visualize the data**"""

class_names = ['A', 'B' , 'C' , 'D' , 'del', 'E' , 'F' , 'G' , 'H', 'I', 'J', 'K', 
          'L' ,'M' , 'N', 'nothing', 'O', 'P' , 'Q' , 'R' , 'S' , 'space' , 
          'T' ,'U' , 'V', 'W', 'X' , 'Y' , 'Z']

#plotting stuff
plt.figure(figsize = (10,10))
for i in range(25):
  plt.subplot(5,5,i+1)
  plt.xticks([])
  plt.yticks([])
  plt.grid(False)
  plt.imshow(test_images[i], cmap=plt.cm.binary)
  plt.xlabel(class_names[test_labels[i]])
plt.show()

"""**CNN Architecture**\
*As you can see input shape is resized to (64,64) which was needed in order to reduce the time for training and expense on the machine*
"""

model = models.Sequential()
model.add(layers.Conv2D(64, (3,3), activation='relu', input_shape=(64,64,3)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(29))

model.summary()

class_names = ['A', 'B' , 'C' , 'D' , 'del', 'E' , 'F' , 'G' , 'H', 'I', 'J', 'K', 
          'L' ,'M' , 'N', 'nothing', 'O', 'P' , 'Q' , 'R' , 'S' , 'space' , 
          'T' ,'U' , 'V', 'W', 'X' , 'Y' , 'Z']

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
CNN_trained = model.fit(train_images, train_labels, epochs=10,
                        validation_data=(test_images, test_labels))

plt.imshow(test_images[0], cmap=plt.cm.binary)
plt.xlabel(class_names[test_labels[0]])
plt.show()

"""Our Validation accuracy is very low here which means the model is overfitting to the training set.

**Model with dropout Regularization**\
*The same parameters we kept as the above model but with added dropout regularization to attempt to deal with overfitting to the training set*

"""

model2 = models.Sequential()
model2.add(layers.Conv2D(64, (3,3), activation='relu', input_shape=(64,64,3)))
model2.add(Dropout(0.5))
model2.add(layers.MaxPooling2D((2,2)))
model2.add(layers.Conv2D(64, (3,3), activation='relu'))
model2.add(Dropout(0.5))
model2.add(layers.MaxPooling2D((2,2)))
model2.add(layers.Conv2D(128, (3,3), activation='relu'))
model2.add(Dropout(0.5))
model2.add(layers.Flatten())
model2.add(layers.Dense(128, activation='relu'))
model2.add(layers.Dense(29))

model2.summary()

class_names = ['A', 'B' , 'C' , 'D' , 'del', 'E' , 'F' , 'G' , 'H', 'I', 'J', 'K', 
          'L' ,'M' , 'N', 'nothing', 'O', 'P' , 'Q' , 'R' , 'S' , 'space' , 
          'T' ,'U' , 'V', 'W', 'X' , 'Y' , 'Z']

model2.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
CNN_trained = model2.fit(train_images, train_labels, epochs=10,
                        validation_data=(test_images, test_labels))

plt.imshow(test_images[0], cmap=plt.cm.binary)
plt.xlabel(class_names[test_labels[0]])
plt.show()

"""**Conclusion**\
Our first CNN model was able to achieve a high level of accuracy on the training data but had a very poor validation accuracy. We constructed a new model with dropout regularization to attempt to deal with overfitting to the training data but unfortunately it only raised the validation accuracy a miniscule amount and drastically lowered our training accuracy.

*Why the low accuracy?*\
We believe that our model has achieved these results because of the dataset we have used. The kaggle dataset is very large but the images to do not have much variation. There is similar lighting in each photo and the same hand is used every time.

*How could we improve?*\
To achieve a higher validation accuracy we would need to use a dataset that has much higher variation. Unfortunately it is very difficult to find an effective way to augment the dataset because some signs with mean different things when they are rotated or skewed. 
"""
