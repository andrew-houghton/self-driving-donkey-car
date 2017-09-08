
import pickle
import numpy as np
import cv2
import os
from PIL import Image
from keras.models import Sequential, Model
from keras.layers import Input, Dense, Dropout, Flatten, GlobalAveragePooling2D, Activation, merge, ZeroPadding2D, BatchNormalization
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D, AveragePooling2D
from keras.utils import np_utils
from keras.layers.advanced_activations import LeakyReLU
from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator, img_to_array, array_to_img, load_img
from keras.callbacks import ModelCheckpoint
from matplotlib import pyplot

def resize_crop_one(LRS, filename):

    if(LRS == 'Left'):
        path = "Dataset/COMP3615/Left/" + filename
    elif (LRS == 'Right'):
        path = "Dataset/COMP3615/Right/" + filename
    elif (LRS == 'Straight'):
        path = "Dataset/COMP3615/Straight/" + filename
    elif(LRS == 'Testing'):
        path = "Dataset/COMP3615/Testing/" + filename
    else:
        raise Exception("??")

    img = cv2.imread(path)

    img = cv2.resize(img, (120, 120))

    img[0:40, 0:120] = 255
    img[100:120, 0:120] = 255

    if (LRS == 'Left'):
        path2 = "Dataset/COMP3615/Processed/Left/" + filename
        cv2.imwrite(path2, img)
    elif (LRS == 'Right'):
        path2 = "Dataset/COMP3615/Processed/Right/" + filename
        cv2.imwrite(path2, img)
    elif (LRS == 'Straight'):
        path2 = "Dataset/COMP3615/Processed/Straight/" + filename
        cv2.imwrite(path2, img)
    elif (LRS == 'Testing'):
        path2 = "Dataset/COMP3615/Processed/Testing_All_Straight/" + filename
        cv2.imwrite(path2, img)
    else:
        raise Exception("??")

    print("done")


# Call it using resize_crop_a_dir("Dataset/COMP3615/Straight/")
def resize_crop_a_dir(dir_name):
    from os import listdir

    if("Left" in dir_name):
        LRS = "Left"
    if ("Right" in dir_name):
        LRS = "Right"
    if ("Straight" in dir_name):
        LRS = "Straight"
    if("Testing" in dir_name):
        LRS = "Testing"

    for file_name in listdir(dir_name):
        if(str(file_name) == ".DS_Store"):
            continue

        print(file_name)
        resize_crop_one(LRS, file_name)
        # break


# Path should be the directory containing all images
# e.g. "/Users/ChesterAiGo/Desktop/PV_Dataset1/Right/"
def loadData(LRS, path):
    dir = os.listdir(path)
    num = 0
    for fileName in dir:
        if(fileName.endswith(".jpg")):
            num += 1

    data = np.zeros((num, 120, 120, 3), dtype="float32")
    label = np.zeros((num, 1), dtype="int32")

    index = 0

    for fileName in dir:
        if(fileName.endswith(".jpg")):
            img = load_img(path + fileName)
            x = img_to_array(img)
            data[index] = x

            # Left = 0, Straight = 1, Right = 2
            if(LRS == "Left"):
                label[index] = 0
            elif (LRS == "Right"):
                label[index] = 1
            elif (LRS == "Straight"):
                label[index] = 2
            else:
                print("what?")

            index += 1

    # to_categorical has to be 0 indexed
    label = np_utils.to_categorical(label, 3)

    data /= 255

    # Should be (?, 150, 150, 3) & (?)
    # For testing only
    # print("Data shape:", data.shape)
    # print("Label shape:", label.shape)

    return data, label

# For comp3615 - self_driving only, paths need to be modified when running on P2
def loadAllData(testing = False):

    path_L = "Dataset/COMP3615/Processed/Left/"
    path_R = "Dataset/COMP3615/Processed/Right/"
    path_S = "Dataset/COMP3615/Processed/Straight/"

    if(testing):
        path_L = "Dataset/COMP3615/Processed/Testing/Left/"
        path_R = "Dataset/COMP3615/Processed/Testing/Right/"
        path_S = "Dataset/COMP3615/Processed/Testing/Straight/"

    data_left, label_left = loadData("Left", path_L)
    data_right, label_right = loadData("Right", path_R)
    data_straight, label_straight = loadData("Straight", path_S)

    data = np.concatenate((data_left, data_right, data_straight))
    label = np.concatenate((label_left, label_right, label_straight))

    print("Total Data shape:", data.shape)
    print("Total Label shape:", label.shape)

    return data, label


def buildModel():
    model = Sequential()

    model.add(Conv2D(32, (3, 3), padding='same',
                     input_shape=(120, 120, 3)))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

  #  model.add(Conv2D(64, (3, 3), padding='same'))
  #  model.add(Activation('relu'))
  #  model.add(Conv2D(64, (3, 3)))
  #  model.add(Activation('relu'))
  #  model.add(MaxPooling2D(pool_size=(2, 2)))
  #  model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(3))
    model.add(Activation('softmax'))

    return model


# All the data & Label now have been loaded
data, label = loadAllData()
data_test, label_test = loadAllData(testing = True)
cp = ModelCheckpoint("3615_2nd_fromCp.hdf5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='max')
callbacks_list = [cp]

# vgg_16_model = VGG16(input_shape=(120, 120, 3), include_top=False, weights=None)
# vgg_16_model.summary()
#
# input_layer = Input(shape=(120, 120, 3))
# x = vgg_16_model.output
# x = Flatten()(x)
# x = Dense(3, activation='softmax')(x)
#
# finalModel = Model(input = vgg_16_model.input, output = x)
# finalModel.summary()

finalModel = buildModel()
# sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)

finalModel.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])

finalModel.fit(x = data, y = label, epochs = 10, validation_split=0.2, callbacks=callbacks_list, batch_size=10)

# For testing only
# finalModel.load_weights("/Users/ChesterAiGo/Desktop/All_Files/Sem2_2017/COMP3615/3615.h5")

print("Done")

score = finalModel.evaluate(x = data_test, y = label_test)

print(score[1] * 100)

# if(score[1] * 100 > 80):
#     finalModel.save('finalModel.h5')
