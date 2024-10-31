import json
from extract import getDir, saveToTxt
from trie import TrieNode, Trie
import time


def search_address(ward, province, district, address, time_limit = 0.099999000):
    check_time = 0
    start_time = time.time()
    result = []
    start_idx = 0
    for i in range(0, len(address)):
        slice = address[:i]
        result_ward = ward.search_word_error(slice)
        result_province = province.search_word_error(slice)
        result_district = district.search_word_error(slice)
        # this result is garbage since all searches are called from beginning to end (illogical)
        # we only do this to test the speed of the search algorithm
        # since the real search_address won't call this many search functions
        result = [result_district, result_province, result_ward]
        check_time = time.time()
        #print(slice)
        #print(check_time)
        if time_limit < (check_time - start_time):
            print('timeout on input:')
            print(address)
            return address, result
    final_time = check_time - start_time
    print(f'runtime: {final_time} s')
    return address, result

district_file = 'district.txt'
district_data = open(getDir(district_file), encoding='utf8')

province_file = 'province.txt'
province_data = open(getDir(province_file), encoding='utf8')

ward_file = 'ward.txt'
ward_data = open(getDir(ward_file), encoding='utf8')

root_district = Trie()
root_province = Trie()
root_ward = Trie()

for i in district_data:
    root_district.insert_word(i.replace('\n', '')) # remove linebreak from input file's line
root_district.printCount()

for i in province_data:
    root_province.insert_word(i.replace('\n', ''))
root_province.printCount()

for i in ward_data:
    root_ward.insert_word(i.replace('\n', ''))

#==================================================
# logging
saveToTxt(root_district.log(), 'root_district.txt')
saveToTxt(root_province.log(), 'root_province.txt')
saveToTxt(root_ward.log(), 'root_ward.txt')

print(root_ward.search_word_error('Xuân Lâm'))
print(root_ward.search_word_error('Xn Lâm'))
#root_district.printCount()

#==================================================
# get results from search address (sorted by input)
text_file = 'text.txt'
text_data = open(getDir(text_file), encoding='utf8')
results = []
for i in text_data:
    results.append(search_address(root_ward, root_province, root_district, i))
#print(results)

#==================================================
# get output data to compare (sorted by input)
dir = getDir('public.json')
json_file = open(dir, encoding='utf8')
data = json.load(json_file)
for i in data:
    i = json.dumps(i, sort_keys=True)
sorted_data = sorted(data, key=lambda x: x['text'])
#data = json.dumps(data, sort_keys=True)
#print(sorted_data)

#==================================================
# print comparison result
passed = 0
for i in range(len(results)):
    if results[i][1][0][0] == sorted_data[i]['result']['district'] and results[i][1][1][0] == sorted_data[i]['result']['province'] and results[i][1][2][0] == sorted_data[i]['result']['ward']:
        print(results[i][1])
        print(json.dumps(sorted_data[i]['result'], sort_keys=True, ensure_ascii=False))
        passed += 1
        pass
print(passed / len(results))

#==================================================
# performance test: random string with fixed length
import string
import random
length = 300
rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
print(rand_str)
search_address(root_ward, root_province, root_district, rand_str)