"""

@author: Ray

"""
#! /usr/bin/env python3
import pandas as pd
import os
pd.options.display.max_colwidth = 1000

def text_to_csv(txt_path, attr = 'brand'):
    '''
    return a Dataframe
    args:
    ---------------
    txt_path: str
    '''
    data = pd.read_csv(txt_path, sep = '\n', header = None)
    data.columns = ["tmp"]
    dict_for_df = {}
    dict_for_df.setdefault(attr, [])
#     dict_for_df.setdefault('page_num', [])
    dict_for_df.setdefault('title', [])
#     dict_for_df.setdefault('item_url', [])
#     dict_for_df.setdefault('image_url', [])
#     dict_for_df.setdefault('price', [])

    for row in data.tmp:
        row_ls = row.split('||')
        #print (row_ls)
        dict_for_df[attr].append(row_ls[0])
#         dict_for_df['page_num'].append(row_ls[1])
        dict_for_df['title'].append(row_ls[2])
#         dict_for_df['item_url'].append(row_ls[3])
#         dict_for_df['image_url'].append(row_ls[4])
#         dict_for_df['price'].append(row_ls[5])
        
    output = [attr,'title']
    df = pd.DataFrame(dict_for_df)[output] 
    return df
#-----------------
# mobile
#-----------------
for category in ['mobile']:
    print ('category : {}'.format(category))
    path = '../output/ID/{}'.format(category)
    attr_txt_files = [i for i in os.listdir(path) if '.json' not in i] 
    print ('number of attributes : {}'.format(len(attr_txt_files)))
    for ix, txt_file in enumerate(attr_txt_files):
        attr = txt_file.lower()[:-5].replace(' ','_')
        txt_path = os.path.join(path, txt_file)
        print ('attr : ', attr)
        #-----------
        # bahasa to English
        #-----------
        if attr == 'color_family':
            attr = 'color'
        elif attr == 'merek':
            attr = 'brand'
        elif attr == 'kapasitas_penyimpanan':
            attr = 'memory storage'
        elif attr == 'sistem_operasi':
            attr = 'operation system'
        elif attr == 'koneksi_jaringan':
            attr = 'connection network'
        else:
            pass
        df = text_to_csv(txt_path, attr = attr)
        df.drop_duplicates(subset = [attr, 'title'], inplace = True)    
        print ('shape : ', df.shape)
        if ix == 0:
            tmp = df.copy()
        elif ix == 1:
            output = pd.merge(tmp, df, on = 'title', how = 'outer') 
            output.drop_duplicates(subset = ['title'], inplace = True)  
        else:
            output = output.merge(df, on = 'title', how = 'outer')
            output.drop_duplicates(subset = ['title'], inplace = True) 
    print ('output : ', output.shape)
    # save
    save_path = '../test_data/{}'.format(category)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    output.to_csv('../test_data/{}/{}_attr.csv'.format(category,category), index = False)
#-----------------
# fashion
#-----------------
outputs = []
for category in ['women_top','women_dress']:
    print ('category : {}'.format(category))
    path = '../output/ID/{}'.format(category)
    attr_txt_files = [i for i in os.listdir(path) if '.json' not in i] 
    print ('number of attributes : {}'.format(len(attr_txt_files)))
    for ix, txt_file in enumerate(attr_txt_files):
        attr = txt_file.lower()[:-5].replace(' ','_')
        txt_path = os.path.join(path, txt_file)
        print ('attr : ', attr)
        #-----------
        # bahasa to English
        #-----------
        if attr == 'color_family':
            attr = 'color'
        elif attr == 'merek':
            attr = 'brand'
        elif attr == 'tren_fashion_wanita':
            attr = 'style'
        elif attr == 'motif___detail':
            attr = 'pattern'
        elif attr == 'bahan_pakaian':
            attr = 'clothing material'
        elif attr == 'jenis_kerah___leher_baju':
            attr = 'collar'
        else:
            pass
        if attr == 'jenis_kerah':
            pass
        else:
            df = text_to_csv(txt_path, attr = attr)
            df.drop_duplicates(subset = [attr, 'title'], inplace = True)    
            if attr == 'brand':
                break
            print ('shape : ', df.shape)
            if ix == 0:
                tmp = df.copy()
            elif ix == 1:
                output = pd.merge(tmp, df, on = 'title', how = 'outer') 
                output.drop_duplicates(subset = ['title'], inplace = True)  
            else:
                output = output.merge(df, on = 'title', how = 'outer')
                output.drop_duplicates(subset = ['title'], inplace = True) 
    print ('output : ', output.shape)
    outputs.append(output)
output = pd.concat(outputs, axis = 0)  
print ('output : ', output.shape)
# save
category = 'fashion'
save_path = '../test_data/{}'.format(category)
if not os.path.exists(save_path):
    os.makedirs(save_path)
output.to_csv('../test_data/{}/{}_attr.csv'.format(category,category), index = False)
#------------------
# beauty
#------------------
outputs = []
for category in ['lips','face']:
    print ('category : {}'.format(category))
    path = '../output/ID/{}'.format(category)
    attr_txt_files = [i for i in os.listdir(path) if '.json' not in i] 
    print ('number of attributes : {}'.format(len(attr_txt_files)))
    for ix, txt_file in enumerate(attr_txt_files):
        attr = txt_file.lower()[:-5].replace(' ','_')
        txt_path = os.path.join(path, txt_file)
        print ('attr : ', attr)
        #-----------
        # bahasa to English
        #-----------
        if attr == 'color_family':
            attr = 'color_family'
        elif attr == 'merek':
            attr = 'brand'
        elif attr == 'face_makeup_finish':
            attr = 'lips Makeup finish'
        elif attr == 'tekstur_produk':
            attr = 'product form'
        else:
            pass
        if attr == 'jenis_kerah':
            pass
        else:
            df = text_to_csv(txt_path, attr = attr)
            df.drop_duplicates(subset = [attr, 'title'], inplace = True)    
            if attr == 'brand':
                break
            print ('shape : ', df.shape)
            if ix == 0:
                tmp = df.copy()
            elif ix == 1:
                output = pd.merge(tmp, df, on = 'title', how = 'outer') 
                output.drop_duplicates(subset = ['title'], inplace = True)  
            else:
                output = output.merge(df, on = 'title', how = 'outer')
                output.drop_duplicates(subset = ['title'], inplace = True) 
    print ('output : ', output.shape)
    outputs.append(output)
output = pd.concat(outputs, axis = 0)  
print ('output : ', output.shape)
# save
category = 'beauty'
save_path = '../test_data/{}'.format(category)
if not os.path.exists(save_path):
    os.makedirs(save_path)
output.to_csv('../test_data/{}/{}_attr.csv'.format(category,category), index = False)