"""
It's a step1 for cralwing lazada data as our reliable testing data.

In this step, we'll get url for each attribute that we would like to get from the lazada webset.

Take mobile as an example, the output of the python will be:

{
 'Merek': {'Samsung': 'https://www.lazada.co.id/beli-handphone/samsung/',
  'Xiaomi': 'https://www.lazada.co.id/beli-handphone/xiaomi/',
  'Apple': 'https://www.lazada.co.id/beli-handphone/apple/',
  'Nokia': 'https://www.lazada.co.id/beli-handphone/nokia/',
  'ASUS': 'https://www.lazada.co.id/beli-handphone/asus/',
  'Advan': 'https://www.lazada.co.id/beli-handphone/advan/',
  'Evercoss': 'https://www.lazada.co.id/beli-handphone/evercoss/',
  'iCherry': 'https://www.lazada.co.id/beli-handphone/icherry/',
  'Huawei': 'https://www.lazada.co.id/beli-handphone/huawei/',
  'Sony': 'https://www.lazada.co.id/beli-handphone/sony/',
  'OPPO': 'https://www.lazada.co.id/beli-handphone/oppo/',
  'brandcode': 'https://www.lazada.co.id/beli-handphone/brandcode/',
  'Mito': 'https://www.lazada.co.id/beli-handphone/mito/'},

 'Color Family': {'Gold': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:12560',
  'White': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:37689',
  'Silver': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:14788',
  'Blue': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:9985',
  'Red': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:17131',
  'Pink': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:6732',
  'Clear': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:3462',
  'Green': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:6266',
  'Brown': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:17600',
  'Orange': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:12784',
  'Rose': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:34740',
  'Light Grey': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:79599',
  'Rose Gold': 'https://www.lazada.co.id/beli-handphone/?ppath=30113:78353'},

}

@author: Ray
"""

import os
import json
import unicodedata
import copy
import pandas as pd
from time import sleep
from selenium import webdriver
import argparse


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

if __name__ == "__main__":
    for category in ['mobile','lips','face','women_top','women_dress'][-2:]:
        #--------------------
        # standard setting
        #--------------------
        #current_folder = os.path.dirname(os.path.abspath('.'))
        path2driver = '../chromedriver'
        driver = webdriver.Chrome(path2driver)
        print('Standard-Successfully launch driver')

        #--------------------
        # customized setting
        #--------------------
        if category == 'mobile':
            start_urls = ['https://www.lazada.co.id/beli-handphone']
            attr_tree_path = '../attribute_tree/mobile/mobile_ID_attribute.json'
        elif category == 'lips':
            start_urls = ['https://www.lazada.co.id/beli-make-up-bibir']
            attr_tree_path = '../attribute_tree/beauty/beauty_attribute_v1.json'
        elif category == 'face':
            start_urls = ['https://www.lazada.co.id/makeup-wajah']
            attr_tree_path = '../attribute_tree/beauty/beauty_attribute_v1.json'
        elif category == 'women_top':
            start_urls = ['https://www.lazada.co.id/kaos-wanita']
            attr_tree_path = '../attribute_tree/fashion/fashion_attribute_v1.json'
        elif category == 'women_dress':
            start_urls = ['https://www.lazada.co.id/gaun-wanita']
            attr_tree_path = '../attribute_tree/fashion/fashion_attribute_v1.json'
        else:
            assert False, 'so far the category only support mobile,lips,face,women_top and women_dress'

        #--------------------
        # get all attribute values we're caring about
        #--------------------
        with open(attr_tree_path) as f:
            attr_tree = json.load(f)


        all_attr_value = []
        for attr_type in attr_tree.keys():
            print ('attr_type : {}'.format(attr_type))
            for attr in list(attr_tree[attr_type].keys()):
                print ('attr : {}'.format(attr))
                all_attr_value.append(attr.lower())
        all_attr_value = set(all_attr_value)     

        #------------------
        # web observation
        #------------------
        attribute_divs_class = "c2cYd1"
        attribute_type_class = "cnHBqi"
        attribute_block_class = "c3NQn0"
        url_class = "ant-checkbox-input" # for finding click press
        selected_attributes_types = []

        driver.get(start_urls[0])


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
                        if attribute_name.lower() in all_attr_value:
                            att_list.update({attribute_name: url})
                        else:
                            pass
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
        output_dir = '../output/ID/{}'.format(category)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        with open(os.path.join(output_dir,'{}_ID_attribute_url.json'.format(category)), 'w') as fp:
            json.dump(result, fp)
        print ('Successfully saving the result')

        driver.close()




