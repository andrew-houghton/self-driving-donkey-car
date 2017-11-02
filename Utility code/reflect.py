import os
import pickle
import cv2

dataset_folder='second_dataset'
save_folder='reflected_dataset'
file_index_offset=9269

def show_image(image):
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots()
    ax.imshow(image)
    plt.show()
    plt.close()

def new_filename(original):
    original = original.replace('.pickle','')
    split_fname=original.split('_')

    # change file index
    old_num=int(split_fname[1])
    new_num=str(old_num+file_index_offset)
    split_fname[1]=new_num

    # reflect steering
    old_steer=float(split_fname[3])
    new_steer=1-old_steer
    split_fname[3]='{0:.4f}'.format(new_steer)

    return '_'.join(split_fname)+'.pickle'


# all files
prefix='image_'
prefixed = sorted([filename for filename in os.listdir(dataset_folder) if filename.startswith(prefix)])

index_num=0

for image_pickle_file in prefixed:
    if index_num%25==0:
        print('{} images have been flipped'.format(index_num))
    image = pickle.load( open( dataset_folder+'/'+image_pickle_file, "rb" ) )
    flipped = cv2.flip(image,1)
    new_fname = new_filename(image_pickle_file)
    pickle.dump( flipped, open( save_folder + '/' + new_fname, "wb"))
    index_num+=1
