'''
Place trenches over a defined area
Work in progress
'''

import geopandas as gpd
import numpy as np

''' Inputs '''
percentage_area = 2
num_trenches = 100
len_trench = 15
width_trench = 2


#read in poly
area = 'read in polygon'
gdf = gpd.read_file("YOUR_SHAPE_FILE.shp")
gdf = gdf['geometry'].to_crs({'proj': 'cea'})

class Trench:
    def __init__(self, id, length, width):
        self.id = id
        self.length = length
        self.width = width
        self.orientation = 0

''' From a gdf and associated information calculate how many trenches are required over an area '''
def calc_number_of_trenches(gdf, trench_len, trench_width, percentage = '', trench_num = ''):

    # We either have a % coverage or a number of trenches
    if percentage:
        # get the area of the site
        site_area = gdf.area
        # get the area of a trench

        site_area = 10456 # msq
        percentage_area = 2
        trench_len = 50
        trench_width = 2
        trench_area = trench_len * trench_width

        area_sample = site_area/100 * percentage_area

        trench_num = np.ceil(area_sample/trench_area)
        return trench_num
    elif trench_num:
        return trench_num



def distribute_points(gdf, len_trench, width_trench, percentage_area, num_trenches):




def place_trenches():

    # use length, width then width, length to rotate the trenches.
    # global angle calculation, find the orientation of the site polygon

    # if the trench overlaps with another trench and/or the site boundary, move it!

    pass


# calculate how many trenches are needed
trench_num = calc_number_of_trenches(gdf, trench_len, trench_width, percentage = '', trench_num = '')

# create a trench object, give it a length, width, rotation, location

'''

'''
starting_number = 0
i=1
while i < num_trench:
    current_trench = starting_number + i
    new_trench = Trench(id=current_trench, length=50, width=2)
    print(new_trench)

    i += 1

i = 1
while i < 6:
  print(i)
  i += 1
