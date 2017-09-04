
import cv2
import numpy as np

def resize_crop_one(LRS, filename):

    if(LRS == 'Left'):
        path = "Dataset/COMP3615/Left/" + filename
    elif (LRS == 'Right'):
        path = "Dataset/COMP3615/Right/" + filename
    elif (LRS == 'Straight'):
        path = "Dataset/COMP3615/Straight/" + filename
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




