class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.true_word = []
        self.word = ""

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, true_word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.true_word.append(true_word)
        node.word = word
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False, None, None
            node = node.children[char]
        return node.is_end_of_word, node.true_word, node.word
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


