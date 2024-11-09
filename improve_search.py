import json
import time

from extract import getDir, saveToTxt
from improve_trie import Trie, TrieNode


def search_address(ward_trie: Trie, province_trie: Trie, district_trie: Trie, address):
    time_limit = 0.08

    start_time = time.time()
    province_match = ""
    district_match = ""
    ward_match = ""

    n = len(address)
    end_index = 0
    for i in range(n):
        slice1 = address[: n - i]
        province_match, length = province_trie.search_word(slice1)

        if province_match is not None:
            print(f"matched after {length} char")
            end_index += length + i
            break

    print(f"province end_index: {end_index}, slice: {address[:n - end_index]}")

    for i in range(n - end_index):
        slice1 = address[: n - end_index - i]
        district_match, length = district_trie.search_word(slice1)

        if district_match is not None:
            print(f"matched after {length} char")
            end_index += length + i
            break

    print(f"ward end_index: {end_index}, slice: {address[:n - end_index]}")
    for i in range(n - end_index):
        slice1 = address[: n - end_index - i]
        ward_match, length = ward_trie.search_word(slice1)

        if ward_match is not None:
            print(f"matched after {length} char")
            end_index += length + i
            break

    print(f"result end_index: {end_index}, slice: {address[:n - end_index]}")

    return {
        "address": address,
        "province": province_match or "",
        "district": district_match or "",
        "ward": ward_match or "",
    }


district_file = "district.txt"
district_data = open(getDir(district_file), encoding="utf8")

province_file = "province.txt"
province_data = open(getDir(province_file), encoding="utf8")

ward_file = "ward.txt"
ward_data = open(getDir(ward_file), encoding="utf8")

root_district = Trie()
root_province = Trie()
root_ward = Trie()

for i in district_data:
    root_district.insert_word_variants(
        i.replace("\n", "")
    )  # remove linebreak from input file's line
root_district.printCount()


for i in province_data:
    root_province.insert_word_variants(i.replace("\n", ""))
root_province.printCount()

for i in ward_data:
    root_ward.insert_word_variants(i.replace("\n", ""))

root_ward.printCount()

start_time = time.time()
print(
    search_address(
        root_ward,
        root_province,
        root_district,
        "2 dãy C ngõ 16 Ngô Quyền, tổ 14, Quang Trung, Hà Đông, Hà Nội",
    )
)
end_time = time.time()

print(f"time: {end_time - start_time}")

# # ==================================================
# # get results from search address (sorted by input)
# text_file = "text.txt"
# text_data = open(getDir(text_file), encoding="utf8")
# results = []
# for i in text_data:
#     print(f"text: {i}")
#     results.append(
#         search_address(root_ward, root_province, root_district, i.replace("\n", ""))
#     )
#     break
#
# print(results[:1])
#
# # ==================================================
# # get output data to compare (sorted by input)
# dir = getDir("public.json")
# json_file = open(dir, encoding="utf8")
# data = json.load(json_file)
# for i in data:
#     i = json.dumps(i, sort_keys=True)
# sorted_data = sorted(data, key=lambda x: x["text"])
# # data = json.dumps(data, sort_keys=True)
# print(sorted_data[0])
#
# # ==================================================
# # print comparison result
# # passed = 0
# # for i in range(len(results)):
# #     if (
# #         results[i][1][2][0] == sorted_data[i]["result"]["ward"]
# #     ):  # and results[i][1][1][0] == sorted_data[i]['result']['province'] \
# #         # and results[i][1][0][0] == sorted_data[i]['result']['district']\
# #
# #         # print(results[i][0].replace('\n',''))
# #         # print(results[i][1])
# #         # print(json.dumps(sorted_data[i]['result'], sort_keys=True, ensure_ascii=False))
# #         passed += 1
# #         pass
# # print(passed / len(results))
