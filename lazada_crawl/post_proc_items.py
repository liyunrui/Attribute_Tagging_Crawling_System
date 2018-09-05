import pandas as pd

from multiprocessing.pool import ThreadPool

pool = ThreadPool()


def parse_items(item):
    items = item.split('||')
    return items[0:4]

input_file_path = 'attribute_items/Jenis Kerah _ Leher Baju_.txt'
with open(input_file_path, 'r') as fp:
    item_list = fp.readlines()


results = pool.map(lambda item: parse_items(item), item_list)
pool.close()

results = pd.DataFrame(results, columns=['attribute_name', 'item_title', 'item_url', 'image_url']).drop_duplicates()
results.to_csv(input_file_path.split('.')[0] + '.csv', index=False)





