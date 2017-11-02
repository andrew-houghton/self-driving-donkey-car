def convert_grey(dataset_folder,newfolder):
    #This function opens all the files in dataset folder
    #it converts the image to greyscale
    #it joins the depth information onto the greyscale pixel.
    #this means the data for each pixel is (greyscle value, depth value)

    import cv2
    import pickle
    import numpy as np
    import os
    # all files
    prefix='image_'
    prefixed = sorted([filename for filename in os.listdir(dataset_folder) if filename.startswith(prefix)])

    index_num=0

    for image_pickle_file in prefixed:
        if index_num%25==0:
            print('{} images have had depth removed'.format(index_num))
        index_num+=1
        #load files
        full_image = pickle.load( open( dataset_folder+'/'+image_pickle_file, "rb" ) )
        # keep depth
        red,green,blue,depth = cv2.split(full_image)
        #change colour
        grey = cv2.cvtColor( full_image, cv2.COLOR_RGB2GRAY )
        #merge greyscale pixel and depth pixel
        output_data=cv2.merge((grey,depth))
        #save file
        pickle.dump(output_data,open( newfolder + '/' + image_pickle_file , 'wb' ))

convert_grey('full_datasets/sized_250','full_datasets/greydepth_250')