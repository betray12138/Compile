'''
    used to finish the Semantic Analyser process
'''
from claim import *

class function_table(object):
    def __init__(self):
        self.quad = 0
        self.param_list = []
        self.function_name = ''
        self.returntype = ''
        self.local_var = []

    def function_insert(self, function_name, quad, returntype):
        self.function_name = function_name
        self.quad = quad
        self.returntype = returntype

    def param_insert(self, param):
        self.param_list.append(param)

    def local_var_insert(self, variable):
        self.local_var.append(variable)

    def get_function_info(self):
        return self.function_name, self.param_list, self.quad, self.returntype

    def get_local_var(self):
        return self.local_var

class Semantic_element(object):
    def __init__(self):
        self.layer = 0
        self.size = 0
        self.quad = 0
        self.param_list = []
        self.nextlist = []
        self.truelist = []
        self.falselist = []
        self.name = None       # relop   use to record INTEGER_CONST

    def get_layer(self):
        return self.layer

    def get_size(self):
        return self.size

    def get_quad(self):
        return self.quad

    def get_param_list(self):
        return self.param_list

    def get_nextlist(self):
        return self.nextlist

    def get_truelist(self):
        return self.truelist

    def get_falselist(self):
        return self.falselist

    def get_name(self):
        return self.name

    def set_layer(self, layer):
        self.layer = layer

    def set_size(self, size):
        self.size = size

    def set_quad(self, quad):
        self.quad = quad

    def set_name(self, name):
        self.name = name

    def set_param_list(self, param_list):
        self.param_list = param_list

    def set_nextlist(self, nextlist):
        self.nextlist = nextlist

    def set_truelist(self, truelist):
        self.truelist = truelist

    def set_falselist(self, falselist):
        self.falselist = falselist

    def merge(self, *obj):
        '''
        merge all of the list in the obj
        '''
        for i in obj:
            self.nextlist += i
        self.nextlist = list(set(self.nextlist))   # remove the same elements

class Semantic_Process(object):
    def __init__(self):
        self.emit_code = []    # 100: =, a, b, T1   101: j,_,_,_
        self.func_table = []
        self.var_table = []
        self.nextquad = 100    # initialized setting 100
        self.newtmpcnt = 0
        self.process = []      # save the Semantic element
        self.err_list = []
        self.layer = 0         # record the global layer
        self.info_table = [function_table()]   # record all of the function and variable info

    def get_emit_code(self):
        return self.emit_code

    def get_err_list(self):
        return self.err_list

    def backpatch(self, list, quad):
        '''
        use quad to backpatch the specific list object
        '''
        for i in range(len(self.emit_code)):
            if int(self.emit_code[i][:self.emit_code[i].index(":")]) in list:
                self.emit_code[i] = self.emit_code[i][:-1]
                self.emit_code[i] += str(quad)   # delete the _ at the end

    def var_table_insert(self, name, type, layer, size):
        '''
        used to save the variability within the semantic process
        var_table: [name, type, layer, size]
        '''
        self.var_table.append([name, type, layer, size])

    def var_table_pop(self):
        '''
        used to pop the variability of the layer which finished just now
        '''
        while len(self.var_table) and self.var_table[-1][2] == self.layer+1:
            self.var_table.pop()

    def var_table_find(self, name, layer, symbol=0, size=None):
        '''
        find the variable within the table
        the first ret_value denotes whether can be found ; the second ret_value denotes whether exists in the same layer
        if need accurate match, must point the symbol=1 and input the size for variable
        point the symbol=2 and input the size for array
        '''
        def array_size_comp(size1, size2):
            if len(size1) != len(size2):
                return False
            for i in range(len(size1)):
                if size1[i] >= size2[i]:
                    return False
            return True

        for i in self.var_table[::-1]:
            if symbol == 0 and i[0] == name and i[2] == layer:
                return True, True
            if symbol == 0 and i[0] == name and i[2] < layer:
                return True, False
            if symbol == 1 and i[0] == name and i[2] == layer and i[3] == size:
                return True, True
            if symbol == 1 and i[0] == name and i[2] < layer and i[3] == size:
                return True, False
            if symbol == 2 and i[0] == name and i[2] == layer and array_size_comp(size, i[3]):
                return True, True
            if symbol == 2 and i[0] == name and i[2] < layer and array_size_comp(size, i[3]):
                return True, False
        return False, False


    def func_table_insert(self, name, type, param_list, quad):
        '''
        used to save the function within the semantic process
        func_table: [name,type,param_list,quad]
        '''
        self.func_table.append([name,type,param_list,quad])

    def func_table_find(self, name, symbol, param_list=None):
        '''
        use to find the searching function within the function table
        symbol: 0 using when define the function and find function according to the name
        symbol: 1 using when call the existed function
        return: is_find -- denotes whether can be found    quad -- denotes the inner statement index in the function
                type -- denotes the function ret type
        '''
        for i in self.func_table:
            if symbol == 1 and i[0] == name and len(i[2]) == len(param_list):
                return True, i[3], i[1]
            if symbol == 0 and i[0] == name:
                return True, i[3], i[1]
        return False, 100, None

    def emit(self, op, r1, r2, res):
        '''
        used to generate the final code : str
        # 100: =, a, b, T1   101: j,_,_,_
        '''
        self.emit_code.append(str(self.nextquad) + ":" + str(op) + ", " + str(r1) + ", " + str(r2) + ", " + str(res))
        self.nextquad += 1

    def newTemp(self):
        '''
        generate a new temp variable name
        '''
        self.newtmpcnt += 1
        return 'T' + str(self.newtmpcnt)

    def semantic_sendin(self, value):
        '''
        the terminal will in stack
        '''
        tmp = Semantic_element()
        tmp.set_name(value)
        tmp.set_layer(self.layer)
        self.process.append(tmp)

    def semantic_reduct(self, grammar):
        '''
        used the following semantic rules to face the reduct grammar
        '''
        if grammar == "@->^A":
            "<??????> ::= <?????????N> <?????????>                      backpatch(N.nextlist, find(main).quad)"
            _placeholderN = self.process[-2]
            # find the quad of function MAIN
            is_find, _quad, _type = self.func_table_find('main', 0)
            self.backpatch(_placeholderN.get_nextlist(), _quad)
        elif grammar == "A->B":
            "<?????????> ::= <??????>"
            _program = Semantic_element()
            _program.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_program)
        elif grammar == "A->BA":
            "<?????????> ::= <??????><?????????>"
            _program = Semantic_element()
            _program.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_program)
        elif grammar == "B->td;":
            "<??????> ::= INT ID ;             var_table.insert(ID.name, int, layer, 4)"
            _ID = self.process[-2]
            is_find, is_same_layer = self.var_table_find(_ID.get_name(), _ID.get_layer())
            if is_find and is_same_layer:
                self.err_list.append("Semantic Error: The variable " + _ID.get_name() + " redefinition")
                return False
            else:
                self.var_table_insert(_ID.get_name(), "int", _ID.get_layer(), 1)
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(Semantic_element())
            self.process[-1].set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
        elif grammar == "B->td]_E":
            "<??????> ::= INT ID <?????????M> <?????????A> <????????????> "
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(Semantic_element())
            self.process[-1].set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
        elif grammar == "B->tdF;":
            "<??????> ::= INT ID <????????????> ;    var_table.insert(ID.name, int, layer, 4 * <????????????>.size)"
            _ID = self.process[-3]
            _array = self.process[-2]
            is_find, is_same_layer = self.var_table_find(_ID.get_name(), _ID.get_layer())
            if is_find and is_same_layer:
                self.err_list.append("Semantic Error: The Array " + _ID.get_name() + " redefinition")
                return False
            else:
                self.var_table_insert(_ID.get_name(), "int", _ID.get_layer(), _array.get_size())
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(Semantic_element())
            self.process[-1].set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
        elif grammar == "B->vd]_E":
            "<??????> ::= VOID ID <?????????M> <?????????A> <????????????> "
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(Semantic_element())
            self.process[-1].set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
        elif grammar == "E->(G)`J":
            "<????????????> ::= ( <??????> ) <?????????S> <?????????>         <????????????>.param_list =  <??????>.param_list "
            _function_declare = Semantic_element()
            _formal_params = self.process[-4]
            _function_declare.set_param_list(_formal_params.get_param_list())
            _function_declare.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_function_declare)

            self.info_table.append(function_table())    # create a new node
        elif grammar == "F->zgk":
            "<????????????> ::= [ INTEGER_CONST ]              <????????????>.size = [INTEGER_CONST]"
            _array_declare = Semantic_element()
            _integer = self.process[-2]
            _array_declare.set_size([int(_integer.get_name())])
            _array_declare.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_array_declare)
        elif grammar == "F->zgkF":
            "<????????????1> ::= [ INTEGER_CONST ]<????????????2>    <????????????1>.size = [INTEGER_CONST] + <????????????2>.size"
            _array_declare1 = Semantic_element()
            _integer = self.process[-3]
            _array_declare2 = self.process[-1]
            _array_declare1.set_size([int(_integer.get_name())] + _array_declare2.get_size())
            _array_declare1.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_array_declare1)
        elif grammar == "G->H":
            "<??????> ::= <????????????>                         <??????>.param_list = <????????????>.param_list"
            _formal_params = Semantic_element()
            _params_list = self.process[-1]
            _formal_params.set_param_list(_params_list.get_param_list())
            _formal_params.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_formal_params)
        elif grammar == "G->v":
            "<??????> ::= VOID                             <??????>.param_list = []"
            _formal_params = Semantic_element()
            _formal_params.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_formal_params)
        elif grammar == "H->I":
            "<????????????> ::= <??????>                         <????????????>.param_list = [<??????>.name]"
            _params = self.process[-1]
            _params_list = Semantic_element()
            _params_list.set_param_list([_params.get_name()])
            _params_list.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_params_list)
        elif grammar == "H->I,H":
            "<????????????1> ::= <??????> , <????????????2>        <????????????1>.param_list = <????????????2>   <????????????1>.append(<??????>.name)"
            _params = self.process[-3]
            _params_list1 = Semantic_element()
            _params_list2 = self.process[-1]
            tmp_param_list = _params_list2.get_param_list()
            tmp_param_list.append(_params.get_name())
            _params_list1.set_param_list(tmp_param_list)
            _params_list1.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_params_list1)
        elif grammar == "I->td":
            "<??????> ::= INT ID                            var_table.insert(ID.name, int, layer, 4)"
            _ID = self.process[-1]
            self.var_table_insert(_ID.get_name(), "int", _ID.get_layer(), 1)
            self.info_table[-1].param_insert(_ID.get_name())
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            _params = Semantic_element()
            _params.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_params)
        elif grammar == "J->{KM}":
            "<?????????> ::= { <????????????> <?????????> }   <?????????>.nextlist = <?????????>.nextlist layer--   var_table.pop(layer+1)"
            _statement_block = Semantic_element()
            _statement_set = self.process[-2]
            _statement_block.set_nextlist(_statement_set.get_nextlist())
            _statement_block.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.layer -= 1
            self.var_table_pop()
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_statement_block)
        elif grammar == "K->e":
            "<????????????> ::= e"
            _inner_declare = Semantic_element()
            _inner_declare.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_inner_declare)
        elif grammar == "K->L;K":
            "<????????????> ::= <??????????????????> ;<????????????>"
            _inner_declare = Semantic_element()
            _inner_declare.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">")+1:])):
                self.process.pop()
            self.process.append(_inner_declare)
        elif grammar == "L->td":
            "<??????????????????> ::= INT ID                      var_table.insert(ID.name, int, layer, 4)"
            _ID = self.process[-1]
            is_find, is_same_layer = self.var_table_find(_ID.get_name(), _ID.get_layer())
            if is_find and is_same_layer:
                self.err_list.append("Semantic Error: The variable " + _ID.get_name() + " redefinition")
                return False
            else:
                self.var_table_insert(_ID.get_name(), "int", _ID.get_layer(), 1)
            self.info_table[-1].local_var_insert([_ID.get_name(), _ID.get_layer()])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            _inner_variable_declare = Semantic_element()
            _inner_variable_declare.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_inner_variable_declare)
        elif grammar == "M->N":
            "<?????????> ::= <??????>                            <?????????>.nextlist = <??????>.nextlist"
            _statement_set = Semantic_element()
            _statement = self.process[-1]
            _statement_set.set_nextlist(_statement.get_nextlist())
            _statement_set.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_statement_set)
        elif grammar == "M->N]M":
            "<?????????1> ::= <??????><?????????M><?????????2>  <?????????1>.nextlist = <?????????2>.nextlist backpatch(<??????>.nextlist, M.quad)"
            _statement_set1 = Semantic_element()
            _statement_set2 = self.process[-1]
            _statement = self.process[-3]
            _placeholderM = self.process[-2]
            self.backpatch(_statement.get_nextlist(), _placeholderM.get_quad())
            _statement_set1.set_nextlist(_statement_set2.get_nextlist())
            _statement_set1.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_statement_set1)
        elif grammar == "N->R" or grammar == "N->Q":
            "<??????> ::= <if??????>                           <??????>.nextlist = <if??????>.nextlist"
            "<??????> ::= <while??????>                        <??????>.nextlist = <while??????>.nextlist"
            _statement = Semantic_element()
            _if_while_statement = self.process[-1]
            _statement.set_nextlist(_if_while_statement.get_nextlist())
            _statement.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_statement)
        elif grammar == "N->O" or grammar == "N->P":
            "<??????> ::= <return??????>                       <??????>.nextlist = []"
            "<??????> ::= <????????????>                          <??????>.nextlist = []"
            _statement = Semantic_element()
            _statement.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_statement)
        elif grammar == "O->d=S;":
            "<????????????> ::= ID = <?????????>;                  emit(=,<?????????>.name,_,ID.name)"
            _expression = self.process[-2]
            _ID = self.process[-4]
            is_find, is_same_layer = self.var_table_find(_ID.get_name(), _ID.get_layer(), 1, 1)
            if not is_find:
                self.err_list.append("Semantic Error: The variable " + _ID.get_name() + " undefined")
                return False
            self.emit("=", _expression.get_name(), "_", _ID.get_name())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            _assign_statement = Semantic_element()
            _assign_statement.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_assign_statement)
        elif grammar == "O->Y=S;":
            "<????????????> ::= <??????> = <?????????>;               emit(=,<?????????>.name,_,<??????>.name)"
            _expression = self.process[-2]
            _array = self.process[-4]
            _array_name = _array.get_name()[:_array.get_name().index("[")]
            is_find, is_same_layer = self.var_table_find(_array_name, _array.get_layer(), 2, _array.get_size())
            if not is_find:
                self.err_list.append("Semantic Error: The Array " + _array.get_name() + " undefined")
                return False
            self.emit("=", _expression.get_name(), "_", _array.get_name())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            _assign_statement = Semantic_element()
            _assign_statement.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_assign_statement)
        elif grammar == "P->r;":
            "<return??????> ::= RETURN ;                    emit(return, _, _, _)      "
            if self.func_table[-1][1] == "INT":
                self.err_list.append("Semantic Error: The Function " + self.func_table[-1][0] + " lose return value")
                return False
            self.emit("ret", "_", "_", "_")
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            _return_statement = Semantic_element()
            _return_statement.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_return_statement)
        elif grammar == "P->rS;":
            "<return??????> ::= RETURN <?????????> ;            emit(return, <?????????>.name,_,_)"
            if self.func_table[-1][1] == "VOID":
                self.err_list.append("Semantic Error: The Function " + self.func_table[-1][0] + " can't exist return value")
                return False
            _expression = self.process[-2]
            self.emit("ret", _expression.get_name(), "_", "_")
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            _return_statement = Semantic_element()
            _return_statement.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_return_statement)
        elif grammar == "Q->w](S)]_J":
            "<while??????> ::= WHILE <?????????M1>( <?????????> ) <?????????M2> <?????????A> <?????????>"
            "backpatch(<?????????>.nextlist,M1.quad)  backpatch(<?????????>.truelist, M2.quad)"
            "<while??????>.nextlist = <?????????>.falselist  emit(j,_,_,M1.quad)"
            _while_statement = Semantic_element()
            _placeholderM1 = self.process[-7]
            _placeholderM2 = self.process[-3]
            _expression = self.process[-5]
            _statement_block = self.process[-1]
            self.backpatch(_statement_block.get_nextlist(), _placeholderM1.get_quad())
            self.backpatch(_expression.get_truelist(), _placeholderM2.get_quad())
            _while_statement.set_nextlist(_expression.get_falselist())
            _while_statement.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.emit("j", "_", "_", _placeholderM1.get_quad())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_while_statement)
        elif grammar == "R->i(S)]_J":
            "<if??????> ::= IF ( <?????????> ) <?????????M> <?????????A> <?????????>"
            "backpatch(<?????????>.truelist,M.quad) <if??????>.nextlist = merge(<?????????>.falselist, <?????????>.nextlist)"
            _if_statement = Semantic_element()
            _expression = self.process[-5]
            _placeholderM = self.process[-3]
            _statement_block = self.process[-1]
            self.backpatch(_expression.get_truelist(), _placeholderM.get_quad())
            _if_statement.merge(_expression.get_falselist(), _statement_block.get_nextlist())
            _if_statement.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_if_statement)
        elif grammar == "R->i(S)]_J^l]_J":
            "<if??????> ::= IF ( <?????????> ) <?????????M1> <?????????A> <?????????1> <?????????N> ELSE <?????????M2> <?????????A> <?????????2>"
            "backpatch(<?????????>.truelist,M1.quad)  backpatch(<?????????>.falselist,M2.quad)"
            "<if??????>.nextlist = merge(<?????????1>.nextlist, N.nextlist, <?????????2>.nextlist)"
            _if_statement = Semantic_element()
            _expression = self.process[-10]
            _placeholderM1 = self.process[-8]
            _statement_block1 = self.process[-6]
            _placeholderN = self.process[-5]
            _placeholderM2 = self.process[-3]
            _statement_block2 = self.process[-1]
            self.backpatch(_expression.get_truelist(), _placeholderM1.get_quad())
            self.backpatch(_expression.get_falselist(), _placeholderM2.get_quad())
            _if_statement.merge(_statement_block1.get_nextlist(), _placeholderN.get_nextlist(), _statement_block2.get_nextlist())
            _if_statement.set_name("MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]]")
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_if_statement)
        elif grammar == "S->T":
            "<?????????> ::= <???????????????>      !!! ???????????????relop?????????????????????"
            "<?????????>.name = <???????????????>.name <?????????>.truelist = [nextquad] <?????????>.falselist=[nextquad+1]"
            _expression = Semantic_element()
            _plus_expression = self.process[-1]
            _expression.set_name(_plus_expression.get_name())
            _expression.set_truelist([self.nextquad])
            _expression.set_falselist([self.nextquad+1])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_expression)
        elif grammar == "S->TxT" or grammar == "S->TyT" or grammar == "S->TfT" or grammar == "S->TcT" or grammar == "S->TbT" or grammar == "S->TnT":
            "<?????????> ::= <???????????????1> relop <???????????????2>         !!! ????????????relop????????? ?????????????????? ?????????????????????"
            "<?????????>.name = NULL  <?????????>.truelist = [nextquad]  <?????????>.falselist = [nextquad+1]"
            "emit(j relop, <???????????????1>.name, <???????????????2>.name???_)  emit(j,_,_,_)"
            _expression = Semantic_element()
            _plus_expression1 = self.process[-3]
            _plus_expression2 = self.process[-1]
            _relop = self.process[-2]
            _expression.set_truelist([self.nextquad])
            _expression.set_falselist([self.nextquad+1])
            self.emit("j"+_relop.get_name(), _plus_expression1.get_name(), _plus_expression2.get_name(), "_")
            self.emit("j", "_", "_", "_")
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_expression)
        elif grammar == "T->U":
            "<???????????????> ::= <???>                   <???????????????>.name = <???>.name"
            _plus_expression = Semantic_element()
            _item = self.process[-1]
            _plus_expression.set_name(_item.get_name())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_plus_expression)
        elif grammar == "T->U+T" or grammar == "T->U-T":
            "<???????????????1> ::= <???> + <???????????????2>  <???????????????1>.name = newTemp()  emit(+,<???>.name,<???????????????2>.name,<???????????????1>.name)"
            _plus_expression1 = Semantic_element()
            _plus_expression2 = self.process[-1]
            _item = self.process[-3]
            _op = self.process[-2]
            _plus_expression1.set_name(self.newTemp())
            self.emit(_op.get_name(), _item.get_name(), _plus_expression2.get_name(), _plus_expression1.get_name())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_plus_expression1)
        elif grammar == "U->V":
            "<???> ::= <??????>                        <???>.name = <??????>.name"
            _item = Semantic_element()
            _factor = self.process[-1]
            _item.set_name(_factor.get_name())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_item)
        elif grammar == "U->V*U" or grammar == "U->V/U":
            "<???1> ::= <??????> * <???2>          <???1>.name = newTemp()   emit(*,<??????>.name,<???2>.name,<???1>.name)"
            _item1 = Semantic_element()
            _factor = self.process[-3]
            _op = self.process[-2]
            _item2 = self.process[-1]
            _item1.set_name(self.newTemp())
            self.emit(_op.get_name(), _factor.get_name(), _item2.get_name(), _item1.get_name())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_item1)
        elif grammar == "V->g":
            "<??????> ::= INTEGER_CONST               <??????>.name = INTEGER_CONST"
            _factor = Semantic_element()
            _integer = self.process[-1]
            _factor.set_name(str(int(_integer.get_name())))
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_factor)
        elif grammar == "V->(S)":
            "<??????> ::= ( <?????????> )                  <??????>.name = <?????????>.name"
            _factor = Semantic_element()
            _expression = self.process[-2]
            _factor.set_name(_expression.get_name())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_factor)
        elif grammar == "V->d":
            "<??????> ::= ID                           <??????>.name = ID.name"
            _factor = Semantic_element()
            _ID = self.process[-1]
            is_find, is_same_layer = self.var_table_find(_ID.get_name(), _ID.get_layer(), 1, 1)
            if not is_find:
                self.err_list.append("Semantic Error: The Variable " + _ID.get_name() + " undefined")
                return False
            _factor.set_name(_ID.get_name())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_factor)
        elif grammar == "V->d(Z)":
            "<??????> ::= ID ( <??????> )  push <??????>.param_list   emit(jal,func_table.find(ID.name).enterPoint)"
            " if(f.returnType == int) <??????>.name = newTemp()  emit(=,ID.name(),_,<??????>.name)"
            _factor = Semantic_element()
            _ID = self.process[-4]
            _actual_params = self.process[-2]
            is_find, _quad, _type = self.func_table_find(_ID.get_name(), 1, _actual_params.get_param_list())
            if not is_find:
                self.err_list.append("Semantic Error: The Function " + _ID.get_name() + " undefined or params Error")
                return False
            for i in _actual_params.get_param_list()[::-1]:
                self.emit("param", i, "_", "_")
            self.emit("push", "_", "_", "sp")
            self.emit("jal", "_", "_", str(_quad))
            self.emit("pop", "_", "_", "sp")
            if _type == "INT":
                _factor.set_name(self.newTemp())
                self.emit("=", _ID.get_name() + "()", "_", _factor.get_name())
            else:
                self.err_list.append("Semantic Error: The Function " + _ID.get_name() + " return type is not fit")
                return False
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_factor)
        elif grammar == "V->Y":
            "<??????> ::= <??????>                          <??????>.name = <??????>.name"
            _factor = Semantic_element()
            _array = self.process[-1]
            is_find, is_same_layer = self.var_table_find(_array.get_name()[:_array.get_name().index("[")],
                                                         _array.get_layer(), 2, _array.get_size())
            if not is_find:
                self.err_list.append("Semantic Error: The Array " + _array.get_name() + " undefined")
                return False
            _factor.set_name(_array.get_name())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_factor)
        elif grammar == "Y->dzSk":
            "<??????> ::= ID [ <?????????> ]    <??????>.layer  <??????>.name = ID.name[<?????????>.name]   <??????>.size = [int(<?????????>.name)]"
            _array = Semantic_element()
            _ID = self.process[-4]
            _expression = self.process[-2]
            _array.set_name(_ID.get_name() + "[" + _expression.get_name() + ']')
            _array.set_size([int(_expression.get_name())])
            _array.set_layer(_ID.get_layer())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_array)
        elif grammar == "Y->YzSk":
            "<??????1> ::= <??????2> [ <?????????> ]    <??????1>.name = <??????2>.name + [<?????????>.name] "
            "<??????1>.size = <??????2>.size +[int(<?????????>.name)]  <??????1>.layer = <??????2>.layer"
            _array1 = Semantic_element()
            _array2 = self.process[-4]
            _expression = self.process[-2]
            _array1.set_name(_array2.get_name() + "[" + _expression.get_name() + ']')
            _array1.set_size(_array2.get_size() + [int(_expression.get_name())])
            _array1.set_layer(_array2.get_layer())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_array1)
        elif grammar == "Z->e":
            "<??????> ::= e                              <??????>.param_list = []"
            _actual_params = Semantic_element()
            self.process.append(_actual_params)
        elif grammar == "Z->[":
            "<??????> ::= <????????????>                       <??????>.param_list = <????????????>.param_list"
            _actual_params = Semantic_element()
            _actual_param_list = self.process[-1]
            _actual_params.set_param_list(_actual_param_list.get_param_list())
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_actual_params)
        elif grammar == "[->S":
            "<????????????> ::= <?????????>                     <????????????>.param_list = [<?????????>.name]"
            _expression = self.process[-1]
            _actual_params_list = Semantic_element()
            _actual_params_list.set_param_list([_expression.get_name()])
            _actual_params_list.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_actual_params_list)
        elif grammar == "[->S,[":
            "<????????????1> ::= <?????????> , <????????????2> <????????????1>.param_list = <????????????2>.param_list <????????????1>.append(<?????????>.name)"
            _actual_params_list1 = Semantic_element()
            _actual_params_list2 = self.process[-1]
            _expression = self.process[-3]
            tmp_params_list = _actual_params_list2.get_param_list()
            tmp_params_list.append(_expression.get_name())
            _actual_params_list1.set_param_list(tmp_params_list)
            _actual_params_list1.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            for i in range(len(grammar[grammar.index(">") + 1:])):
                self.process.pop()
            self.process.append(_actual_params_list1)
        elif grammar == "]->e":
            "<?????????M> ::= e                            M.quad = nextquad"
            _placeholderM = Semantic_element()
            _placeholderM.set_quad(self.nextquad)
            _placeholderM.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_placeholderM)
        elif grammar == "^->e":
            "<?????????N> ::= e                            N.nextlist = [nextquad]  emit(j,_,_,_)"
            _placeholderN = Semantic_element()
            _placeholderN.set_nextlist([self.nextquad])
            self.emit("j", "_", "_", "_")
            _placeholderN.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_placeholderN)
        elif grammar == "_->e":
            "<?????????A> ::= e                            layer++"
            _placeholderA = Semantic_element()
            self.layer += 1
            _placeholderA.set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
            self.process.append(_placeholderA)
        elif grammar == "`->e":
            "<????????????> ::= ( <??????> ) <?????????S> <?????????>                    E->(G)`J"
            "<??????> ::= INT ID <?????????M> <?????????A> <????????????>"
            "<??????> ::= VOID ID <?????????M> <?????????A> <????????????>"
            _ID = self.process[-6]
            _return_type = self.process[-7]
            _formal_params = self.process[-2]
            _placeholderM = self.process[-5]
            is_find, _quad, _type = self.func_table_find(_ID.get_name(), 0)
            if is_find:
                self.err_list.append("Semantic Error: The Function " + _ID.get_name() + " redefinition")
                return False
            self.func_table_insert(_ID.get_name(), _return_type.get_name(), _formal_params.get_param_list(), _placeholderM.get_quad())
            self.info_table[-1].function_insert(_ID.get_name(), _placeholderM.get_quad(), _return_type.get_name())
            self.process.append(Semantic_element())
            self.process[-1].set_name(MAP_REVERSE_NONTERMINAL_EN_LIST[grammar[0]])
        return True












