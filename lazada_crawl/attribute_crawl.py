import os
import json

from time import sleep
from selenium import webdriver

start_urls = ['https://www.lazada.co.id/gaun-wanita']
current_folder = os.path.dirname(os.path.abspath(__file__))
path2driver = os.path.join(current_folder, 'chromedriver')
driver = webdriver.Chrome(path2driver)
attribute_divs_class = "c2cYd1"
attribute_type_class = "cnHBqi"
attribute_name_class = "c1WzWT"

driver.get(start_urls[0])
attribute_divs = driver.find_elements_by_class_name(attribute_divs_class)
result = dict()
for attribute_div in attribute_divs:
    try:
        attribute_type = attribute_div.find_element_by_class_name(attribute_type_class).text
        print('parse attribute type {}'.format(attribute_type))
        try:
            find_callaps = attribute_div.find_element_by_class_name("c1qSmo")
            find_callaps.click()
            sleep(1)
        except Exception as e:
            print('find callaps error %s' % e)
        attributes = attribute_div.find_elements_by_class_name(attribute_name_class)
        attr_list = dict()
        for attribute in attributes:
            tmp_list = attribute.text.split('\n')
            for tmp in tmp_list:
                attr_list.update({tmp: [tmp]})
        if len(attr_list) > 0:
            result.update({attribute_type: attr_list})

    except Exception as e:
        print('Error %s' % e)

with open('gaun_wanita.json', 'w') as fp:
    json.dump(result, fp)

driver.close()
