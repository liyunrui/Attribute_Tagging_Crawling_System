"""
It's a step2 for cralwing lazada data as our reliable testing data.

@author: Ray
"""

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
            url_file_path = '../output/ID/mobile/mobile_ID_attribute_url.json'
            attribute_folder_path = '../output/ID/mobile/'
        elif category == 'lips':
            start_urls = ['https://www.lazada.co.id/beli-make-up-bibir']
            attr_tree_path = '../attribute_tree/beauty/beauty_attribute_v1.json'
            url_file_path = '../output/ID/lips/lips_ID_attribute_url.json'
            attribute_folder_path = '../output/ID/lips/'
        elif category == 'face':
            start_urls = ['https://www.lazada.co.id/makeup-wajah']
            attr_tree_path = '../attribute_tree/beauty/beauty_attribute_v1.json'
            url_file_path = '../output/ID/face/face_ID_attribute_url.json'
            attribute_folder_path = '../output/ID/face/'
        elif category == 'women_top':
            start_urls = ['https://www.lazada.co.id/kaos-wanita']
            attr_tree_path = '../attribute_tree/fashion/fashion_attribute_v1.json'
            url_file_path = '../output/ID/women_top/women_top_ID_attribute_url.json'
            attribute_folder_path = '../output/ID/women_top/'
        elif category == 'women_dress':
            start_urls = ['https://www.lazada.co.id/gaun-wanita']
            attr_tree_path = '../attribute_tree/fashion/fashion_attribute_v1.json'
            url_file_path = '../output/ID/women_dress/women_dress_ID_attribute_url.json'
            attribute_folder_path = '../output/ID/women_dress/'
        else:
            assert False, 'so far the category only support mobile,lips,face,women_top and women_dress'
        #--------------------
        # get all attribute values we're caring about
        #--------------------
        with open(url_file_path, 'r') as pf:
            url_file = json.load(pf)

        attribute_types = url_file.keys()

        error_div_class = 'c1nVRb'
        navigate_list_class = 'cpF1IH'
        url_suffix = '?page='
        attribute_types = []
        for attr_type in url_file:
            if len(url_file[attr_type])!=0:
                #print (attr_type)
                attribute_types.append(attr_type)
        #-----------------
        # main
        #-----------------
        for key in attribute_types:
            print ('Start to crawl items with attribute type {}'.format(key))
            #-------------------------
            # setting for saving attribute_name.txt
            #-------------------------
            attributes = url_file[key]

            key_name = key.split('/')
            save_name = ''
            for tmp in key_name:
                save_name += tmp + '_'
            print ('save_name : {}'.format(save_name))
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