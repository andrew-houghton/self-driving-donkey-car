# Update the folder and range for images before executing

from PIL import Image
start_pos = 4535
end_pos = 4935
# open images
for i in range(start_pos, end_pos):
    folder = "/Users/Dpro/Desktop/University/USYD_Semester_2_2017/COMP3615_Project/code/selfdriving/GengxingWang_SourceCode_of_NN_Models_and_Image_preprocessing/ProcessedDataset/RedLine/"
    my_file = folder + str(i) + "_cam-image_array_"
    im = Image.open(my_file + ".jpg")

    # enhance every pixel
    img_width = 159
    img_height = 119
    for x in range(0, img_width):
       for y in range(0, img_height):
           r, g, b = im.getpixel((x, y))

           # using pixel logic values from  https://github.com/KENJU/enhanshot#enhanshotjs
           im.putpixel( (x,y), (int(r * 1.24),int(g * 1.33),int(b * 1.21)))

    im.save(my_file + "new.jpg" )
