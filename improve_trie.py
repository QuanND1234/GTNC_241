import re

import editdistance
from unidecode import unidecode


class TrieNode:
    count = 0
    indent = "  "

    def __init__(self, string="", letter=""):
        self.children = {}
        self.is_terminated = False
        self.true_value = set()
        self.value = string
        self.letter = letter
        # self.aliases = []  # Store abbreviations or common variants here


class Trie:
    # constructor

    def __init__(self):
        self.root = TrieNode()
        self.max_length = 0

    def printCount(self):
        print(self.root.count)

    def generate_variants_within_distance(self, s, max_distance):
        def generate_variants(current, distance_left, position):
            if distance_left == 0:
                variants.add(current)
                return
            # Insertion
            for c in alphabet:
                generate_variants(
                    current[:position] + c + current[position:],
                    distance_left - 1,
                    position + 1,
                )

            # Deletion
            if position < len(current):
                generate_variants(
                    current[:position] + current[position + 1 :],
                    distance_left - 1,
                    position,
                )

            # Substitution
            if position < len(current):
                for c in alphabet:
                    generate_variants(
                        current[:position] + c + current[position + 1 :],
                        distance_left - 1,
                        position + 1,
                    )

            # Move to the next character without editing
            if position < len(current):
                generate_variants(current, distance_left, position + 1)

        alphabet = "abcdeghiklmnopqrstuvxy"  # Define the alphabet to use for insertions/substitutions
        if len(s) < 2:
            return {s}
        variants = set()
        generate_variants(s, max_distance, 0)
        return variants

    def insert_word_variants(self, word: str):
        max_distance = 1
        if len(word) >= 8:
            max_distance = 1

        rev = word[::-1]
        normalized = self.normalize(rev)
        variants = self.generate_variants_within_distance(normalized, max_distance)
        for variant in variants:
            self.insert_word(variant, word)

    def normalize(self, text):
        text = unidecode(text)  # Convert diacritics to closest ASCII representation
        text = text.lower()  # Convert to lowercase to standardize
        text = re.sub(r"\.", "", text)  # Remove periods
        text = re.sub(
            r"[^a-z0-9\s]", "", text
        )  # Remove all non-alphanumeric characters except spaces
        text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space

        text = "".join(text.split())
        # Handle specific abbreviations
        # text = text.replace('tgiang', 'tien giang')
        # text = text.replace('tp hcm', 'ho chi minh')
        # text = text.replace('tp', 'thanh pho ')
        # text = text.replace('tp ', 'thanh pho ')
        # text = text.replace('thanh pho hcm', 'ho chi minh')
        # text = text.replace('thanh pho hochiminh', 'ho chi minh')
        return text

    def insert_word(self, word, true_word, verbose=False):
        node = self.root
        if verbose:
            print(f"variant: {word}")
        for char in word:
            if verbose:
                print(f"char: {char}")
            if char not in node.children:
                node.children[char] = TrieNode()
                TrieNode.count += 1
            node = node.children[char]
            node.letter = char

        node.is_terminated = True
        node.true_value.add(true_word)
        node.value = word

    def search_word(self, word: str):
        normalized = self.normalize(word)
        print(f"normalized: {normalized}")
        normalized = normalized[::-1]
        current_node = self.root
        matches = []
        # iter through input word

        length = 0
        shorted_match = 0
        for letter in normalized:
            length += 1
            # iter though child node
            # print(f"letter: {letter}")
            # print(f"children: {current_node.children.keys()}")
            if letter in current_node.children:
                current_node = current_node.children[letter]
                if current_node.is_terminated:
                    print(
                        f"letter: {letter}, current_node: {current_node.value}, {current_node.true_value}"
                    )
                    shorted_match = length
                    matches.extend(current_node.true_value)
            else:
                # print(f"letter not found: {letter}")
                break
        # print(f"matches: {matches}")
        # print(f"trailling matches: {self.get_trailling_terminal(current_node)}")
        # trailing_matches = self.get_trailling_terminal(current_node)

        # matches = set(matches + trailing_matches)

        # TODO remove this hack
        # matches.discard("")

        # Find the string with the smallest edit distance
        min_distance = float("inf")
        closest_match = None

        print(f"word: {word}, matches: {matches}")

        for s in matches:
            distance = editdistance.eval(word, s)
            # print(f"{s} distance: {distance}")
            if distance < min_distance:
                min_distance = distance
                closest_match = s
        print(f"min_distance: {min_distance}")
        return closest_match, shorted_match

    def get_trailling_terminal(self, node: TrieNode):
        results = []

        def dfs(current_node: TrieNode, level):
            level += 1
            if level > 2:
                return
            if current_node.is_terminated:
                results.extend(current_node.true_value)
            for _, child_node in current_node.children.items():
                dfs(child_node, level)

        dfs(node, 0)
        return results
