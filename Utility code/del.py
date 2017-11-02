import os
import sys

folder_to_delete='second_dataset'

def get_image_filename(index):
    import os
    prefix='image_{}_'.format(index)
    prefixed = [filename for filename in os.listdir(folder_to_delete) if filename.startswith(prefix)]
    if len(prefixed)>0:
        return folder_to_delete+'/'+prefixed[0]
    else:
        raise FileNotFoundError("No filename found with index of {}".format(index))
        return ''


if len(sys.argv) == 3:
    try:
        start=int(sys.argv[1])
        end=int(sys.argv[2])
    except:
        print('wrong argument type')

    for i in range(start,end+1):
        file_to_del=get_image_filename(i)
        print(file_to_del)
        os.remove(file_to_del)
else:
    print('incorrect arguments.\nUsage del.py START_INDEX FINISH_INDEX')