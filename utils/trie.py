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
            if full_word not in node.sub_words.keys():
                node.sub_words[full_word] = 0
            node.sub_words[full_word] += delta
            if node.sub_words[full_word] == 0:
                node.sub_words.pop(full_word)
        if full:
            if full_word not in node.full_words.keys():
                node.full_words[full_word] = 0
                self.all.append(full_word)
            node.full_words[full_word] += delta
            if node.full_words[full_word] == 0:
                node.full_words.pop(full_word)
                self.all.remove(full_word)

    def insert(self, word):
        self.__process(word, 1)

    def remove(self, word):
        self.__process(word, -1)

    def __process(self, word, delta):
        self.dfs_path(word, word, True, delta)
        for i in range(len(word)):
            self.dfs_path(word[i:], word, False, delta)

    def dfs_trie(self, node, exact, limit, result):
        if len(result.all) < limit:
            if exact:
                for word in node.full_words.keys():
                    if len(result.all) < limit:
                        result.insert(word)
                    else:
                        break
            else:
                for word in node.sub_words.keys():
                    if len(result.all) < limit:
                        result.insert(word)
                    else:
                        break
                for child in node.children.values():
                    self.dfs_trie(child, exact, limit, result)

    def query(self, word, exact, limit):
        result = Trie()
        node = self.root
        for char in word:
            char = char.lower()
            if char in node.children:
                node = node.children[char]
            else:
                return result.all
        self.dfs_trie(node, exact, limit, result)
        return result.all
