
from Semantic_analyse import *
from SLR import *
'''
    used to finish the operation of Parser Process
'''

class Parse_Element(object):
    def __init__(self):
        '''
        symbol: INT -> t
        position: [row,col]
        value: c
        '''
        self.symbol = None
        self.position = None
        self.value = None

    def update_element(self, info):
        '''
        info: the str like Token(TokenType.INT& 'INT'& position=1:1)
        update self.symbol self.position self.value
        '''
        # tmp_update[0] -- Token(TokenType.INT  tmp_update[1] --  'INT'  tmp_update[2] --  position=1:1)
        tmp_update = info.split(" ")
        # solve the self.symbol
        dot_pos = tmp_update[0].index(".")
        self.symbol = MAP_TERMINAL_LIST[tmp_update[0][dot_pos+1:]]

        # solve the self.value
        try:
            quota_pos = tmp_update[1].index("'")
        except ValueError:
            self.value = int(tmp_update[1])  # solve the condition like Token(TokenType.INTEGER_CONST, 0, position=12:5)
        else:
            self.value = tmp_update[1][quota_pos+1: -1]

        # solve the position
        equal_pos = tmp_update[2].index("=")
        double_dot_pos = tmp_update[2].index(":")
        self.position = [int(tmp_update[2][equal_pos+1:double_dot_pos]), int(tmp_update[2][double_dot_pos+1:-1])]

    def get_symbol(self):
        '''
        return self.symbol
        '''
        return self.symbol

    def get_position(self):
        '''
        return self.position
        '''
        return self.position

    def get_value(self):
        '''
        return self.value
        '''
        return self.value

class Parse(object):
    def __init__(self):
        '''
        token_list : the input of output_lexer
        obj: SLR object
        parse_analyse_string: the string used to parse_analyse
        parse_element_list: the list of parse_element
        '''
        self.token_list = None
        self.obj = SLR(GRAMMAR, '@')
        self.semantic_analyser = None
        self.parse_analyse_string = ""
        self.parse_element_list = []
        self.err_list = []

    def gen_parse_prepare(self, output_lexer):
        '''
        output_lexer: the output of Lexer (token_list)
        fill the self.token_list and self.parse_element_list and self.parse_analyse_string
        '''
        self.token_list = output_lexer
        self.parse_analyse_string = ""
        self.parse_element_list = []
        for i in self.token_list:
            if str(i) == "Token(TokenType.EOF None position=None:None)":
                continue
            tmp_element = Parse_Element()
            tmp_element.update_element(str(i))
            self.parse_element_list.append(tmp_element)
            self.parse_analyse_string += tmp_element.get_symbol()

    def parse_process(self, output_lexer):
        self.gen_parse_prepare(output_lexer)
        self.semantic_analyser = Semantic_Process()
        result = self.obj.construct_parse_tree(self.parse_analyse_string, self.parse_element_list, self.semantic_analyser)
        self.err_list = []
        if result > 0:
            self.err_list.append(
                "ParseError: Meet Wrong input:" + MAP_REVERSE_TERMINAL_LIST[self.parse_analyse_string[0-result]] +
                " position=" + str(self.parse_element_list[0-result].get_position()[0]) + "," +
                str(self.parse_element_list[0-result].get_position()[1]))
        elif result == 0:
            self.err_list.append(
                "ParseError: Meet Wrong input: #  Can't finish Successfully")

    def get_err_list(self):
        '''
        return the err_list
        '''
        return self.err_list

if __name__ =='__main__':
    list = ["Token(TokenType.INT 'INT' position=1:1)",
            "Token(TokenType.ID 'a' position=1:5)",
            "Token(TokenType.SEMI ';' position=1:6)",
            "Token(TokenType.INT 'INT' position=2:1)",
            "Token(TokenType.ID 'b' position=2:5)",
            "Token(TokenType.LBRACKET '[' position=2:6)",
            "Token(TokenType.INTEGER_CONST 2 position=2:7)",
            "Token(TokenType.RBRACKET ']' position=2:8)",
            "Token(TokenType.SEMI ';' position=2:9)",
            "Token(TokenType.INT 'INT' position=3:1)",
            "Token(TokenType.ID 'main' position=3:5)",
            "Token(TokenType.LPAREN '(' position=3:9)",
            "Token(TokenType.VOID 'VOID' position=3:10)",
            "Token(TokenType.RPAREN ')' position=3:14)",
            "Token(TokenType.LBRACE '{' position=3:15)",
            "Token(TokenType.ID 'a' position=4:2)",
            "Token(TokenType.ASSIGN '=' position=4:3)",
            "Token(TokenType.ID 'b' position=4:4)",
            "Token(TokenType.LBRACKET '[' position=4:5)",
            "Token(TokenType.INTEGER_CONST 0 position=4:6)",
            "Token(TokenType.RBRACKET ']' position=4:7)",
            "Token(TokenType.SEMI ';' position=4:8)",
            "Token(TokenType.RBRACE '}' position=5:1)"]
    test = Parse()
    test.parse_process(list)