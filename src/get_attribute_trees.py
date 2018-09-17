#! /usr/bin/env python3
'''

Please put the following instruction in the terminal
python3 get_attribute_trees.py -c face
python3 get_attribute_trees.py -c lips
python3 get_attribute_trees.py -c mobile

'''
import os
import json
import pandas as pd
from time import sleep
from selenium import webdriver
import argparse

def pad_1d(array, max_len):
    '''
    make all the list have same lengh through padding with zero.
    '''
    array = array[:max_len]
    length = len(array)
    padded = array + [0]*(max_len - len(array))
    return padded

#--------------------
# argument
#--------------------
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--category', type=str, required=True)

args = parser.parse_args()
category = args.category

#--------------------
# standard setting
#--------------------
current_folder = os.path.dirname(os.path.abspath(__file__))
path2driver = os.path.join(current_folder, 'chromedriver/chromedriver')
driver = webdriver.Chrome(path2driver)
print('Standard-Successfully launch driver')


#--------------------
# customized setting
#--------------------
if category == 'mobile':
    start_urls = ['https://www.lazada.co.id/beli-handphone']
elif category == 'makeup':
    start_urls = ['https://www.lazada.co.id/beli-makeup']
elif category == 'lips':
    start_urls = ['https://www.lazada.co.id/beli-make-up-bibir']
elif category == 'face':
    start_urls = ['https://www.lazada.co.id/makeup-wajah']
else:
    assert False, 'so far the category only support makeup, mobile, lips, and face'

attribute_divs_class = "c2cYd1"
attribute_type_class = "cnHBqi"
attribute_name_class = "c1WzWT"

driver.get(start_urls[0])
print('Successfully local url')

#------------------
# find div
#------------------
attribute_divs = driver.find_elements_by_class_name(attribute_divs_class) # return list of WebElement 

#-----------------------
# main
#-----------------------
result = dict()
for attribute_div in attribute_divs:
    # attribute_div: WebElement object
    try:
        attribute_type = str(attribute_div.find_element_by_class_name(attribute_type_class).text)
        print('parse attribute type {}'.format(attribute_type))
        try:
            #--------------------
            # find view more
            #--------------------
            find_callaps = attribute_div.find_element_by_class_name("c1qSmo")
            # click
            find_callaps.click()
            sleep(1)
        except Exception as e:
            print('find callaps error %s' % e)
        attributes = attribute_div.find_elements_by_class_name(attribute_name_class) #return list of WebElement 
        attr_list = dict()
        for attribute in attributes:
            # .text(): WebElement to string
            tmp_list = str(attribute.text).split('\n')
            for tmp in tmp_list:
                attr_list.update({tmp: [tmp]})
        if len(attr_list) > 0:
            result.update({attribute_type: attr_list})

    except Exception as e:
        print('Error %s' % e)

#-----------------------
# save
#-----------------------

############
# json
############
output_dir = 'output/ID/{}'.format(category)
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

with open(os.path.join(output_dir,'{}_ID_attribute.json'.format(category)), 'w') as fp:
    json.dump(result, fp)
print ('Successfully saving the result')
driver.close()

############
# csv
############
attributes = pd.DataFrame({'attributes': list(result.keys())})
attributes.to_csv(os.path.join(output_dir, '{}_ID_attributes.csv'.format(category)), index = False)

dict_for_df = {}
for k in list(result.keys()):
    dict_for_df[k] = list(result[k].keys())
max_len = max([len(dict_for_df[k]) for k in list(dict_for_df.keys())])

for k in list(dict_for_df.keys()):
    dict_for_df[k] = pad_1d(dict_for_df[k], max_len)
attribute_name = pd.DataFrame(dict_for_df)
attribute_name.to_csv(os.path.join(output_dir,'{}_ID_attribute_name.csv'.format(category)), index = False, encoding = 'utf-8')

