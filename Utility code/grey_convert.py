def convert_grey(dataset_folder,newfolder):
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
        #change colour
        grey = cv2.cvtColor( full_image, cv2.COLOR_RGB2GRAY )
        #save file
        pickle.dump(grey,open( newfolder + '/' + image_pickle_file , 'wb' ))

convert_grey('full_datasets/sized_250','full_datasets/grey_250')