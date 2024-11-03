
def levenshtein(str1, str2, m=-1, n=-1):
    # str1 is empty
    if m == -len(str1)-1:
        return 0
    # str2 is empty
    if n == -len(str2)-1:
        return 0
    if str1[m] == str2[n]:
        return levenshtein(str1, str2, m - 1, n - 1)
    return 1 + min(
        # Insert
        levenshtein(str1, str2, m, n - 1),
        min(
            # Remove
            levenshtein(str1, str2, m - 1, n),
            # Replace
            levenshtein(str1, str2, m - 1, n - 1))
    )

class TrieNode:
    count = 0
    indent = '  '
    # constructor
    def __init__(self, string='', letter='', depth=0):
        self.string = string
        self.letter = letter
        self.children = []
        self.depth = depth
        # end of legit word
        self.terminal = False
        self.fragment = False
        # increase static counter
        TrieNode.count += 1
        
    # log number of nodes
    def printCount(self):
        print(TrieNode.count)
    
    # log current letter
    def logLetter(self, line_break = ''):
        #print(line_break + self.letter)
        return line_break + self.letter

    # log current string
    def logString(self, line_break = ''):
        #print(line_break + self.string)
        return line_break + self.string

    # log string recursively (find children nodes to log)
    def log(self, line_break = '\n',):
        log = ''
        log += self.logString(line_break) + ': ' + str(self.depth)
        for child in self.children:
            log += child.log(line_break + TrieNode.indent)
        return log

    # log string recursively IF current node is terminal
    def logTerminal(self, line_break = '\n'):
        log = ''
        if self.terminal:
            log += self.logString(line_break)
        for child in self.children:
            log += child.logTerminal(line_break + TrieNode.indent)
        return log
            
    # log string recursively IF current node is terminal
    def logFragment(self, line_break = '\n'):
        log = ''
        if self.fragment:
            log += self.logString(line_break)
        for child in self.children:
            log += child.logFragment(line_break + TrieNode.indent)
        return log


class Trie:
    # constructor
    def __init__(self):
        self.root = TrieNode()
        self.max_length = 0
        
    # log number of nodes
    def printCount(self):
        return self.root.printCount()
    
    # log current letter
    def logLetter(self, line_break = ''):
        return self.root.logLetter(line_break = line_break)

    # log current string
    def logString(self, line_break = ''):
        return self.root.logString(line_break = line_break)

    # log string recursively (find children nodes to log)
    def log(self, line_break = '\n',):
        return self.root.log(line_break = line_break)

    # log string recursively IF current node is terminal
    def logTerminal(self, line_break = '\n'):
        return self.root.logTerminal(line_break = line_break)
            
    # log string recursively IF current node is terminal
    def logFragment(self, line_break = '\n'):
        return self.root.logFragment(line_break = line_break)

    # basic insert
    def insert_word(self, word, current_str = '', type = 'terminal'):
        if word =='':
            return
        self.max_length = max(self.max_length, len(word))
        current_node = self.root
        # iter through input word
        for letter in word:
            current_str += letter
            found = False
            # iter though child node
            for child in current_node.children:
                if letter == child.letter:
                    # switch node
                    current_node = child
                    found = True
                    break
            if (not found):
                current_node.children.append(TrieNode(current_str, letter, current_node.depth+1))
                current_node = current_node.children[-1]
        if type == 'terminal':
            current_node.terminal = True
        elif type == 'fragment':
            current_node.fragment = True
        #print(current_str)
        return

    # basic search (Needs to enhance for auto correct)
    def search_word(self, word):
        current_node = self.root
        # iter through input word
        for letter in word:
            found = False
            # iter though child node
            for child in current_node.children:
                #print(child.letter)
                #print(child.terminal)
                if letter == child.letter:
                    # switch node
                    current_node = child
                    found = True
                    break
            if (not found):
                pass
        return {'string': current_node.string,
                'terminal': current_node.terminal}

    '''
    def search_word_leven(self, word, node=None, idx=0, lim=0.5):
        current_node = node if node else self.root
        # base cases:
        leven = levenshtein(current_node.string, word)
        if leven > 3:
            return None
            
        
        # iter through input word
        for letter in word:
            # iter though child node
            for child in current_node.children:
                child_node = self.search_word_leven(word, child)    
            if (not found):
                pass
        return {'string': current_node.string,
                'terminal': current_node.terminal,
                'leven': leven}
    '''