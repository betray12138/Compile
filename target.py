'''
    use to generate the target code
'''
'''
$zero 默认始终为0
$at   预留寄存器
$v0-v1 存储返回值  函数使用$v0存储返回值
$a0-a3 存储函数形参内容
$t0-t9 存储临时使用变量
$s0-s7 存储函数局部变量
$k0-k1 存放main函数相关局部变量
$gp $fp 存放全局变量首地址
$ra   函数返回地址
'''

from Semantic_analyse import *

class TARGET(object):
    def __init__(self, emit_code, var_table, info_table):
        self.emit_code = emit_code
        self._global = var_table
        self.reg_memory = {}
        self.basic_block_index = []
        self.basic_block = []
        self.info_table = []
        self.object_code = []
        self.function_entry = {}
        self.rvalue = {'$t0': None, '$t1': None, '$t2': None, '$t3': None, '$t4': None,
                       '$t5': None, '$t6': None, '$t7': None, '$t8': None, '$t9': None}
        self.avalue = {}
        self.gen_basic_block_index()
        self.gen_basic_block()
        self.info_search()
        self.fill_reg_memory(info_table)
        self.fill_function_entry(info_table)
        self.generate_object_code()

    def get_object_code(self):
        return self.object_code

    def fill_function_entry(self, info_table):
        '''
        find the entry of every function, register in the function_entry like main:122
        '''
        for i in range(len(info_table)-1):
            _name, _params, _quad, _rettype = info_table[i].get_function_info()
            self.function_entry[_name] = _quad

    def fill_reg_memory(self, info_table):
        '''
        set the global variable first-address and generate the .data
        set the register of formal variable and local variable within every function
        '''
        ''' first solve the condition of global variable'''
        global_var_add = ['$gp', '$fp']
        tmp_global = {}
        self.object_code.append('.data')
        for i in range(len(self._global)):
            tmp_global[self._global[i][0]] = global_var_add[i]
            _space = 1
            if self._global[i][3] == 1:
                _space = 1
            else:
                for j in self._global[i][3]:
                    _space *= j
            self.object_code.append(self._global[i][0] + ":.space " + str(_space*4))
        self.reg_memory["global"] = tmp_global

        ''' second solve the condition within every function'''
        for i in range(len(info_table)-1):
            tmp = {}
            ''' formal params'''
            _name, _params, _quad, _rettype = info_table[i].get_function_info()
            for j in range(len(_params)):
                tmp[_params[j]] = '$a' + str(j)
            ''' local variable'''
            _local_var = info_table[i].get_local_var()
            for j in range(len(_local_var)):
                tmp[_local_var[j][0]] = '$s' + str(j)
            self.reg_memory[_name] = tmp

    def info_search(self):
        '''
        search all of the variables within every basic_block and fill the info_table
        '''
        for block in self.basic_block:
            info_link = {}     # update every block
            for statement in block:
                '''  the comma divided statement like 100:j   _   _   102'''
                segment = statement.split(",")
                for i in range(len(segment)):
                    segment[i] = segment[i].strip(" ")
                colon_place = segment[0].index(":")
                if segment[0][colon_place + 1:] == "=":
                    ''' = has only one operation'''
                    if segment[1].isdigit():
                        info_link[segment[1]] = "^,^"
                    elif segment[1][-2:] == '()':
                        ''' assign process for a function'''
                        info_link[segment[1]] = "^,^"
                    else:
                        info_link[segment[1]] = "^,y"
                    info_link[segment[3]] = "^,y"
                elif segment[0][colon_place+1:] in ["+", "-", "*", "/"]:
                    ''' has two operations'''
                    info_link[segment[1]] = "^," + ('^' if segment[1].isdigit() else 'y')
                    info_link[segment[2]] = "^," + ('^' if segment[2].isdigit() else 'y')
                    info_link[segment[3]] = "^,y"
                elif segment[0][colon_place+1:] in ['j>', 'j<', 'j>=', 'j<=', 'j==', 'j!=']:
                    ''' has two operations'''
                    info_link[segment[1]] = "^," + ('^' if segment[1].isdigit() else 'y')
                    info_link[segment[2]] = "^," + ('^' if segment[2].isdigit() else 'y')

            block_length = len(block)
            tmp_block = {}
            for i in range(block_length):
                ''' the form of tmp_list like [left value, op1, op2]'''
                tmp_list = []
                '''  the comma divided statement like 100:j   _   _   102'''
                segment = block[block_length-1-i].split(",")
                for j in range(len(segment)):
                    segment[j] = segment[j].strip(" ")
                colon_place = segment[0].index(":")
                if segment[0][colon_place+1:] == "=":
                    tmp_list.append(info_link.get(segment[3], '^,^'))  # left value
                    tmp_list.append(info_link.get(segment[1], '^,^'))  # op1
                    tmp_list.append("^,^")
                    info_link[segment[3]] = '^,^'
                    info_link[segment[1]] = str(block_length - 1 - i) + ",y"
                elif segment[0][colon_place+1:] in ["+", "-", "*", "/"]:
                    tmp_list.append(info_link.get(segment[3], '^,^'))    # left value
                    tmp_list.append(info_link.get(segment[1], '^,^'))    # op1
                    tmp_list.append(info_link.get(segment[2], '^,^'))    # op2
                    info_link[segment[3]] = '^,^'
                    info_link[segment[1]] = str(block_length - 1 - i) + ",y"
                    info_link[segment[2]] = str(block_length - 1 - i) + ",y"
                elif segment[0][colon_place+1:] in ['j>', 'j<', 'j>=', 'j<=', 'j==', 'j!=']:
                    tmp_list.append('^,^')  # jump_addr
                    tmp_list.append(info_link.get(segment[1], '^,^'))  # op1
                    tmp_list.append(info_link.get(segment[2], '^,^'))  # op2
                    info_link[segment[1]] = str(block_length - 1 - i) + ",y"
                    info_link[segment[2]] = str(block_length - 1 - i) + ",y"
                tmp_block[block_length-1-i] = tmp_list
            self.info_table.append(tmp_block)

    def gen_basic_block_index(self):
        '''
        fill the basic_block_index
        '''
        self.basic_block_index.append(100)
        for i in range(len(self.emit_code)):
            colon_place = self.emit_code[i].index(":")
            if self.emit_code[i][colon_place+1] == "j":
                tmp_array = self.emit_code[i].split(",")
                self.basic_block_index.append(int(tmp_array[3]))
                if i+1 < len(self.emit_code):
                    _colon = self.emit_code[i+1].index(":")
                    self.basic_block_index.append(int(self.emit_code[i+1][:_colon]))
            elif self.emit_code[i][colon_place+1:colon_place+4] == 'ret':
                if i+1 < len(self.emit_code):
                    _colon = self.emit_code[i+1].index(":")
                    self.basic_block_index.append(int(self.emit_code[i+1][:_colon]))
        self.basic_block_index = list(set(self.basic_block_index))
        self.basic_block_index.sort()

    def gen_basic_block(self):
        '''
        fill the basic_block
        '''
        pointer = 1
        cur = 0
        while True:
            tmp_block = []
            while True:
                _colon_pos = self.emit_code[cur].index(":")
                if int(self.emit_code[cur][:_colon_pos]) < self.basic_block_index[pointer]:
                    tmp_block.append(self.emit_code[cur])
                else:
                    break
                cur += 1
            self.basic_block.append(tmp_block)
            pointer += 1
            if pointer == len(self.basic_block_index):
                break
        tmp_block = []
        _last_index = int(self.emit_code[-1][:self.emit_code[-1].index(":")])
        _cur_index = int(self.emit_code[cur][:self.emit_code[-1].index(":")])
        while _cur_index <= _last_index:
            tmp_block.append(self.emit_code[cur])
            _cur_index += 1
            cur += 1
        self.basic_block.append(tmp_block)

    def register_designate(self, var_name, func_name, code_index, op):
        '''
        designate a proper register for the var
        op : left_value -- 0 ,  op1 -- 1, op2 -- 2
        return the chosen register
        '''
        code_index = int(code_index)
        if var_name[-2:] == '()':
            ''' obtain the function return value'''
            return '$v0'
        param_or_local = self.reg_memory[func_name].get(var_name, -1)
        if param_or_local != -1:
            return param_or_local
        tmp_var = self.avalue.get(var_name, -1)
        if tmp_var == -1:
            _reg = self.register_allocate(var_name, func_name)
            if var_name in self.reg_memory["global"]:
                self.object_code.append("lw " + _reg + ", 0(" + self.reg_memory["global"][var_name] + ")")
            _lar_pos = var_name.find("[")
            if _lar_pos != -1 and var_name[:_lar_pos] in self.reg_memory["global"]:
                _bias = self.obtain_array_bias(var_name)
                self.object_code.append("lw " + _reg + ", " + str(_bias*4) + "(" + self.reg_memory["global"][var_name[:_lar_pos]] + ")")
            return _reg
        else:
            return tmp_var
            _end = True
            _basic_cnt = 0
            _basic_inner_index = 0
            for i in range(1, len(self.basic_block_index)):
                if self.basic_block_index[i] <= code_index:
                    _basic_cnt += 1
                    continue
                else:
                    _end = False
                    _basic_inner_index = code_index - self.basic_block_index[_basic_cnt]
                    break
            if _end:
                _basic_cnt = -1
                _basic_inner_index = code_index - self.basic_block_index[_basic_cnt]

            op_dict = {"left_value": 0, "op1": 1, "op2": 2}
            if self.info_table[_basic_cnt][_basic_inner_index][op_dict[op]][-1] == 'y':
                ''' will be used later'''
                return self.register_allocate(var_name, func_name)
            else:
                ''' will not be used later'''
                ''' can not be a formal param or a local variable'''
                return tmp_var

    def register_allocate(self, var_name, func_name):
        '''
        allocate a new tmp_register for the var
        '''
        if func_name != "main":
            for i in self.rvalue:
                if self.rvalue[i] is None:
                    self.rvalue[i] = var_name
                    self.avalue[var_name] = i
                    return i
        else:
            for i in range(len(self.rvalue)):
                if self.rvalue['$t' + str(9-i)] is None:
                    self.rvalue['$t' + str(9 - i)] = var_name
                    self.avalue[var_name] = '$t' + str(9-i)
                    return '$t' + str(9-i)
        print("all of the registers have been allocated, must release")
        for i in self.rvalue:
            if self.rvalue[i].isdigit():
                self.rvalue[i] = var_name
                self.avalue[var_name] = i
                return i

    def obtain_array_bias(self, var_name):
        '''
        return the array variable bias
        '''
        _bias = 0
        tmp_list = []
        _lar_pos = var_name.find("[")
        for i in range(_lar_pos+1, len(var_name)):
            if var_name[i].isdigit():
                tmp_list.append(int(var_name[i]))
        for i in self._global:
            if i[0] == var_name[:_lar_pos]:
                for j in range(len(i[3]) - 1):
                    _bias += tmp_list[j] * i[3][j + 1]
                _bias += tmp_list[-1]
        return _bias

    def generate_object_code(self):
        '''
        finish the process of generating object code
        '''
        self.object_code.append(".text")
        for i in self.reg_memory['global']:
            self.object_code.append("la " + self.reg_memory['global'][i] + ", " + i)
        self.object_code.append("add $sp, $0, 0x10010100")
        self.object_code.append("j main")

        _param_cnt = 0  # record the number of push params

        for i in range(1, len(self.emit_code)):
            ''' emit code: 100:j, _, _, 121'''
            segment = self.emit_code[i].split(",")
            for j in range(len(segment)):
                segment[j] = segment[j].strip(" ")

            colon_pos = segment[0].index(":")
            ''' append the function name'''
            for j in self.function_entry:
                if int(segment[0][:colon_pos]) == self.function_entry[j]:
                    self.object_code.append(j + ":")

            for j in self.basic_block_index:
                if int(segment[0][:colon_pos]) == j:
                    self.object_code.append("label" + str(j) + ":")

            ''' find the current belonging function name'''

            _index = segment[0][:colon_pos]
            _func_name = None
            for j in self.function_entry:
                if self.function_entry[j] <= int(_index):
                    _func_name = j
            _func_space = 4
            if segment[0][colon_pos+1:] == "=":
                is_set = False
                ''' op1 is global variable'''
                _lar_pos = segment[1].find("[")
                if segment[1] in self.reg_memory['global'] and segment[1] not in self.reg_memory[_func_name]:
                    _reg = self.register_designate(segment[3], _func_name, _index, "left_value")
                    self.object_code.append("lw " + _reg + ", 0(" + self.reg_memory['global'][segment[1]] + ")")
                    is_set = True
                elif _lar_pos != -1 and segment[1][:_lar_pos] in self.reg_memory['global']:
                    _reg = self.register_designate(segment[3], _func_name, _index, "left_value")
                    _bias = self.obtain_array_bias(segment[1])
                    self.object_code.append("lw " + _reg + ", " + str(_bias*4) + "(" + self.reg_memory["global"][segment[1][:_lar_pos]] + ")")
                    is_set = True

                ''' left_value is global variable'''
                _lar_pos = segment[3].find("[")
                if segment[3] in self.reg_memory['global'] and segment[3] not in self.reg_memory[_func_name]:
                    _reg = self.register_designate(segment[1], _func_name, _index, "op1")
                    if segment[1].isdigit():
                        self.object_code.append("add " + _reg + ", $0, " + segment[1])
                    self.object_code.append("sw " + _reg + ", 0(" + self.reg_memory['global'][segment[3]] + ")")
                    is_set = True
                elif _lar_pos != -1 and segment[3][:_lar_pos] in self.reg_memory['global']:
                    _reg = self.register_designate(segment[1], _func_name, _index, "op1")
                    if segment[1].isdigit():
                        self.object_code.append("add " + _reg + ", $0, " + segment[1])
                    _bias = self.obtain_array_bias(segment[3])
                    self.object_code.append("sw " + _reg + ", " + str(_bias*4) + "(" + self.reg_memory["global"][segment[3][:_lar_pos]] + ")")
                    is_set = True

                ''' normal condition'''
                if not is_set:
                    _reg1 = self.register_designate(segment[1], _func_name, _index, "op1")
                    _reg2 = self.register_designate(segment[3], _func_name, _index, "left_value")
                    if segment[1].isdigit():
                        self.object_code.append("add " + _reg1 + ", $0, " + segment[1])
                    if segment[2].isdigit():
                        self.object_code.append("add " + _reg2 + ", $0, " + segment[2])
                    self.object_code.append("add " + _reg2 + ", $zero, " + _reg1)

            elif segment[0][colon_pos+1:] == "jal":
                for j in self.function_entry:
                    if self.function_entry[j] == int(segment[3]):
                        self.object_code.append("jal " + j)
                _param_cnt = 0

            elif segment[0][colon_pos+1:] in ["+", "-", "*", "/"]:
                op_dict = {"+": "add", "-": 'sub', "*": 'mul', '/': 'div'}
                _reg1 = self.register_designate(segment[1], _func_name, _index, "op1")
                _reg2 = self.register_designate(segment[2], _func_name, _index, "op2")
                if segment[1].isdigit():
                    self.object_code.append("add " + _reg1 + ", $0, " + segment[1])
                if segment[2].isdigit():
                    self.object_code.append("add " + _reg2 + ", $0, " + segment[2])
                _reg3 = self.register_designate(segment[3], _func_name, _index, "left_value")
                self.object_code.append(op_dict[segment[0][colon_pos+1:]] + " " + _reg3 + ", " + _reg1 + ", " + _reg2)

            elif segment[0][colon_pos+1:] == "param":
                _reg = self.register_designate(segment[1],  _func_name, _index, "op1")
                if segment[1].isdigit():
                    self.object_code.append("add " + _reg + ", $0, " + segment[1])
                self.object_code.append("add $a" + str(_param_cnt) + ", $0, " + _reg)
                _param_cnt += 1

            elif segment[0][colon_pos+1:] == "ret":
                if segment[1] != "_":
                    _reg = self.register_designate(segment[1], _func_name, _index, "op1")
                    self.object_code.append("add $v0, $0, " + _reg)
                self.avalue.clear()
                for j in self.rvalue:
                    self.rvalue[j] = None
                self.object_code.append("jr $ra")

            elif segment[0][colon_pos+1:] in ["j>", "j<", "j==", "j>=", "j<=", "j!="]:
                jump_dict = {"j>": "bgt", "j<": "blt", "j==": "beq", "j>=": "bge", "j<=": "ble", "j!=": "bne"}
                _reg1 = self.register_designate(segment[1], _func_name, _index, "op1")
                _reg2 = self.register_designate(segment[2], _func_name, _index, "op2")
                if segment[1].isdigit():
                    self.object_code.append("add " + _reg1 + ", $0, " + segment[1])
                if segment[2].isdigit():
                    self.object_code.append("add " + _reg2 + ", $0, " + segment[2])
                self.object_code.append(jump_dict[segment[0][colon_pos+1:]] + " " + _reg1 + ", " + _reg2 + ", label" + segment[3])

            elif segment[0][colon_pos+1:] == 'j':
                self.object_code.append("j label" + segment[3])

            elif segment[0][colon_pos+1:] == 'push':
                self.object_code.append("sub $sp, $sp, " + str(_func_space))
                self.object_code.append("sw $ra, 0($sp)")

            elif segment[0][colon_pos+1:] == "pop":
                self.object_code.append("lw $ra, 0($sp)")
                self.object_code.append("add $sp, $sp, " + str(_func_space))

        ''' emit the last jr code'''
        self.object_code.pop()


if __name__ == "__main__":
    test = ['100:j, _, _, 122', '101:=, 0, _, i', '102:+, y, z, T1', '103:j>, x, T1, 105', '104:j, _, _, 110', '105:*, y, z, T2', '106:+, T2, 1, T3', '107:+, x, T3, T4', '108:=, T4, _, j', '109:j, _, _, 111', '110:=, x, _, j', '111:j<=, i, 100, 113', '112:j, _, _, 117', '113:*, j, 2, T5', '114:+, i, T5, T6', '115:=, T6, _, i', '116:j, _, _, 111', '117:ret, i, _, _', '118:+, c, 2, T7', '119:=, T7, _, c', '120:*, c, 2, T8', '121:ret, T8, _, _', '122:=, 3, _, b[0][0]', '123:+, b[0][0], 1, T9', '124:=, T9, _, b[0][1]', '125:/, b[0][0], 3, T10', '126:=, T10, _, b[1][0]', '127:param, b[1][0], _, _', '128:jal, _, _, 118', '129:=, demo(), _, T11', '130:param, b[0][0], _, _', '131:param, b[0][1], _, _', '132:param, T11, _, _', '133:jal, _, _, 101', '134:=, program(), _, T12', '135:=, T12, _, b[1][1]', '136:ret, _, _, _']
    var_table = [['b', 'int', 0, [2, 2]]]
    function_ = [function_table(), function_table(), function_table(), function_table()]
    function_[0].function_insert('program', 101, 'INT')
    function_[0].param_insert("x")
    function_[0].param_insert("y")
    function_[0].param_insert("z")
    function_[0].local_var_insert(["i", 1])
    function_[0].local_var_insert(["j", 1])
    function_[1].function_insert('demo', 118, 'INT')
    function_[1].param_insert('c')
    function_[2].function_insert('main', 122, 'VOID')
    TARGET(test, var_table, function_)