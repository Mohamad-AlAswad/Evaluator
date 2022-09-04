class TrieNode:
    def __init__(self, char):
        self.char = char
        self.sub_words = {}
        self.full_words = {}
        self.children = {}


class Trie(object):
    def __init__(self):
        self.root = TrieNode("")
        self.all = []

    def dfs_path(self, word, full_word, full, delta):
        node = self.root
        for char in word:
            char = char.lower()
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        if full:
            if full_word not in node.full_words.keys():
                node.full_words[full_word] = 0
                self.all.append(full_word)
            node.full_words[full_word] += delta
            if node.full_words[full_word] == 0:
                node.full_words.pop(full_word)
                self.all.remove(full_word)

        if full_word not in node.sub_words.keys():
            node.sub_words[full_word] = 0
        node.sub_words[full_word] += delta
        if node.sub_words[full_word] == 0:
            node.sub_words.pop(full_word)

    def insert(self, word):
        self.dfs_path(word, word, True, 1)
        prefix = ''
        for c in word:
            prefix += c
            self.dfs_path(prefix, word, False, 1)

    def remove(self, word):
        self.dfs_path(word, word, True, -1)
        prefix = ''
        for c in word:
            prefix += c
            self.dfs_path(prefix, word, False, -1)

    def dfs_trie(self, node, exact, result):
        if exact:
            for word in node.full_words.keys():
                result.insert(word)
        else:
            for word in node.sub_words.keys():
                result.insert(word)
            for child in node.children.values():
                self.dfs_trie(child, exact, result)

    def query(self, word, exact):
        result = Trie()
        node = self.root
        for char in word:
            char = char.lower()
            if char in node.children:
                node = node.children[char]
            else:
                return result.all
        self.dfs_trie(node, exact, result)
        return result.all
