'''
This script includes several functions that should be enough for:
1. Taking pickle files as input
2. Generates /

Run in Python3, Keras 2.08

Author: Chester Wang - 450647297
'''


from PIL import Image
import os
import scipy.misc
import numpy as np
import random
import pickle
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.utils import np_utils
from keras.models import Sequential, Model
from keras.layers import Input, Flatten, Dense, Dropout, Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint
from keras.models import load_model



##################
#                #
#   Deprecated   #
#                #
##################

# TODO: Deprecated
# Returns a numpy array in shape (x,y,4)
# Two images (PIL.Image objects) have to in same resolution!
# It'd be better in square shape
def merge_image(original_image_path, depth_image_path, width, height):

    d_img = load_img(depth_image_path, grayscale=True)
    d_array = img_to_array(d_img).reshape(height, width)
    print(d_array.shape)

    o_img = load_img(original_image_path, grayscale=False)
    o_array = img_to_array(o_img)
    print(o_array.shape)


    combined_array = np.zeros((height, width, 3), dtype="float32")
    combined_array[:, :, 0:3] = o_array # The first three layers will be the original one
    combined_array[:, :, 3] = d_array

    return combined_array


# image_size has to be a tuple
# Returns data, label
def load_data_from_directory(dir_path, image_size = None, use_throttle = False, use_steering = False):

    if(not use_throttle and not use_steering):
        print("Use either throttle or steering for training!")
        quit(-1)

    if(use_steering and use_throttle):
        print("Cannot use both throttle and steering for training!")
        quit(-1)

    if(image_size == None):
        print("Specify image size first!")
        quit(-1)

    num = 0
    for each in os.listdir(dir_path):
        if(each.endswith(".pickle")):
            num += 1


    data = np.zeros((num, image_size[0], image_size[1], image_size[2]), dtype="float32")
    label = np.zeros((num, 1), dtype="float32")

    index = 0

    for file_name in os.listdir(dir_path):
        if(file_name.endswith(".pickle")):
            file_path = dir_path + file_name
            p = pickle.load(open(file_path, "rb"))
            data[index, :, :, :] = p

            if(use_steering):
                label[index] = float(file_name[:-7].split("_")[3])

            if(use_throttle):
                label[index] = float(file_name[:-7].split("_")[2])

            index += 1


    # Categorize them into 31 classes.
    # Assumed the range of throttle / steering is [0, 1]
    label = np.digitize(label, np.arange(0,1,1/30))
    label = np_utils.to_categorical(label, 31)

    data /= 255

    print("Data shape", data.shape)
    print("Label shape", label.shape)

    return data, label



# input_shape is a tuple, such as (800, 1200) height, width
# VGG
def build_model(input_shape, nb_class):

    img_input = Input(shape=input_shape)

    model = Sequential()

    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)


    x = Flatten(name='flatten')(x)
    x = Dense(4096, activation='relu', name='fc1')(x)
    x = Dense(4096, activation='relu', name='fc2')(x)
    x = Dense(nb_class, activation='softmax', name='predictions')(x)

    model = Model(img_input, x, name='vgg16')

    model.summary()

    return model


# Train the model, notice that this function has to be called before evaluate
def train(data, label, input_shape, nb_class):

    cp = ModelCheckpoint("MIT_Car.hdf5", monitor='val_acc', verbose=1, save_best_only=True,
                         save_weights_only=False, mode='max')
    callbacks_list = [cp]

    model = build_model(input_shape=input_shape, nb_class=nb_class)

    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

    if(data is not None and label is not None):
        model.fit(data, label, batch_size=64, epochs=30, validation_split=0.2, verbose=1, shuffle=True, callbacks=callbacks_list)

    print("\n\nTraining done!")

    return model



# The main method
# Parameters: train_path, test_path. They can be the same, but the result might be misleading.
def run(train_path, test_path, image_size, use_throttle=False, use_steering=False):
    train_data, train_label = load_data_from_directory(image_size=image_size,
                                                       use_throttle=use_throttle, use_steering=use_steering, dir_path=train_path)

    test_data, test_label = load_data_from_directory(image_size=image_size,
                                                       use_throttle=use_throttle, use_steering=use_steering, dir_path=test_path)


    # Currently we are spliting them into 31 classes. See line 104 (or somewhere near) in load_data_from_directory
    model = train(train_data, train_label, image_size, 31)

    # After we evaluate it's performance
    scores = model.evaluate(test_data, test_label, verbose=1)
    print("Overall Accuracy: %.2f%%" % (scores[1] * 100))


# Evaluate one pickle file
def evaluate_one(pickle_file, model_path):
    model = load_model(model_path)
    
    pickle_file = pickle_file.reshape((1, pickle_file.shape[0], pickle_file.shape[1], pickle_file.shape[2]))
    
    return np.argmax(model.predict(pickle_file), axis=1)



# Change parameters here for different purposes
if __name__ == "__main__":
    import sys
    folder="full_datasets/{}/".format(sys.argv[1])

    im_size = int(sys.argv[2])
    num_pixel = int(sys.argv[3])
    run(folder,folder, use_throttle=False, use_steering=True, image_size=(im_size, im_size, num_pixel))