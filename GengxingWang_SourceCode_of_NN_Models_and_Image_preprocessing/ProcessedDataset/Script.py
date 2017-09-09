
import cv2
import numpy as np
from PIL import Image
import os

def resize_crop_one(LRS, filename):

    if(LRS == 'Left'):
        path = "/Users/ChesterAiGo/Desktop/ProcessedDataset/Left/" + filename
    elif (LRS == 'Right'):
        path = "/Users/ChesterAiGo/Desktop/ProcessedDataset/Right/" + filename
    elif (LRS == 'Straight'):
        path = "/Users/ChesterAiGo/Desktop/ProcessedDataset/Straight/" + filename
    else:
        raise Exception("??")

    img = cv2.imread(path)

    img = cv2.resize(img, (120, 120))

    img[0:40, 0:120] = 255
    img[100:120, 0:120] = 255

    if (LRS == 'Left'):
        path2 = "/Users/ChesterAiGo/Desktop/ProcessedDataset/Left/" + filename
        cv2.imwrite(path2, img)
    elif (LRS == 'Right'):
        path2 = "/Users/ChesterAiGo/Desktop/ProcessedDataset/Right/" + filename
        cv2.imwrite(path2, img)
    elif (LRS == 'Straight'):
        path2 = "/Users/ChesterAiGo/Desktop/ProcessedDataset/Straight/" + filename
        cv2.imwrite(path2, img)
    else:
        raise Exception("??")

    print("done")


# Call it using resize_crop_a_dir("Dataset/COMP3615/Straight")
def resize_crop_a_dir(dir_name):
    from os import listdir

    if("Left" in dir_name):
        LRS = "Left"
    if ("Right" in dir_name):
        LRS = "Right"
    if ("Straight" in dir_name):
        LRS = "Straight"

    for file_name in listdir(dir_name):
        if(str(file_name) == ".DS_Store"):
            continue

        print(file_name)
        resize_crop_one(LRS, file_name)
        # break



def bright_all_images():
    # enhance every pixel


    path = "/Users/ChesterAiGo/Desktop/ProcessedDataset/Straight/"

    for filename in os.listdir(path):

        if(filename.endswith(".jpg")):

            im = Image.open(path+filename)

            img_width, img_height = im.size

            for x in range(0, img_width):

                for y in range(0, img_height):
                    r, g, b = im.getpixel((x, y))

                    im.putpixel((x, y), (int(r * 1.24), int(g * 1.33), int(b * 1.21)))

            im.save(path + filename)
            print("Done")


resize_crop_a_dir("/Users/ChesterAiGo/Desktop/ProcessedDataset/Straight/")
