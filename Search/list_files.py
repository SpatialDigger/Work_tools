'''
This searches a directory and sub directories, listing
all files with the specified extension

returns the filename, its extension, and the creation date
'''

import os
import time

''' initiate lists '''
file_list = []

''' Inputs '''
path = input('Enter the search directory:')
ext = input('define the extension:')

''' Add in the point if not in the input '''
if not ext[0] == '.':
	ext = '.' + ext

''' loop through the directory appending the files to the file_list '''
for root, dirs, files in os.walk(path):
	for file in files:
		if file.endswith(ext):
			creation_date = time.ctime(os.path.getctime(os.path.join(root, file)))
			text = file + "," + creation_date
			file_list.append(text)

''' If any file are found list them, otherwise tell the user nothing was found'''
if file_list:
	for file in file_list:
		print(file)
else:
	print('No data found')
