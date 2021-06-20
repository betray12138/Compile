

''' used to compute the FIRST & FOLLOW set of the grammar'''
from claim import *

class FIRST_FOLLOW(object):
    def __init__(self, grammar_list, start):
        '''
        role: constructive function
        !!!assume that only the follow set of the start char may have one element
        parameter: grammar_list  input all of the grammar
                   start         the start character of the grammar
        variable: nonterminal   all of the nonterminal 'A'-'Z'
                  terminal      all of the terminal including epsilon
                  first_set     the FIRST about all of the nonterminal including epsilon
                  follow_set    the FOLLOW about all of the nonterminal including #
                  grammar_list  input all of the grammar by pre-process
        default terminal are lower-case
        '''
        self.start = start
        self.nonterminal = []
        self.terminal = TERMINAL_LIST
        self.first_set = [set() for i in range(Array_Num)]
        self.follow_set = [set() for i in range(Array_Num)]
        self.grammar_list = [[] for i in range(Array_Num)]
        self.pre_process(grammar_list)
        self.compute_first_set()
        self.compute_follow_set()

    def compute_follow_set(self):
        '''
        role: used to compute the follow_set about all of the nonterminal
        '''
        for s in self.nonterminal:
            self.recur_compute_follow_set(s)
        self.compute_follow_ends(self.start)


    def compute_follow_ends(self, nonterminal):
        '''
        role: used to compute the follow_set about all of the nonterminal appending #
        param: nonterminal
        '''
        self.follow_set[self.search_set_index(nonterminal)].add('#')
        for li in self.grammar_list[self.search_set_index(nonterminal)]:
            for i in range(len(li)-1, -1, -1):
                if li[i] in self.terminal:
                    break
                elif li[i] in self.nonterminal and li[i] != nonterminal:
                    self.compute_follow_ends(li[i])
                elif li[i] == 'e': #epsilon
                    continue
                if 'e' not in self.first_set[self.search_set_index(li[i])]:
                    break



    def recur_compute_follow_set(self, nonterminal):
        '''
        role: assist to compute follow set with recursion
        param: search the follow set of nonterminal
        return: the follow set of nonterminal
        '''
        if len(self.follow_set[self.search_set_index(nonterminal)]):        # memory search
            return self.follow_set[self.search_set_index(nonterminal)]
        for el in self.nonterminal:
            for li in self.grammar_list[self.search_set_index(el)]:
                for st in range(len(li)):                                   # scan the generation formula
                    if li[st] == nonterminal and st == len(li)-1 and li[st] != el:    # non-terminal and last
                        self.follow_set[self.search_set_index(li[st])] = self.follow_set[
                            self.search_set_index(li[st])].union(self.recur_compute_follow_set(el))
                    elif li[st] == nonterminal and st < len(li)-1:
                        for ind in range(st+1, len(li)):
                            if li[ind] in self.terminal:
                                self.follow_set[self.search_set_index(li[st])].add(li[ind])
                                break
                            self.follow_set[self.search_set_index(li[st])] = self.follow_set[
                                self.search_set_index(li[st])].union(self.first_set[self.search_set_index(li[ind])])
                            self.follow_set[self.search_set_index(li[st])] -= {'e'}
                            if ind == len(li)-1 and 'e' in self.first_set[self.search_set_index(li[ind])] and li[st] != el:
                                self.follow_set[self.search_set_index(li[st])] = self.follow_set[
                                    self.search_set_index(li[st])].union(self.recur_compute_follow_set(el))
                                break
                            if 'e' not in self.first_set[self.search_set_index(li[ind])]:
                                break

        return self.follow_set[self.search_set_index(nonterminal)]


    def compute_first_set(self):
        '''
        default e is epsilon
        role: used to compute the first_set about all of the nonterminal
        '''
        for s in self.nonterminal:
            stack = []
            self.first_set[self.search_set_index(s)] = self.first_set[
                self.search_set_index(s)].union(self.recur_compute_first_set(s, stack))



    def recur_compute_first_set(self, nonterminal, stack):
        '''
        role: assist to compute first set with recursion
        param: search the first set of nonterminal
        return: the first set of nonterminal
        '''
        if nonterminal in stack:
            return set()
        else:
            stack.append(nonterminal)

        for li in self.grammar_list[self.search_set_index(nonterminal)]:
            for st in range(len(li)):
                if li[st] in self.terminal:
                    self.first_set[self.search_set_index(nonterminal)].add(li[st])
                    break
                elif li[st] in self.nonterminal:
                    self.first_set[self.search_set_index(nonterminal)] = self.first_set[
                        self.search_set_index(nonterminal)].union(self.recur_compute_first_set(li[st], stack)-{'e'})
                    if 'e' not in self.first_set[self.search_set_index(li[st])]:
                        break
                if st == len(li)-1:
                    self.first_set[self.search_set_index(nonterminal)].add('e')
        stack.pop()
        return self.first_set[self.search_set_index(nonterminal)]

    def search_set_index(self, nonterminal):
        '''
        role: used to compute the index  first_set[A] => first_set[0]
        param: nonterminal
        return: compatible index
        '''
        return ord(nonterminal) - ord(Front_Char)


    def pre_process(self, grammar_list):
        '''
        role: pre-process the input grammar list  A->aA|bB => A->aA A->aB default sep '|'
        param: grammar_list  type(list)
        return: the grammar_list has been done
        '''
        for li in grammar_list:
            tmp_nonterminal = li[0]
            self.nonterminal.append(tmp_nonterminal)

            tmp_sep_list = li.split('>')[1].split('|')
            for tmp_li in tmp_sep_list:
                self.grammar_list[self.search_set_index(tmp_nonterminal)].append(tmp_li)
        return


if __name__ == '__main__':
    test = FIRST_FOLLOW(['M->N|N]M', ']->e', 'N->i|r|w'], 'M')
    '''print(test.grammar_list[test.search_set_index('T')])
    print(test.nonterminal)
    print(test.first_set[test.search_set_index('T')])
    print(test.first_set[test.search_set_index('S')])
    print(test.first_set[test.search_set_index('A')])'''
    print(test.first_set)
    print(test.follow_set)