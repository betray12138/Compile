
''' used to generate the table of SLR'''
from queue import Queue
from FIRST_FOLLOW_SET import *
from Parse_Analyse_Tree import ANTREE, ANNODE
from claim import *
from Semantic_analyse import *

class SLR(FIRST_FOLLOW):
    def __init__(self, grammar_list, start):
        '''
        grammar_list: not exist the grammar like A->aB|Ca
        start: the start character of the grammar
        '''
        super(SLR, self).__init__(grammar_list, start)
        self.nonterminal = NONTERMIAL_LIST
        self.active_closure = []                      # record the active_project_closure
        self.transfer = []                            # aim the active_closure to record the transition condition
        self.living_prefix = [[] for i in range(Array_Num+1)]
        self.gen_extend_grammar()
        self.get_active_project()
        self.order_grammar = []
        self.action_table = []
        self.goto_table = []
        self.gen_order_grammar()
        self.construct_action_goto_table()
        self.tree = ANTREE()

    def gen_extend_grammar(self):
        '''
        fill the living_prefix
        '''
        # first solve the condition of S' -> E
        self.living_prefix[Array_Num].append("."+self.start)
        self.living_prefix[Array_Num].append(self.start+".")

        # second solve the condition of others
        tmp_cnt_epsilon = False  # solve the condition of meeting epsilon
        for c in range(len(self.grammar_list)):
            for i in range(len(self.grammar_list[c])):
                for j in range(len(self.grammar_list[c][i])+1):
                    if j < len(self.grammar_list[c][i]) and self.grammar_list[c][i][j] == 'e' and tmp_cnt_epsilon is False:
                        tmp_cnt_epsilon = True
                        continue
                    elif self.grammar_list[c][i][j-1] == 'e' and tmp_cnt_epsilon is True:
                        tmp_cnt_epsilon = False
                        self.living_prefix[c].append(self.grammar_list[c][i][0:j-1] + "." + self.grammar_list[c][i][j:])
                    else:
                        self.living_prefix[c].append(self.grammar_list[c][i][0:j]+"."+self.grammar_list[c][i][j:])

                    # remove the epsilon within the prefix
                    self.living_prefix[c][len(self.living_prefix[c])-1] = \
                        self.living_prefix[c][len(self.living_prefix[c])-1].replace("e", "")

    def get_project_closure(self, prefix_list):
        '''
        input the set of prefix_list, and return the project_closure
        the form of prefix_set like ['S->.E','A->a.']
        '''
        ret_list = prefix_list
        index = 0

        # when the meet_length unchanged and cnt == meet_length could confirm the project closure
        meet_length = len(ret_list)
        cnt = 0

        while True:
            dot_pos = ret_list[index].index(".")
            if dot_pos + 1 < len(ret_list[index]) and ret_list[index][dot_pos+1] in self.nonterminal:
                for c in self.living_prefix[self.search_set_index(ret_list[index][dot_pos+1])]:
                    if c[0] == ".":
                        tmp_ret = ret_list[index][dot_pos+1] + "->" + c
                        try:
                            ret_list.index(tmp_ret)
                        except ValueError:
                            ret_list.append(tmp_ret)

            if len(ret_list) == meet_length:
                cnt += 1
                if cnt == meet_length:
                    break
            else:
                meet_length = len(ret_list)
                # clear the count of cnt and recount
                cnt = 0
            index = (index+1) % meet_length

        return ret_list

    def get_closure_through_one_char(self, prefix_list, char):
        '''
        prefix_list: the list of the prefix
        function: [S'->.a S'->.aBc, S'->A.ac, S'->.bc] =>a [S'->a. S'->a.Bc S'->Aa.c]
        '''
        ret_list = []
        for c in prefix_list:
            dot_pos = c.index(".")
            if dot_pos + 1 < len(c) and c[dot_pos+1] == char:
                ret_list.append(c[0:dot_pos] + char + "." + c[dot_pos+2:])

        return ret_list

    def get_active_project(self):
        '''
        fill the active_closure and transfer
        the form of transfer like {'character':index}
        '''
        tmp_project = []
        tmp_project.append("1->" + self.living_prefix[Array_Num][0])  # append the prefix like S'->.E

        tmp_init_active_closure = set(self.get_project_closure(tmp_project))   # use set in order to index
        self.active_closure.append(tmp_init_active_closure)
        queue = Queue()
        queue.put(tmp_init_active_closure)

        while not queue.empty():
            tmp_active_closure = queue.get()
            tmp_transfer = {}
            for c in self.terminal + self.nonterminal:
                tmp_go_function = self.get_closure_through_one_char(tmp_active_closure, c)
                # tmp_go_function may be null set
                if len(tmp_go_function) == 0:
                    continue
                tmp_generate_new_closure = set(self.get_project_closure(tmp_go_function))
                try:
                    self.active_closure.index(tmp_generate_new_closure)
                except ValueError:
                    self.active_closure.append(tmp_generate_new_closure)
                    queue.put(tmp_generate_new_closure)
                des_pos = self.active_closure.index(tmp_generate_new_closure)
                tmp_transfer[c] = des_pos
            self.transfer.append(tmp_transfer)

    def construct_action_goto_table(self):
        '''
        fill the action_table and goto_table
        active_table use map like a=[{"i":1,"+":2},{"i":2,"+":3}]
        goto_table use map like {"E":1, "A":2}
        make sure has no send-reduct conflict and reduct-reduct conflict
        '''
        # fill the action_table
        for i in range(len(self.active_closure)):
            tmp_action = {}
            tmp_terminal_list = self.terminal
            tmp_terminal_list.append('#')
            for c in tmp_terminal_list:
                if self.transfer[i].get(c, -1) != -1:
                    tmp_action[c] = 's' + str(self.transfer[i][c])
                else:
                    tmp_reduct = False
                    for j in self.active_closure[i]:
                        dot_pos = j.index(".")
                        if dot_pos == len(j) - 1:   # "." is at the end
                            if j[0] == "1":   # omit the condition of "1->E."
                                continue
                            if c in self.follow_set[self.search_set_index(j[0])]:
                                tmp_search = j[:-1] + 'e' if len(j[:-1]) == 3 else j[:-1]
                                tmp_action[c] = "r" + str(self.order_grammar.index(tmp_search))
                                tmp_reduct = True
                                break
                    if tmp_reduct is False:
                        tmp_action[c] = "error"
            self.action_table.append(tmp_action)

        # solve the condition of acc  => "S'->E."
        for i in range(len(self.active_closure)):
            if "1->" + self.start + "." in self.active_closure[i]:
                self.action_table[i]["#"] = "acc"

        # fill the goto_table
        for i in range(len(self.active_closure)):
            tmp_goto = {}
            for c in self.nonterminal:
                tmp_goto[c] = self.transfer[i].get(c, -1)  # -1 means error
            self.goto_table.append(tmp_goto)


    def search_set_index(self, nonterminal):
        '''
        role: used to compute the index  first_set[A] => first_set[0]
        param: nonterminal
        return: compatible index
        '''
        return ord(nonterminal) - ord(Front_Char)

    def gen_order_grammar(self):
        '''
        fill the order_grammar
        generate the order_grammar_list like 0 S'->S  1 S->A
        '''
        self.order_grammar.append("1->" + self.start)
        for c in range(len(self.grammar_list)):
            if len(self.grammar_list[c]):
                for i in self.grammar_list[c]:
                    if self.nonterminal[c] == '':
                        continue
                    self.order_grammar.append(self.nonterminal[c] + "->" + i)

    def construct_parse_tree(self, sentence, parse_element_list, semantic_main):
        '''
        construct the parse_tree according to the sentence
        '''
        # each generate will clear the result of the latest
        self.node = []
        self.tree = ANTREE()
        tmp_cnt = 0

        state_order = [0]
        has_been_reduct = '#'
        input_sentence = sentence + '#'
        node_stack = []
        while True:
            tmp_op = self.action_table[state_order[-1]][input_sentence[0]]
            if tmp_op[0] == 's':
                # solve the analyse
                state_order.append(int(tmp_op[1:]))
                has_been_reduct += input_sentence[0]

                semantic_main.semantic_sendin(parse_element_list[len(sentence)-len(input_sentence)+1].get_value())

                input_sentence = input_sentence[1:]
                # solve the tree operation
                tmp_cnt += 1
                tmp_node = ANNODE(has_been_reduct[-1], tmp_cnt)
                node_stack.append(tmp_node)
            elif tmp_op[0] == 'r':
                # solve the analyse
                reduct_length = len(self.order_grammar[int(tmp_op[1:])]) - 3  # omit the begin and ->
                reduct_length -= ('e' in self.order_grammar[int(tmp_op[1:])])  # the real length of A->epsilon is zero
                reduct_nonterminal = self.order_grammar[int(tmp_op[1:])][0]

                is_semantic_right = semantic_main.semantic_reduct(self.order_grammar[int(tmp_op[1:])])
                if not is_semantic_right:
                    print("Semantic Error")
                    semantic_main.err_list[len(semantic_main.err_list)-1] += " position= " + \
                    str(parse_element_list[1-len(input_sentence)].get_position()[0]) + "," + \
                    str(parse_element_list[1-len(input_sentence)].get_position()[1])
                    return -2

                for i in range(reduct_length):
                    state_order.pop()
                state_order.append(self.goto_table[state_order[-1]][reduct_nonterminal])
                # solve the tree operation
                tmp_list_node = []   # in order to maintain the order with from the left to the right
                if reduct_length == 0:      # the condition like A-> epsilon
                    tmp_cnt += 1
                    tmp_epsilon = ANNODE('ε', tmp_cnt)
                    tmp_list_node.append(tmp_epsilon)
                else:
                    for i in range(reduct_length):
                        has_been_reduct = has_been_reduct[:-1]
                        tmp_list_node.append(node_stack.pop())
                tmp_cnt += 1
                tmp_node = ANNODE(reduct_nonterminal, tmp_cnt)
                node_stack.append(tmp_node)
                has_been_reduct += reduct_nonterminal
                for i in range(reduct_length + (reduct_length == 0)):
                    tmp_child = tmp_list_node.pop()
                    tmp_child.add_parent(tmp_node)
                    tmp_node.add_child(tmp_child)
            elif tmp_op == "acc":
                self.tree.update_root(node_stack.pop())
                self.tree.draw_tree_pic(self.tree.get_root())
                self.tree.tree_pic_show_save(is_show=False, is_save=True)
                return -1
            elif tmp_op == "error":
                return len(input_sentence) - 1

if __name__ == '__main__':
    test = SLR(GRAMMAR, '@')
    test.construct_parse_tree("td(td){d=(dcd);}")


