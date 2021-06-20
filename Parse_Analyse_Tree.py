
'''use to construct the parse_analyse_tree'''
''' include the class of ANTREE and ANNODE'''
from graphviz import Digraph
from claim import *


class ANNODE(object):
    def __init__(self, val, cnt):
        if val in TERMINAL_LIST:
            self.value = MAP_REVERSE_TERMINAL_LIST[val]
        elif val in NONTERMIAL_LIST:
            self.value = MAP_REVERSE_NONTERMINAL_EN_LIST[val]
        else:
            self.value = val   # don't forget to solve the epsilon
        self.parent = None
        self.child = []
        self.index = cnt

    def add_child(self, *node):
        '''
        add new children for the current node
        use uncertain variables
        the order must be from the left to right
        '''
        for i in node:
            self.child.append(i)

    def add_parent(self, node):
        '''
        add new parent for the current node
        '''
        self.parent = node

    def get_value(self):
        '''
        return the value
        '''
        return self.value

    def get_child(self):
        '''
        return the child
        '''
        return self.child

    def get_index(self):
        '''
        return the index
        '''
        return self.index

    def get_parent(self):
        '''
        return the parent
        '''
        return self.parent

class ANTREE(object):
    def __init__(self):
        self.root = None
        self.dot = Digraph(name="ParseTree", format="png")

    def update_root(self, node):
        '''
        change the root for this tree
        '''
        self.root = node

    def traverse(self, node):
        '''
        traverse the tree from the root
        input the root at the beginning
        '''
        print(node.get_value())
        for i in node.get_child():
            self.traverse(i)

    def get_root(self):
        return self.root

    def draw_tree_pic(self, node, cnt=0):
        '''
        use graphviz to generate the picture of tree
        input the root at the beginning
        '''
        if node == self.root:
            self.dot = Digraph(name="ParseTree", format="png")
            self.dot.node(name=str(node.get_index()), label=node.get_value())
        else:
            self.dot.node(name=str(node.get_index()), label=node.get_value())
            self.dot.edge(str(node.get_parent().get_index()), str(node.get_index()))

        for c in node.get_child():
            self.draw_tree_pic(c)

    def tree_pic_show_save(self, is_save=False, is_show=False):
        if is_show:
            self.dot.view(filename="ParseTree", directory="./")
        if is_save:
            self.dot.render(filename="ParseTree", directory="./")