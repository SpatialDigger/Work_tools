'''
This searches through all shp files in a directory and sub directories,
looking through indicated columns for specified values
'''

import os
import geopandas as gpd

''' Initiate lists '''
shapefiles = []
returned_file = []
row_list = []

''' Inputs '''
path = input('Enter the search directory: ')
col_name = input('Enter a column to search: ')
values = input('Enter a comma separated list of values you are interested in: ')

''' Recursive search for shp files '''
for root, dirs, files in os.walk(path):
	for file in files:
		if file.endswith(".shp"):
			filepath = os.path.join(root, file)
			shapefiles.append(filepath)

''' Searching through the shapefiles for the relevant values '''
for shp in shapefiles:
	gdf = gpd.read_file(shp)
	for col in col_name:
		if col in gdf:
			for value in values:
				# string and numeric handling
				search = gdf.loc[~(gdf[col] == value) | ~(gdf[col] == str(value))]
				print(search)

				if not search.empty:
					row_list.append(search)
					returned_file.append(shp)

if returned_file:
	for p in returned_file:
		print(p)
else:
	print('No data found')

if row_list:
	for r in row_list:
		print(r)



