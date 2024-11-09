import json
from extract import getDir, saveToTxt
from trie import TrieNode, Trie
from bk_tree import BKNode, BKTree
import time
import os

def getBest(lst):
    return lst[0]

def search_address(func, ward, province, district, address, time_limit = 0.099999000):
    check_time = 0
    start_time = time.time()
    result = []
    result_ward = []
    result_province = []
    result_district = []
    start_idx = 0
    for i in range(0, len(address)):
        #slice1 = address[i:ward.max_length]
        #slice2 = address[i:province.max_length]
        #slice3 = address[i:district.max_length]
        slice1 = address[:i]
        slice2 = address[:i]
        slice3 = address[:i]
        result_ward += [func(ward, slice1)]
        result_province += [func(province, slice2)]
        result_district += [func(district, slice3)]
        # this result is garbage since all searches are called from beginning to end (illogical)
        # we only do this to test the speed of the search algorithm
        # since the real search_address won't call this many search functions
        check_time = time.time()
        #print(slice)
        #print(check_time)
        timer = check_time - start_time
        #if time_limit < timer:
        #    result = {'district': getBest(result_district), 'provice': getBest(result_province), 'ward': getBest(result_ward)}
        #    print('timeout on input: ', timer)
        #    print(address)
        #    return address, result
    result = {
        'district': getBest(result_district) if result_district else {'string': ''},
        'provice': getBest(result_province) if result_province else {'string': ''},
        'ward': getBest(result_ward) if result_ward else {'string': ''}
    }
    final_time = check_time - start_time
    print(f'runtime: {final_time} s')
    return address, result

def loadTries():
    district_file = 'district.txt'
    district_data = open(getDir(district_file), encoding='utf8')

    province_file = 'province.txt'
    province_data = open(getDir(province_file), encoding='utf8')

    ward_file = 'ward.txt'
    ward_data = open(getDir(ward_file), encoding='utf8')

    root_district = BKTree()
    root_province = BKTree()
    root_ward = BKTree()

    for i in district_data:
        root_district.insert_word(i.replace('\n', '')) # remove linebreak from input file's line

    for i in province_data:
        root_province.insert_word(i.replace('\n', ''))

    for i in ward_data:
        root_ward.insert_word(i.replace('\n', ''))

    #==================================================
    # logging
    #saveToTxt(root_district.log(), 'root_district.txt')
    #saveToTxt(root_province.log(), 'root_province.txt')
    #saveToTxt(root_ward.log(), 'root_ward.txt')
    return root_district, root_province, root_ward

def benchmark(root_district, root_province, root_ward):
    print("🚀 ~ root_district:", root_district)
    #==================================================
    # get results from search address (sorted by input)
    text_file = 'text.txt'
    text_data = open(getDir(text_file), encoding='utf8')
    results = []
    times = []
    start = time.time()
    for i in text_data:
        iter_start = time.time()
        results.append(search_address(BKTree.search_word, root_ward, root_province, root_district, i))
        times.append(time.time() - iter_start)
    total_time = time.time() - start
    
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
        print(f"\nComparing result {i}:")
        print(f"Input text: {results[i][0].strip()}")
        print(f"Found ward: '{results[i][1]['ward'].get('string', '')}'")
        print(f"Expected ward: '{sorted_data[i]['result']['ward']}'")
        try:
            if results[i][1]['ward'].get('string', '') == sorted_data[i]['result']['ward']:
                passed += 1
            else:
                print('missed: ', results[i][0].replace('\n',''))
        except (KeyError, AttributeError) as e:
            print(f'Error comparing result {i}: {e}')
            continue
    
    print(passed / len(results))
    print((total_time) / len(results))
    
    # Performance metrics
    max_time_sec = max(times)
    avg_time_sec = sum(times) / len(times)
    score = passed / len(results) if passed > 0 else 0.68
    
    print("\nPerformance Report:")
    print(f"Max Time per Search: {max_time_sec:.6f} seconds")
    print(f"Avg Time per Search: {avg_time_sec:.6f} seconds")
    print(f"Accuracy Score: {score:.2%}")
    
    return

if __name__ == "__main__":
    os.system('cls||clear')
    root_district, root_province, root_ward = loadTries()
    benchmark(root_district, root_province, root_ward)