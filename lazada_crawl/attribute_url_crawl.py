import os
import json
import unicodedata
import copy

from time import sleep
from selenium import webdriver

start_urls = ['https://www.lazada.co.id/gaun-wanita']
current_folder = os.path.dirname(os.path.abspath(__file__))
path2driver = os.path.join(current_folder, 'chromedriver')
driver = webdriver.Chrome(path2driver)
attribute_divs_class = "c2cYd1"
attribute_type_class = "cnHBqi"
attribute_block_class = "c3NQn0"
url_class = "ant-checkbox-input"
selected_attributes_types = [
                             "Kelompok Warna"]

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
    att_name = span_list[-1].text
    check_box.click()
    sleep(0.1)
    attr_url = driver.current_url
    print('attribute {} url {}'.format(att_name, attr_url))
    # current_driver.back()
    sleep(0.5)

    return att_name, attr_url


attribute_divs = driver.find_elements_by_class_name(attribute_divs_class)
result = dict()
for i in range(len(attribute_divs)):
    print('{}th attribute division'.format(i))
    attr_div = driver.find_elements_by_class_name(attribute_divs_class)[i]
    try:
        attr_type = attr_div.find_element_by_class_name(attribute_type_class).text
        if attr_type not in selected_attributes_types:
            continue
        print('parse attribute type {}'.format(attr_type))
        try:
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

with open('gaun_wanita_Kelompok_Warna_attribute_url_list.json', 'w') as fp:
    json.dump(result, fp)

driver.close()
