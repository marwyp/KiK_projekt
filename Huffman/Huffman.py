import binarytree


class DynamicHuffmanCode:
    def __init__(self, auxiliary_code=None, show_progress=False):
        # initial variables
        self.show_progress = show_progress
        self.tree = AdaptiveHuffmanNode("NYT", 0)
        self.auxiliary_code = auxiliary_code

        # show progress
        if self.show_progress:
            print("-----------Initialized tree-----------")
            print(self.tree)

    # reset tree
    def reset(self):
        self.tree = AdaptiveHuffmanNode("NYT", 0)

    # code given word with adaptive Huffman Code
    def coder(self, word: str):
        coded_word = ""
        for letter in word:
            # print progress
            if self.show_progress:
                print("----------Current letter:", letter, "----------")

            # update tree
            old_node = self.get_node(letter)
            if old_node is None:
                # send NYT and letter in auxiliary code
                coded_word += (self.get_symbol_code("NYT") + DynamicHuffmanCode.get_auxiliary_code(letter,
                                                                                                   self.auxiliary_code))
                if self.show_progress:
                    print("Codded word:", coded_word)
                # insert letter to tree
                self.insert_new_node(letter)
            else:
                # send letter
                coded_word += self.get_symbol_code(letter)
                if self.show_progress:
                    print("Codded word:", coded_word)
                # update letter in tree
                self.update_node(old_node)

            # show progress
            if self.show_progress:
                print("Current version of tree:")
                print(self.tree)
                print(self.get_nodes(True))
                print(" ")
        return coded_word

    # decode given word with adaptive Huffman Code
    def decoder(self, word: str):
        decoded_word = ""
        i = 0
        while i < len(word):
            # check if NYT is prefix for next letter
            len_of_nyt = len(self.get_symbol_code("NYT"))
            if word[i:i + len_of_nyt] == self.get_symbol_code("NYT"):
                # get letter from auxiliary code
                letter = DynamicHuffmanCode.get_letter_from_auxiliary_code(word[i + len_of_nyt:i + len_of_nyt + 8])
                i += len_of_nyt + 8
                # insert letter to tree
                self.insert_new_node(letter)
                decoded_word += letter
            else:
                # loop adding next bits and check if this is in tree
                j = 1
                while True:
                    # get letter
                    letter = self.get_letter_from_code(word[i:i + j])
                    if letter is not None and letter != "node":
                        i += j
                        # update letter in tree
                        self.update_node(self.get_node(letter))
                        decoded_word += letter
                        break
                    j += 1

        return decoded_word
    # insert symbol in NYT place
    def insert_new_node(self, symbol):
        nyt = self.get_node("NYT")
        nyt.left = AdaptiveHuffmanNode("NYT", 0, nyt)
        nyt.right = AdaptiveHuffmanNode(symbol, 1, nyt)
        nyt.value = "node"
        nyt.weight = nyt.left.weight + nyt.right.weight
        self.update_tree()

    # updates node
    def update_node(self, node):
        node.weight += 1
        self.update_tree()

    # update tree structure
    def update_tree(self):
        # update weights
        self.tree.update_weights()

        # show progress
        if self.show_progress:
            print("Updating tree")
            print(self.tree)
            print(self.get_nodes(True))

        # update
        flag = True
        while flag:
            flag = False
            tree_list = self.get_nodes()
            for i in range(len(tree_list) - 1):
                if tree_list[i].weight > tree_list[i + 1].weight:
                    self.swap_nodes(i, i + 1)
                    self.tree.update_weights()
                    # show progress
                    if self.show_progress:
                        print(self.tree)
                        print(self.get_nodes(True))
                    flag = True
                    break

        if self.show_progress:
            print("Tree updated")

    # swap 2 nodes, indices from list
    def swap_nodes(self, ind1, ind2):
        # convert indices
        ind1 = self.list2tree_index(ind1)
        ind2 = self.list2tree_index(ind2)

        # show progress
        if self.show_progress:
            print("SWAP:", self.tree[ind1].value, self.tree[ind1].weight, "<->", self.tree[ind2].value,
                  self.tree[ind2].weight)

        # values
        node1 = self.tree[ind1]
        node2 = self.tree[ind2]
        node1_parent = self.tree[ind1].parent
        node2_parent = self.tree[ind2].parent

        eq1 = node1_parent.left == node1
        eq2 = node2_parent.left == node2

        # SWAP nodes in parents
        if eq1:
            self.tree[ind1].parent.left = node2
        else:
            self.tree[ind1].parent.right = node2

        if eq2:
            self.tree[ind2].parent.left = node1
        else:
            self.tree[ind2].parent.right = node1

        # SWAP parents in nodes
        self.tree[ind1].parent = node1_parent
        self.tree[ind2].parent = node2_parent

    # get nodes list
    def get_nodes(self, string=False):
        tree_list = list()
        levels = self.tree.levels
        for i in range(len(levels) - 1, -1, -1):
            for node in levels[i]:
                tree_list.append(node)
        if string is False:
            return tree_list
        else:
            return [(node.value + " " + str(node.weight)) for node in tree_list]

    # get node using symbol
    def get_node(self, symbol):
        node_to_return = None
        for node in self.get_nodes():
            if node.value == symbol:
                node_to_return = node
                break
        return node_to_return

    # converts indexes from list to index from tree class
    def list2tree_index(self, index):
        desired_element = self.get_nodes()[index]
        # self.tree.pprint(index=True)
        # print(self.tree.values)
        for i in range(len(self.tree.values)):
            if self.tree.values[i] is not None:
                if desired_element == self.tree[i]:
                    return i

    # get symbol code from tree
    def get_symbol_code(self, symbol, tree=None, code=""):
        if tree is None:
            # tree is NYT only
            if len(self.tree) == 1:
                return "0"
            # else tree is the whole tree
            tree = self.tree
        if tree.value == symbol:
            return code
        else:
            left_code = None
            right_code = None
            if tree.left is not None:
                left_code = self.get_symbol_code(symbol, tree.left, code + "0")
            if tree.right is not None:
                right_code = self.get_symbol_code(symbol, tree.right, code + "1")
            if left_code is not None:
                return left_code
            if right_code is not None:
                return right_code
            return None

    def get_letter_from_code(self, code):
        tree = self.tree
        for i in range(len(code)):
            if code[i] == "0":
                tree = tree.left
            else:
                tree = tree.right
        return tree.value
    # returns auxiliary code from given symbol
    @staticmethod
    def get_auxiliary_code(symbol, code=None):
        if code is None:
            return symbol
        elif code == "ASCII" or code == "ASCII-8":
            return DynamicHuffmanCode.get_ascii_code(symbol, 8)
        elif code == "ASCII-7":
            return DynamicHuffmanCode.get_ascii_code(symbol, 7)
        else:
            return symbol

    @staticmethod
    def get_letter_from_auxiliary_code(code):
        if len(code) == 1:
            return code
        else:
            return chr(int(code, 2))
    # returns ASCII of given symbol
    @staticmethod
    def get_ascii_code(symbol, mode=7):
        if mode != 7 and mode != 8:
            raise Exception
        ascii_code = ord(symbol)
        ascii_code = format(ascii_code, 'b')
        while len(ascii_code) != mode:
            ascii_code = "0" + ascii_code
        return ascii_code


# Huffman Binary Tree Node with weight
class AdaptiveHuffmanNode(binarytree.Node):
    def __init__(self, symbol, weight, parent=None):
        super().__init__(symbol)
        self.weight = weight
        self.parent = parent
        self.index = 0

    def update_weights(self):
        # update weights
        if self.left.value == "node":
            self.left.update_weights()
        if self.right.value == "node":
            self.right.update_weights()

        # update weight
        self.weight = self.left.weight + self.right.weight




