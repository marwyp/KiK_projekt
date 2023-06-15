import binarytree
from copy import deepcopy


class DynamicHuffmanCode:
    def __init__(self, show_progress=False):
        self.show_progress = show_progress
        self.tree = AdaptiveHuffmanNode("NYT", 0)
        if self.show_progress:
            print("-----------Initialized tree-----------")
            print(self.tree)

    # code given word with adaptive Huffman Code
    def coder(self, word: str):
        coded_word = ""
        for letter in word:
            # code word
            coded_word += letter

            # print progress
            if self.show_progress:
                print("----------Current letter:", letter, "----------")
                print("Codded word:", coded_word)

            # update tree
            old_node = self.get_node(letter)
            if old_node is None:
                self.insert_new_node(letter)
            else:
                self.update_node(old_node)

            if self.show_progress:
                print("Current version of tree:")
                print(self.tree)
                print(self.get_nodes(True))
                print(" ")

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
        if self.show_progress:
            ind1 = self.list2tree_index(ind1)
            ind2 = self.list2tree_index(ind2)

            print("SWAP:", self.tree[ind1].value, self.tree[ind1].weight, "<->", self.tree[ind2].value, self.tree[ind2].weight)

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
            self.tree[ind1].parent = node2_parent
            self.tree[ind2].parent = node1_parent

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




