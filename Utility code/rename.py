import os

dataset_folder = 'dataset_carpark_2'
output_folder = 'dataset_carpark_7'
offset=6930

# all files
prefix='image_'
prefixed = sorted([filename for filename in os.listdir(dataset_folder) if filename.startswith(prefix)])

new_names=[]
for i in prefixed:
	split=i.split('_')

	old_num=int(split[1])
	new_num=str(old_num+offset)

	split[1]=new_num

	new_names.append('_'.join(split))

def rename_batch(old_name,new_name):
	for i in range(len(old_name)):
		if i%25 == 0:
			print('renamed {} files'.format(i))
		os.rename(dataset_folder + '/' + old_name[i],
			output_folder + '/' + new_name[i])

rename_batch(prefixed,new_names)
