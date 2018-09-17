#! /usr/bin/env python3
'''

Please put the following instruction in the terminal
    python3 extract_info.py -c face -i output/ID/face/face_ID_attribute_url.json -t "Merek" 
    python3 extract_info.py -c lips -i output/ID/lips/lips_ID_attribute_url.json -t "Merek"  
    python3 extract_info.py -c mobile -i output/ID/mobile/mobile_ID_attribute_url.json -t "Merek"  

'''

from __future__ import print_function
import json
import os
import argparse
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup


def parse_current_page(page_num, current_driver, attribute_name, fp):
    '''
    write item information
    
    args:
    ----------------
    current_driver: driver
    fp: TextIOWrapper
    
    return:
        number of sku we crawled
    
    '''
    #----------------------
    # Standard way to parse webpage using soup
    #----------------------
    page_source = current_driver.page_source
    soup = BeautifulSoup(page_source, features="html5lib")
    try:
        # soup.find_all(): return lists which including <script type="application/ld+json">
        str_item_info = str(soup.find_all('script', {'type': 'application/ld+json'})[-1].text)
        # convert to dict
        contents = json.loads(str_item_info)
        item_list = contents['itemListElement']
    except Exception as e:
        print("content found error %s"% e)
        item_list = list()

    cc = 0
    for item in item_list:
        try:
            item_title = item['name']
            image_url = item['image']
            item_url = item['url']
            price = item['offers']['price'] + item['offers']['priceCurrency']
            res = attribute_name + '||' + str(page_num) + '||' + item_title + '||' + item_url + '||' + image_url + '||' + price

            fp.write(res + '\n')
            fp.flush()
            cc += 1
        except Exception as e:
            print('Writing item error %s' % e)

    return cc

#--------------------
# standard setting
#--------------------
current_folder = os.path.dirname(os.path.abspath(__file__))
path2driver = os.path.join(current_folder, 'chromedriver/chromedriver')
driver = webdriver.Chrome(path2driver)

#--------------------
# argument
#--------------------
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--url_file_path', type=str, required=True)
parser.add_argument('-t', '--selected_attribute_types', action='append', default=list(), required=False)
parser.add_argument('-a', '--selected_attributes', action='append', default=list(), required=False)
parser.add_argument('-c', '--category', type=str, required=True)
parser.add_argument('-o', '--output_folder', type=str, default=current_folder, required=False)


args = parser.parse_args()
url_file_path = args.url_file_path
selected_attribute_types = args.selected_attribute_types
selected_attributes = args.selected_attributes
category = args.category
attribute_folder_path = args.output_folder

#
#attribute_folder_path = 'output/ID/{}'.format(category)

with open(url_file_path, 'r') as pf:
    url_file = json.load(pf)

attribute_types = url_file.keys()

error_div_class = 'c1nVRb'
navigate_list_class = 'cpF1IH'
url_suffix = '?page='
selected_attribute_types  = [u'Merek'] # put the attr_types u desire to crawl in the list


#-----------------
# main
#-----------------

for key in attribute_types:
    print ('Start to crawl items with attribute type {}'.format(key))
    #-------------------------
    # setting for saving attribute_name.txt
    #-------------------------
    attributes = url_file[key]
    if key not in selected_attribute_types:
        continue
    key_name = key.split('/')
    save_name = ''
    for tmp in key_name:
        save_name += tmp + '_'
    #-------------------------
    # rewrite the file
    #-------------------------
    if os.path.exists(os.path.join(attribute_folder_path, save_name + '.txt')) is False:
        attribute_file = open(os.path.join(attribute_folder_path, save_name + '.txt'), 'w')
    else:
        attribute_file = open(os.path.join(attribute_folder_path, save_name + '.txt'), 'a')
    #-------------------------
    # Crawling information
    #-------------------------   
    for attribute in attributes.items():
        print ('Start to crawl items with attribute {} in attribute type {}'.format(attribute[0], key))
        url = attribute[1]
        attr = attribute[0]
        if len(selected_attributes) != 0:
            if attr not in selected_attributes:
                continue

        driver.get(url)

        try:
            li = driver.find_element_by_class_name(navigate_list_class).\
                    find_elements_by_tag_name('li')
            #-------------------------
            # crawling max page in the current page
            #-------------------------
            max_pages = li[-2].find_element_by_tag_name('a').text
            max_pages = int(max_pages)
        except Exception as e:
            li = None
            max_pages = 102

        total_num = 0
        for i in range(1, max_pages):
            sleep(1)

            if i != 1:
                if (len(li) == 0) or li is None:
                    break
                #-------------------------
                # for moving to the next page
                #-------------------------
                dynamica_page_url = url + url_suffix + str(i)
                driver.get(dynamica_page_url)
                #---------------
                # for error handling
                #---------------
                try:
                    # if error happens in the webpage, we need to find the error div
                    error_block = driver.find_element_by_class_name(error_div_class)
                except Exception as e:
                    error_block = None
                if error_block is not None:
                    continue
                sleep(3)

            parse_num = parse_current_page(i, driver, attr, attribute_file)
            total_num += parse_num
            print ('\r ' + str(total_num), end=" ")

        print ('\n Found {} items from attribute {} in type {}'.format(total_num, attribute[0], key))
    attribute_file.close()

driver.close()
