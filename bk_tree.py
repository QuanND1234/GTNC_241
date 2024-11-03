class BKNode:
    def __init__(self, word):
        self.word = word
        self.children = {}

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

class BKTree:
    def __init__(self):
        self.root = None

    def insert_word(self, word):
        if not self.root:
            self.root = BKNode(word)
        else:
            self._insert_word(word, self.root)

    def _insert_word(self, word, node):
        distance = levenshtein_distance(word, node.word)
        if distance in node.children:
            self._insert_word(word, node.children[distance])
        else:
            node.children[distance] = BKNode(word)

    def query(self, word, max_distance):
        results = []
        if self.root:
            self._query(word, self.root, max_distance, results)
        return results

    def _query(self, word, node, max_distance, results):
        distance = levenshtein_distance(word, node.word)
        if distance <= max_distance:
            results.append(node.word)
        
        for d in range(max(0, distance - max_distance), distance + max_distance + 1):
            if d in node.children:
                self._query(word, node.children[d], max_distance, results)


def all():
    tree = BKTree()
    words = ["hell", "help", "shell", "smell", "fell", "felt", "oops", "pop", "oouch", "halt"]
    
    for word in words:
        tree.insert_word(word)
    
    max_dist = 2
    
    query_word = "ops"
    matches = tree.query(query_word, max_dist)
    
    print(f"Words similar to '{query_word}' within distance {max_dist}: {matches}")

    query_word = "helt"
    matches = tree.query(query_word, max_dist)
    
    print(f"Words similar to '{query_word}' within distance {max_dist}: {matches}")
    return

# Example usage
if __name__ == "__main__":
    all()
    print(levenshtein_distance('kitten', 'sitting'))