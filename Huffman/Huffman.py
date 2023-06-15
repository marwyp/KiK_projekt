import binarytree


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
                print(self.get_nodes())
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
        if self.show_progress:
            print("Updating tree")
        self.tree.update_weights()
        while True:
            tree_list = self.tree.postorder
            for i in range(len(tree_list) - 1):
                if tree_list[i].weight > tree_list[i + 1].weight:
                    # TODO: swap nodes
                    pass
            break
        if self.show_progress:
            print("Tree updated")

    # get nodes list
    def get_nodes(self):
        return [(node.value + " " + str(node.weight)) for node in self.tree.postorder]

    # get node using symbol
    def get_node(self, symbol):
        node_to_return = None
        for node in self.tree.postorder:
            if node.value == symbol:
                node_to_return = node
                break
        return node_to_return


class AdaptiveHuffmanNode(binarytree.Node):
    def __init__(self, symbol, weight, parent=None):
        super().__init__(symbol)
        self.weight = weight
        self.parent = parent

    def update_weights(self):
        # update weights
        if self.left.value == "node":
            self.left.update_weights()
        if self.right.value == "node":
            self.right.update_weights()

        # update weight
        self.weight = self.left.weight + self.right.weight



