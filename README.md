Attribute Tagging
===
First of all, crawling is only the first part of attribute tagging project. This README only include the details of cralwing system.

We all know the supervised data is very expensive in the real word. In order to get effective ground truth as testing data, I designed a crawling system to caputure Lazada data as reference.

Task Overview
===
The task is how to suggest an suitable attributes: Given a seller’s product title and category of the product, to suggest proper attribute for this product.

One of easy understanding example is we consider brand as a certain attribute. For example, given a bunch of sku by sellers, to tag them with corresponding brand.

In order to do so, we need reliable training data, product title and corresponding brand aka ground truth in the first place. That' why this crawling system is quite important for our following model establishment.

Crawling logics
===
There are three steps in our logics. Please refer to the following flowchart.

![](https://i.imgur.com/OAinf70.png)
*-the word inside parentheses is an example for understanding the flowchart.*
*-v1(Samsung) is a one specific attribute*

Please see my [code](https://github.com/liyunrui/Attribute_Tagging_Crawling_System/tree/master/src) for more details.


How to run
====
The below is an example to show how to crawl the sku of face in Lazada. We consider our attribute as brand as example. 

1.Get attribute trees.
```
python3 get_attribute_trees.py -c face
```
2.Get each attribute-level url
```
python3 get_attribute_url.py -c face
```
3.Extract SKU info given 
```
python3 extract_info.py -c face -i url_path/face_ID_attribute_url.json -t "Merek"
```

**Notice: The following command should be step-by-step executed in the terminal.**



Requirements
===
MacOS Sierra or Linux-like system(recommended), Python 3.6.5

Python packages:

- numpy==1.13.3
- pandas==0.23.0
- selenium==3.14.0
- beautifulsoup4==4.6.3
- bs4==0.0.1
