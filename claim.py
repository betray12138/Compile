Array_Num = 33
Front_Char = '@'
'''  非终结符序列
    程序           @
    声明串         A
    声明           B
    声明类型        C
    变量声明        D
    函数声明        E
    数组声明        F
    形参           G
    参数列表        H
    参数           I
    语句块         J
    内部声明        K
    内部变量声明     L
    语句串         M
    语句           N
    赋值语句        O
    return语句     P
    while语句      Q
    if语句         R
    表达式         S
    加法表达式      T
    项            U
    因子           V
    FTYPE         W
    call          X
    数组           Y
    实参           Z
    实参列表        [
    占位符M        ]
    占位符N        ^
    占位符A        _
    占位符S        `
'''
NONTERMIAL_LIST = ['@', 'A', 'B', 'C', 'D', 'E', 'F',
                   'G', 'H', 'I', 'J', 'K', 'L',
                   'M', 'N', 'O', 'P', 'Q', 'R',
                   'S', 'T', 'U', 'V', 'W', 'X',
                   'Y', 'Z', '[', '', ']', '^', '_', '`']


MAP_NONTERMINAL_LIST = {'<声明串>': 'A', '<声明>': 'B', '<声明类型>': 'C', '<变量声明>': 'D', '<函数声明>': 'E',
                        '<数组声明>': 'F', '<形参>': 'G', '<参数列表>': 'H', '<参数>': 'I', '<语句块>': 'J',
                        '<内部声明>': 'K', '<内部变量声明>': 'L', '<语句串>': "M", '<语句>': "N", '<赋值语句>': "O",
                        '<return语句>': 'P', '<while语句>': 'Q', '<if语句>': 'R', '<表达式>': 'S', '<加法表达式>': 'T',
                        '<项>': "U", '<因子>': 'V', '<FTYPE>': 'W', '<call>': 'X', '<数组>': 'Y',
                        '<实参>': 'Z', '<实参列表>': '[', '<程序>': '@', '<占位符M>': ']', '<占位符N>': '^',
                        '<占位符A>': '_', '<占位符S>': '`'}

MAP_REVERSE_NONTERMINAL_LIST = {'A': '<声明串>', 'B': '<声明>', 'C': '<声明类型>', 'D': '<变量声明>', 'E': '<函数声明>',
                                'F': '<数组声明>', 'G': '<形参>', 'H': '<参数列表>', 'I': '<参数>', 'J': '<语句块>',
                                'K': '<内部声明>', 'L': '<内部变量声明>', 'M': "<语句串>", 'N': "<语句>", 'O': "<赋值语句>",
                                'P': '<return语句>', 'Q': '<while语句>', 'R': '<if语句>', 'S': '<表达式>', 'T': '<加法表达式>',
                                'U': "<项>", 'V': '<因子>', 'W': '<FTYPE>', 'X': '<call>', 'Y': '<数组>',
                                'Z': '<实参>', '[': '<实参列表>', '@': '<程序>', ']': '<占位符M>', '^': '<占位符N>',
                                '_': '<占位符A>', '`': '<占位符S>'}

MAP_REVERSE_NONTERMINAL_EN_LIST = {'A': '<Program>', 'B': '<Declare>', 'C': '<Declare Type>', 'D': '<Variable Declare>',
                                   'E': '<Func Declare>', 'F': '<Array Declare>', 'G': '<Formal Param>', 'H': '<Formal Param List>',
                                   'I': '<Params>', 'J': '<Statement Block>', 'K': '<Inner Declare>', 'L': '<Inner Variable Declare>',
                                   'M': "<Statement Set>", 'N': "<Statement>", 'O': "<Assign Statement>", 'P': '<Return Statement>',
                                   'Q': '<While Statement>', 'R': '<If Statement>', 'S': '<Expression>', 'T': '<Plus Expression>',
                                   'U': "<Item>", 'V': '<Factor>', 'W': '<FTYPE>', 'X': '<Call>',
                                   'Y': '<Array>', 'Z': '<Actual Param>', '[': '<Actual Param List>', '@': '<Demo>',
                                   ']': '<placeholder M>', '^': '<placeholder N>', '_': '<placeholder A>', '`': '<placeholder S>'}

''' 终结符序列
    INT           t
    VOID          v
    IF            i
    ELSE          l
    WHILE         w
    RETURN        r
    ID            d
    INTEGER_CONST g
    ASSIGN        =
    PLUS          +
    MINUS         -
    MUL           *
    DIV           /
    LG            y
    LT            x
    LTE           b
    NOT_EQUAL     n
    LGE           c
    EQUAL         f
    SEMI          ;
    COMMA         ,
    LPAREN        (
    RPAREN        )
    LBRACE        {
    RBRACE        }
    LBRACKET      z
    RBRACKET      k
'''
TERMINAL_LIST = ['b', 'c', 'd', 'f', 'g',
                 'i', 'l', 'n', 'r', 't',
                 'v', 'w', 'z', '=', '+',
                 '-', '*', '/', 'x', 'y',
                 ';', ',', ')', '(', '{',
                 '}', 'k']

MAP_TERMINAL_LIST = {"INT": 't', "VOID": 'v', "IF": 'i', "ELSE": 'l', "WHILE": 'w',
                     "RETURN": 'r', "ID": 'd', "INTEGER_CONST": 'g', "ASSIGN": '=', "PLUS": '+',
                     "MINUS": '-', "MUL": '*', "DIV": '/', "LG": 'y', "LT": 'x',
                     "LTE": 'b', "NOT_EQUAL": 'n', "LGE": 'c', "EQUAL": 'f', "SEMI": ';',
                     "COMMA": ',', "LPAREN": '(', "RPAREN": ')', "LBRACE": '{', "RBRACE": '}',
                     "LBRACKET": 'z', "RBRACKET": 'k'}

MAP_REVERSE_TERMINAL_LIST = {"t": 'INT', "v": 'VOID', "i": 'IF', "l": 'ELSE', "w": 'WHILE',
                             "r": 'RETURN', "d": 'ID', "g": 'INTEGER_CONST', "=": 'ASSIGN', "+": 'PLUS',
                             "-": 'MINUS', "*": 'MUL', "/": 'DIV', "y": 'LG', "x": 'LT',
                             "b": 'LTE', "n": 'NOT_EQUAL', "c": 'LGE', "f": 'EQUAL', ";": 'SEMI',
                             ",": 'COMMA', "(": 'LPAREN', ")": 'RPAREN', "{": 'LBRACE', "}": 'RBRACE',
                             "z": 'LBRACKET', "k": 'RBRACKET'}

''' GRAMMAR
    <程序> ::= <占位符N> <声明串>                                 @ -> ^A
    <声明串> ::= <声明> | <声明><声明串>                           A->B|BA
    <声明> ::= INT ID ; | INT ID <占位符M> <占位符A> <函数声明> |
              INT ID <数组声明> ;| VOID ID <占位符M> <占位符A> <函数声明>     B->td;|td]_E|tdF;|vd]_E
    <函数声明> ::= ( <形参> ) <占位符S> <语句块>                    E->(G)`J
    <数组声明> ::= [ INTEGER_CONST ] | [ INTEGER_CONST ]<数组声明> F->zgk|zgkF
    <形参> ::= <参数列表> | VOID                                  G->H|v
    <参数列表> ::= <参数> | <参数> , <参数列表>                     H->I|I,H
    <参数> ::= INT ID                                           I->td
    <语句块> ::= { <内部声明> <语句串> }                           J->{KM}
    <内部声明> ::= e | <内部变量声明> ;<内部声明>                    K->e|L;K
    <内部变量声明> ::= INT ID                                     L->td
    <语句串> ::= <语句> | <语句><占位符M><语句串>                    M->N|N]M
    <语句> ::= <if语句> | <while语句> | <return语句> | <赋值语句>   N->R|Q|P|O
    <赋值语句> ::= ID = <表达式>; | <数组> = <表达式>;              O->d=S;|Y=S;
    <return语句> ::= RETURN ;| RETURN <表达式> ;                 P->r;|rS;
    <while语句> ::= WHILE <占位符M>( <表达式> ) <占位符M2> <占位符A> <语句块>   Q->w](S)]_J
    <if语句> ::= IF ( <表达式> ) <占位符M> <占位符A> <语句块> |      R->i(S)]_J|i(S)]_J^l]_J
                IF ( <表达式> ) <占位符M1> <占位符A> <语句块> <占位符N> ELSE <占位符M2> <占位符A> <语句块>    
    <表达式> ::= <加法表达式> < <加法表达式> | <加法表达式> > <加法表达式> | <加法表达式> == <加法表达式> | <加法表达式> >= <加法表达式>
                <加法表达式> <= <加法表达式> | <加法表达式> != <加法表达式> | <加法表达式>     S->TxT|TyT|TfT|TcT|TbT|TnT|T
    <加法表达式> ::= <项> | <项> + <加法表达式> | <项> - <加法表达式>              T->U|U+T|U-T
    <项> ::= <因子> | <因子> * <项> | <因子> / <项>             U->V|V*U|V/U
    <因子> ::= INTEGER_CONST | ( <表达式> ) | ID | <数组> | ID ( <实参> )  V->g|(S)|d|Y|d(Z)
    <数组> ::= ID [ <表达式> ] | <数组> [ <表达式> ]                Y->dzSk|YzSk
    <实参> ::= <实参列表> | e                                      Z->[|e
    <实参列表> ::= <表达式> | <表达式> , <实参列表>                   [->S|S,[
    <占位符M> ::= e                                               ]->e
    <占位符N> ::= e                                               ^->e
    <占位符A> ::= e                                               _->e
    <占位符S> ::= e                                               `->e
'''
GRAMMAR = ["@->^A",
           "A->B|BA",
           "B->td;|td]_E|tdF;|vd]_E",
           "E->(G)`J",
           "F->zgk|zgkF",
           "G->H|v",
           "H->I|I,H",
           "I->td",
           "J->{KM}",
           "K->e|L;K",
           "L->td",
           "M->N|N]M",
           "N->R|Q|P|O",
           "O->d=S;|Y=S;",
           "P->r;|rS;",
           "Q->w](S)]_J",
           "R->i(S)]_J|i(S)]_J^l]_J",
           "S->T|TxT|TyT|TfT|TcT|TbT|TnT",
           "T->U|U+T|U-T",
           "U->V|V*U|V/U",
           "V->g|(S)|d|Y|d(Z)",
           "Y->dzSk|YzSk",
           "Z->[|e",
           "[->S|S,[",
           "]->e",
           "^->e",
           "_->e",
           "`->e"]

''' Semantic Rules
    <程序> ::= <占位符N> <声明串>                      backpatch(N.nextlist, find(main).quad)
    <声明> ::= INT ID ;                              var_table.insert(ID.name, int, layer, 1)
    <声明> ::= INT ID <占位符M> <占位符A> <函数声明>     func_table.insert(ID.name,int,param_list, M.quad)
    <声明> ::= INT ID <数组声明> ;                     var_table.insert(ID.name, int, layer, <数组声明>.size)
    <声明> ::= VOID ID <占位符M> <占位符A> <函数声明>    func_table.insert(ID.name,void,param_list, M.quad)

    <函数声明> ::= ( <形参> ) <语句块>              <函数声明>.param_list =  <形参>.param_list 
    <数组声明> ::= [ INTEGER_CONST ]              <数组声明>.size = [INTEGER_CONST]
    <数组声明1> ::= [ INTEGER_CONST ]<数组声明2>    <数组声明1>.size = [INTEGER_CONST] + <数组声明2>.size
    
    !! 注：param_list中存放参数的类型 而不是名字
    <形参> ::= <参数列表>                         <形参>.param_list = <参数列表>.param_list
    <形参> ::= VOID                             <形参>.param_list = []  

    <参数列表> ::= <参数>                         <参数列表>.param_list = [int]
    <参数列表1> ::= <参数> , <参数列表2>            <参数列表1>.param_list = <参数列表2>   <参数列表1>.append(int)

    <参数> ::= INT ID                            var_table.insert(ID.name, int, layer, 4)
    <语句块> ::= { <内部声明> <语句串> }            <语句块>.nextlist = <语句串>.nextlist layer--   var_table.pop(layer+1)
    
    <内部变量声明> ::= INT ID                      var_table.insert(ID.name, int, layer, 4)
    
    <语句串> ::= <语句>                            <语句串>.nextlist = <语句>.nextlist
    <语句串1> ::= <语句><占位符M><语句串2>           <语句串1>.nextlist = <语句串2>.nextlist backpatch(<语句>.nextlist, M.quad)
    
    <语句> ::= <if语句>                           <语句>.nextlist = <if语句>.nextlist
    <语句> ::= <while语句>                        <语句>.nextlist = <while语句>.nextlist
    <语句> ::= <return语句>                       <语句>.nextlist = []
    <语句> ::= <赋值语句>                          <语句>.nextlist = []
    
    <赋值语句> ::= ID = <表达式>;                  emit(=,<表达式>.name,_,ID.name)
    <赋值语句> ::= <数组> = <表达式>;               emit(=,<表达式>.name,_,<数组>.name)
    
    <return语句> ::= RETURN ;                    emit(return, _, _, _)          
    <return语句> ::= RETURN <表达式> ;            emit(return, <表达式>.name,_,_)
    
    <while语句> ::= WHILE <占位符M1>( <表达式> ) <占位符M2> <占位符A> <语句块>  
                                backpatch(<语句块>.nextlist,M1.quad) 
                                backpatch(<表达式>.truelist, M2.quad)
                                <while语句>.nextlist = <表达式>.falselist 
                                emit(j,_,_,M1.quad)
    
    <if语句> ::= IF ( <表达式> ) <占位符M> <占位符A> <语句块>
                                backpatch(<表达式>.truelist,M.quad)
                                <if语句>.nextlist = merge(<表达式>.falselist, <语句块>.nextlist)
                                
    <if语句> ::= IF ( <表达式> ) <占位符M1> <占位符A> <语句块1> <占位符N> ELSE <占位符M2> <占位符A> <语句块2>    
                                backpatch(<表达式>.truelist,M1.quad)
                                backpatch(<表达式>.falselist,M2.quad)
                                <if语句>.nextlist = merge(<语句块1>.nextlist, N.nextlist, <语句块2>.nextlist)
                                
    <表达式> ::= <加法表达式>      !!! 默认不出现relop的情况用于赋值
                                <表达式>.name = <加法表达式>.name   
                                <表达式>.truelist = [nextquad]  
                                <表达式>.falselist=[nextquad+1]
                                
    <表达式> ::= <加法表达式1> < <加法表达式2>         !!! 默认出现relop的情况 用于条件比较 不用于赋值操作
                                <表达式>.name = NULL  
                                <表达式>.truelist = [nextquad] 
                                <表达式>.falselist = [nextquad+1]
                                emit(j relop, <加法表达式1>.name, <加法表达式2>.name，_)
                                emit(j,_,_,_)
    <表达式> ::= <加法表达式> > <加法表达式>
    <表达式> ::= <加法表达式> <= <加法表达式>
    <表达式> ::= <加法表达式> >= <加法表达式>
    <表达式> ::= <加法表达式> == <加法表达式>
    <表达式> ::= <加法表达式> != <加法表达式>

    <加法表达式> ::= <项>                   <加法表达式>.name = <项>.name
    <加法表达式1> ::= <项> + <加法表达式2>    <加法表达式1>.name = newTemp()  emit(+,<项>.name,<加法表达式2>.name,<加法表达式1>.name)
    <加法表达式1> ::= <项> - <加法表达式2>    <加法表达式1>.name = newTemp()  emit(-,<项>.name,<加法表达式2>.name,<加法表达式1>.name)

    <项> ::= <因子>                        <项>.name = <因子>.name
    <项1> ::= <因子> * <项2>                <项1>.name = newTemp()   emit(*,<因子>.name,<项2>.name,<项1>.name)
    <项1> ::= <因子> / <项2>                <项1>.name = newTemp()   emit(/,<因子>.name,<项2>.name,<项1>.name)

    <因子> ::= INTEGER_CONST               <因子>.name = INTEGER_CONST
    <因子> ::= ( <表达式> )                  <因子>.name = <表达式>.name
    <因子> ::= ID                           
                            if var_table.find(ID.name) == None error;
                            else  <因子>.name = ID.name
    <因子> ::= ID ( <实参> )
                            f = func_table.find(ID.name, <实参>.param_list)
                            if f == None error;
                            else
                                push <实参>.param_list   emit(jal,func_table.find(ID.name).enterPoint)
                                if(f.returnType == int)
                                    <因子>.name = newTemp()  emit(=,ID.name(),_,<因子>.name)
                                    
    <因子> ::= <数组>                          <因子>.name = <数组>.name    

    <数组> ::= ID [ <表达式> ]      <数组>.layer = ID.layer  <数组>.name = ID.name[<表达式>.name]   <数组>.size = [int(<表达式>.name)]
    <数组1> ::= <数组2> [ <表达式> ]    <数组1>.name = <数组2>.name + [<表达式>.name]  <数组1>.size = <数组2>.size +[int(<表达式>.name)]
                                     <数组1>.layer = <数组2>.layer
    <实参> ::= e                              <实参>.param_list = []
    <实参> ::= <实参列表>                       <实参>.param_list = <实参列表>.param_list

    <实参列表> ::= <表达式>                     <实参列表>.param_list = [<表达式>.name]
    <实参列表1> ::= <表达式> , <实参列表2>        <实参列表1>.param_list = <实参列表2>.param_list   <实参列表1>.append(<表达式>.name) 
    <占位符M> ::= e                            M.quad = nextquad
    <占位符N> ::= e                            N.nextlist = [nextquad]  emit(j,_,_,_)
    <占位符A> ::= e                            layer++
'''