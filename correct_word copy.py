import re
import editdistance
import unicodedata
import json
import pandas as pd
import time

# Define file paths
province_file = 'data/province.txt'
district_file = 'data/district.txt'
ward_file = 'data/ward.txt'
test_case_file = 'data/public.json'
output_pass_file = 'output_pass.txt'
output_fail_file = 'output_fail.txt'

# Load province, district, and ward data
provinces, districts, wards = set(), set(), set()
province_abbr, district_abbr, ward_abbr = {}, {}, {}
district_ward_mapping = {}

def load_names(file_path, container, abbr_mapping):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            name = line.strip()
            container.add(name)
            parts = name.split()
            if len(parts) > 1:
                abbr = ''.join(part[0].upper() for part in parts)  # E.g., "Vĩnh Long" -> "VL"
                abbr_mapping[abbr] = name
                type1_abbr = '.'.join(part[0] for part in parts[:-1]) + '.' + parts[-1]
                abbr_mapping[type1_abbr] = name
                type2_abbr = ''.join(part[0] for part in parts[:-1]) + parts[-1]
                abbr_mapping[type2_abbr] = name

def load_ward_mapping(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            ward_name = line.strip()
            district_name = ward_name.split(",")[-1].strip()  # Extract district from ward
            if district_name not in district_ward_mapping:
                district_ward_mapping[district_name] = []
            district_ward_mapping[district_name].append(ward_name)

# Load data and abbreviations
load_names(province_file, provinces, province_abbr)
load_names(district_file, districts, district_abbr)
load_names(ward_file, wards, ward_abbr)
load_ward_mapping(ward_file)

# Prefix replacements
prefix_replacements = {
    "Ap": "Ấp",
    "F ": "Phường ",
    "F.": "Phường",
    "H ": "Huyện",
    "H. ": "Huyện",
    "H.C.M": "Hồ Chí Minh",
    "HCM": "Hồ Chí Minh",
    "Muyện": "Huyện",
    "Q.": "Quận",
    "T ": "Tỉnh",
    "T.P": "Thành phố",
    "T.Phố": "Thành phố",
    "T.p": "Thành phố",
    "T.X.": "Thị xã",
    "Thx": "Thị xã",
    "TP ": "Thành phố ",
    "TPHCM": "Thành phố Hồ Chí Minh",
    "TT ": "Thị trấn",
    "Thi trấ ": "Thị trấn ",
    "x2": "Xã",
    "X.": "Xã",
    ",H.": "Huyện"
}

stop_word_province = {
    "Tỉnh", "T ", "T. ", ",T.", ", T."
    "Thành phố", "T.P", "T.P", "T.Phố", "T.p", "TP ", "TP"
}

stop_word_district = {
    "Quận", "Q.", "Q. ", 
    "Huyện", "Muyện", "H ", "H. ", 
    "T.X.", "Thx", "TX.", ",TX", ", TX", "TX ", " TX",
    "Thành phố",
}

stop_word_ward = {
    "Phường", "H. ", "F ", "F. ", "F.", "P. ", "P.", "P ",
    "Xã", "X.", "X ", ", X"
    "Thi trấ ", "TT "
}

def replace_prefixes(text):
    for prefix, replacement in prefix_replacements.items():
        text = text.replace(prefix, replacement)
    text = re.sub(r'\b(Q|q)\.?\s*(\d+)', r'Quận \2', text)  # Replace "Q10", "q10" with "Quận 10"
    text = re.sub(r'\b(P|p|F|f)\.?\s*(\d+)', r'Phường \2', text)  # Replace "P10", "p10", "F10" with "Phường 10"
    return text

def normalize(text, retain_diacritics=True):
    text = re.sub(r"[.,]", " ", text)
    if retain_diacritics:
        text = text.lower().strip()
    else:
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        text = text.lower().strip()
    return text

def split_words(text):
    text = re.sub(r'\bT\d+\b', '', text)
    text = re.sub(r'(?<=[a-zà-ỹ])(?=[A-Z])', ' ', text)
    return text.split()

def find_best_match(text, dictionary, abbr_mapping):
    text = replace_prefixes(text)
    words = split_words(text)
    normalized_text = normalize(' '.join(words), retain_diacritics=True)
    best_match, lowest_distance = None, float('inf')

    # Check for abbreviation matches first
    for abbr, full_name in abbr_mapping.items():
        if abbr in normalized_text:
            return full_name, 0

    # Proceed with regular matching
    for start in range(len(words) - 1, -1, -1):
        for count in range(2, min(5, len(words) - start + 1)):
            phrase = ' '.join(words[start:start + count])
            normalized_phrase = normalize(phrase, retain_diacritics=True)
            for entry in sorted(dictionary):
                normalized_entry = normalize(entry, retain_diacritics=True)
                if normalized_phrase in normalized_entry or normalized_entry in normalized_phrase:
                    return entry, 0
                distance = editdistance.eval(normalized_phrase, normalized_entry)
                if distance < lowest_distance or (
                    distance == lowest_distance and len(normalized_entry) < len(best_match or '')
                ):
                    best_match = entry
                    lowest_distance = distance
    return best_match, lowest_distance

def extract_address_components(text):
    normalized_text = replace_prefixes(text)

    # Identify the province
    province, province_distance = find_best_match(normalized_text, sorted(provinces), province_abbr)
    if province_distance > 1:
        province = ""

    # Identify the district
    district_abbr_filtered = {k: v for k, v in district_abbr.items() if v != province}
    district, district_distance = find_best_match(normalized_text, sorted(districts - {province} if province else districts), district_abbr_filtered)
    if district_distance > 1:
        district = ""

    # Identify the ward
    ward_abbr_filtered = {k: v for k, v in ward_abbr.items() if v != province and v != district}
    ward, ward_distance = find_best_match(normalized_text, sorted(wards - {province, district} if province or district else wards), ward_abbr_filtered)
    if ward_distance > 1:
        ward = ""

    # If both province and district are found but ward is missing, default to a known ward
    if province and district and not ward:
        known_wards = district_ward_mapping.get(district, [])
        if known_wards:  # If there are known wards for the district
            ward = known_wards[0]  # Take the first known ward as default

    return {"province": province or "", "district": district or "", "ward": ward or ""}

# Load test cases
with open(test_case_file, 'r', encoding='utf-8') as f:
    test_cases = json.load(f)

# Run tests and store results
pass_results, fail_results = [], []
pass_count, fail_count = 0, 0

for case in test_cases:
    start_time = time.time()
    extracted = extract_address_components(case["text"])
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    expected = {
        "province": case["result"]["province"],
        "district": case["result"]["district"],
        "ward": case["result"]["ward"]
    }
    pass_fail = "Pass" if extracted == expected else "Fail"
    
    result_entry = {
        "Text": case["text"],
        "Extracted (province, district, ward)": f"{extracted['province']}, {extracted['district']}, {extracted['ward']}",
        "Expected (province, district, ward)": f"{expected['province']}, {expected['district']}, {expected['ward']}",
        "Result": pass_fail,
        "Time (s)": round(elapsed_time, 6)
    }
    
    if pass_fail == "Pass":
        pass_results.append(result_entry)
        pass_count += 1
    else:
        fail_results.append(result_entry)
        fail_count += 1

# Convert results to DataFrame for formatting
df_pass = pd.DataFrame(pass_results)
df_fail = pd.DataFrame(fail_results)

# Save results to respective files
with open(output_pass_file, 'w', encoding='utf-8') as f:
    f.write(df_pass.to_string(index=False))
    f.write(f"\n\nTotal Pass: {pass_count}")

with open(output_fail_file, 'w', encoding='utf-8') as f:
    f.write(df_fail.to_string(index=False))
    f.write(f"\n\nTotal Fail: {fail_count}")

print(f"Total Pass: {pass_count}")
print(f"Total Fail: {fail_count}")
