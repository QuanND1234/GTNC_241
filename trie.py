def levenshtein(str1, str2, m=None, n=None):
    if m == None:
        m = len(str1)
    # str2 is empty
    if n == None:
        n = len(str2)
    # str1 is empty
    if m == 0:
        return n
    # str2 is empty
    if n == 0:
        return m
    if str1[m - 1] == str2[n - 1]:
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
        
    def matchLetter(self, letter):
        return letter == self.letter
        
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
                if child.matchLetter(letter):
                    # switch node
                    current_node = child
                    found = True
                    break
            if (not found):
                pass
        return {'string': current_node.string,
                'terminal': current_node.terminal}



    # idea: given a max chance number at the beginning let's say 2, 
    # if leven increase, chance -=1
    # if leven not increase, chance +=1 but can't exceed max (2)
    # if chance < 0, auto return none
    def search_word_leven(self, word, node=None, current_leven=0, current_chance=1, max_chance=1):
        current_node = node if node else self.root
        # base cases:
        sub_word = word[:current_node.depth]
        leven = levenshtein(current_node.string, sub_word)
        if leven > current_leven:
            print('miss a chance') #NOTE: when miss a letter input word, we don't move to the next letter
            current_chance -= 1
        elif leven == current_leven and current_chance < max_chance:
            current_chance += 0.5
        print(sub_word + '|' + current_node.string + ': ' , leven, current_leven, current_chance)
        if current_chance < 0:
            print('out of chance')
            return None
        
        if sub_word == 'Bình Chau' and current_node.string == 'Bình Châu':
            i = 1
        if current_node.terminal:
            return {'string': current_node.string,
                    'terminal': current_node.terminal,
                    'leven': leven}
        
        # recursion ============================
        children = []
        result = {'string': current_node.string,
                'terminal': current_node.terminal,
                'leven': -1}
        # iter through input word
        #for letter in range(current_node.depth, len(word)):
            # iter though child node
        if current_node.depth >= len(word):
            return None
        print(word[current_node.depth] + '|child num: ', len(current_node.children))
        for child in current_node.children:
            child_node = None
            if child.matchLetter(word[current_node.depth]):
                child_node = self.search_word_leven(word, child, current_leven=leven, current_chance=current_chance)
            elif current_chance >= 0:
                child_node = self.search_word_leven(word, child, current_leven=leven, current_chance=current_chance)
                pass
            if not child_node:
                continue
            if result['leven'] == -1 or result['leven'] > child_node['leven']:
                result = child_node
                pass
        #if (not child_node):
        #    pass
        #print(result)
        return result
    