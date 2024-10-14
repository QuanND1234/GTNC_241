class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.value = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, value=None):
        node = self.root
        # Convert to lowercase for case-insensitive matching
        word = word.lower()
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end = True
        node.value = value if value else word

    def search_longest(self, text):
        text = text.lower()
        max_length = 0
        result = None
        n = len(text)
        
        for i in range(n):
            node = self.root
            j = i
            current_match = None
            
            while j < n and text[j] in node.children:
                node = node.children[text[j]]
                if node.is_end:
                    current_match = (node.value, j - i + 1)
                j += 1
            
            if current_match and current_match[1] > max_length:
                max_length = current_match[1]
                result = current_match[0]
        
        return result

def build_tries():
    # Build province trie
    province_trie = Trie()
    with open('province.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                # Split by | and get the province name
                parts = line.split('|')
                if len(parts) > 1:
                    province = parts[1].strip()
                    if province:
                        province_trie.insert(province)

    # Build district trie
    district_trie = Trie()
    with open('district.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) > 1:
                    district = parts[1].strip()
                    if district:
                        district_trie.insert(district)

    # Build ward trie
    ward_trie = Trie()
    with open('root_ward.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split('|')
                if len(parts) > 1:
                    ward = parts[1].strip()
                    if ward:
                        ward_trie.insert(ward)

    return province_trie, district_trie, ward_trie

def preprocess_address(text):
    """
    Preprocess address text to extract potential province, district and ward components
    Returns lists of potential matches for each component
    """
    # Common prefixes/indicators
    province_indicators = [
        "tỉnh", "t.", "t", "tinh", "tp.", "tp", "thành phố", 
        "thanh pho", "tỉnh.", "tinh."
    ]
    
    district_indicators = [
        "quận", "quan", "q.", "q", "huyện", "huyen", "h.", "h",
        "tx.", "thị xã", "thi xa", "tp.", "thành phố", "thanh pho"
    ]
    
    ward_indicators = [
        "phường", "phuong", "p.", "p", "xã", "xa", "x.", "x",
        "thị trấn", "thi tran", "tt.", "tt"
    ]

    def normalize_text(text):
        """Normalize text by removing extra spaces and converting to lowercase"""
        text = text.lower()
        text = ' '.join(text.split())
        return text
    
    def split_address(text):
        """Split address into components based on common delimiters"""
        delimiters = [',', '-', '/', ';']
        parts = [text]
        for delimiter in delimiters:
            new_parts = []
            for part in parts:
                new_parts.extend([p.strip() for p in part.split(delimiter)])
            parts = new_parts
        return [p for p in parts if p]

    # Normalize input text
    text = normalize_text(text)
    
    # Split into components
    components = split_address(text)
    
    # Initialize lists for each address component
    province_candidates = []
    district_candidates = []
    ward_candidates = []
    
    # Process each component
    for component in components:
        component = component.strip()
        
        # Check for province indicators
        for indicator in province_indicators:
            if component.startswith(indicator + " "):
                province_candidates.append(component[len(indicator):].strip())
            elif component.endswith(" " + indicator):
                province_candidates.append(component[:-len(indicator)].strip())
        
        # Check for district indicators
        for indicator in district_indicators:
            if component.startswith(indicator + " "):
                district_candidates.append(component[len(indicator):].strip())
            elif component.endswith(" " + indicator):
                district_candidates.append(component[:-len(indicator)].strip())
        
        # Check for ward indicators
        for indicator in ward_indicators:
            if component.startswith(indicator + " "):
                ward_candidates.append(component[len(indicator):].strip())
            elif component.endswith(" " + indicator):
                ward_candidates.append(component[:-len(indicator)].strip())
    
    # Add the original components as candidates if they don't match any indicators
    for component in components:
        component = component.strip()
        # Add to all candidate lists if it doesn't start with any indicators
        if not any(component.lower().startswith(ind + " ") for ind in 
                  province_indicators + district_indicators + ward_indicators):
            province_candidates.append(component)
            district_candidates.append(component)
            ward_candidates.append(component)

    return province_candidates, district_candidates, ward_candidates

def process_address(text, province_trie, district_trie, ward_trie):
    """
    Process address text and return structured result using trie matching
    """
    result = {
        "province": "",
        "district": "",
        "ward": ""
    }
    
    # Preprocess the address text
    province_candidates, district_candidates, ward_candidates = preprocess_address(text)
    
    # Try to match province
    for candidate in province_candidates:
        province = province_trie.search_longest(candidate)
        if province:
            result["province"] = province
            break
    
    # Try to match district
    for candidate in district_candidates:
        district = district_trie.search_longest(candidate)
        if district:
            result["district"] = district
            break
    
    # Try to match ward
    for candidate in ward_candidates:
        ward = ward_trie.search_longest(candidate)
        if ward:
            result["ward"] = ward
            break
    
    return result

def main():
    # Build tries
    province_trie, district_trie, ward_trie = build_tries()
    
    # Process full file
    output = []
    with open('text.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                result = process_address(line, province_trie, district_trie, ward_trie)
                print("🚀 ~ result:", result)
                output.append({
                    "text": line,
                    "result": result
                })
    
    # Write output to JSON file
    import json
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
