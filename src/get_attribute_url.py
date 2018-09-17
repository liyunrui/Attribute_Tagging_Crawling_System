#! /usr/bin/env python3
'''

Please put the following instruction in the terminal
python3 get_attribute_url.py -c face
python3 get_attribute_url.py -c lips
python3 get_attribute_url.py -c mobile

'''
import os
import json
import unicodedata
import copy
import pandas as pd
from time import sleep
from selenium import webdriver
import argparse

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
attribute_block_class = "c3NQn0"
url_class = "ant-checkbox-input" # for finding click press
selected_attributes_types = []

driver.get(start_urls[0])


def get_attribute_url(current_driver, i_type_block, j_attribute):
    attribute_div = current_driver.find_elements_by_class_name(attribute_divs_class)[i_type_block]

    try:
        collapse = attribute_div.find_element_by_class_name("c1qSmo")
        collapse.click()
        sleep(0.5)
    except Exception as e:
        print('find collapse error %s' % e)

    attribute_block = attribute_div.find_elements_by_class_name(attribute_block_class)[j_attribute]
    check_box = attribute_div.find_elements_by_class_name(url_class)[j_attribute]
    span_list = attribute_block.find_elements_by_tag_name('span')
    att_name = str(span_list[-1].text)
    check_box.click()
    sleep(0.1)
    attr_url = str(driver.current_url)
    print('attribute {} url {}'.format(att_name, attr_url))
    # current_driver.back()
    sleep(0.5)

    return att_name, attr_url

#-----------------
# main
#-----------------
attribute_divs = driver.find_elements_by_class_name(attribute_divs_class)
result = dict()
for i in range(len(attribute_divs)):
    print('{}th attribute division'.format(i))
    attr_div = driver.find_elements_by_class_name(attribute_divs_class)[i]
    try:
        attr_type = str(attr_div.find_element_by_class_name(attribute_type_class).text)
        if len(selected_attributes_types) != 0:
            if attr_type not in selected_attributes_types:
                continue
            print('parse attribute type {}'.format(attr_type))
        try:
            #--------------------
            # to click view more
            #--------------------
            find_collapse = attr_div.find_element_by_class_name("c1qSmo")
            find_collapse.click()
            sleep(1)
        except Exception as e:
            print('find collapse error %s' % e)

        attribute_blocks = attr_div.find_elements_by_class_name(attribute_block_class)
        att_list = dict()
        for j in range(len(attribute_blocks)):
            try:
                attribute_name, url = get_attribute_url(driver, i, j)
                att_list.update({attribute_name: url})
                driver.get(start_urls[0])
                sleep(1)
            except Exception as e:
                print('Find url error %s'% e)

        result.update({attr_type: att_list})
        sleep(1)
    except Exception as e:
       print('Error %s' % e)

#-----------------------
# save
#-----------------------
output_dir = 'output/ID/{}'.format(category)
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)
 
with open(os.path.join(output_dir,'{}_ID_attribute_url.json'.format(category)), 'w') as fp:
    json.dump(result, fp)
print ('Successfully saving the result')

driver.close()
