同济大学编译原理课程设计

简介：程序模拟类C语言编译器，要求提供词法分析、语法分析、符号表管理、中间代码生成、静态语义检查以及目标代码生成等功能。并且类C编译器是一个一遍的编译程序，词法分析程序作为子程序，被语法分析程序所调用。语法分析过程中要求在语法分析的同时生成中间代码，且最终生成汇编可执行的目标代码，要求可以使用mars对汇编代码进行运行。同时该类C语言编译器要求实现函数调用以及包含数组的中间代码和目标代码生成。程序要求提供图形化界面以供展示。

a.notation_removal.py 封装了注释的处理包括注释的错误定位以及源程序中正确注释的去除，提供接口给词法分析器调用

b.Lexer.py封装词法分析器的可接受字段以及词法分析过程，提供词法分析接口供语法分析调用

c.FIRST_FOLLOW_SET.py封装了给定一个文法，计算其每个文法符号FIRST集合和FOLLOW集合的相关算法，提供接口供语法分析调用

d.Semantic_analyse.py封装了语义分析的实现过程，由于需要仅一遍分析即产生中间代码，因此需要提供接口供语法分析调用

e.Parse_Analyse_Tree.py封装了生成语法分析树的过程，提供接口供语法分析调用

f.SLR.py完成对整个自下而上语法分析的封装实现，为语法分析器提供调用接口

g.Parser.py 是连接词法分析器、语义分析器的核心，完成对SLR的调用生成语法分析树、完成词法分析和语义分析的过程

h.target.py 封装了目标代码的实现过程，将最后生成的目标代码保存至文件中

i.claim.py 用于提供文法规则，文法终结符，非终结符等声明信息

语义分析规则：
<程序> ::= <占位符N> <声明串>      backpatch(N.nextlist, find(main).quad)

<声明> ::= INT ID ;               var_table.insert(ID.name, int, layer, 1)

<声明> ::= INT ID <占位符M> <占位符A> <函数声明>     
func_table.insert(ID.name,int,param_list, M.quad)

<声明> ::= INT ID <数组声明> ;
var_table.insert(ID.name, int, layer, <数组声明>.size)

<声明> ::= VOID ID <占位符M> <占位符A> <函数声明>    
func_table.insert(ID.name,void,param_list, M.quad)

<函数声明> ::= ( <形参> ) <语句块>  
<函数声明>.param_list = <形参>.param_list 
  
<数组声明> ::= [ INTEGER_CONST ]              
<数组声明>.size = [INTEGER_CONST]
    
<数组声明1> ::= [ INTEGER_CONST ]<数组声明2>    
<数组声明1>.size = [INTEGER_CONST] + <数组声明2>.size
    
    !! 注：param_list中存放参数的类型 而不是名字
<形参> ::= <参数列表>                         
<形参>.param_list = <参数列表>.param_list

<形参> ::= VOID                  <形参>.param_list = []  

<参数列表> ::= <参数>             <参数列表>.param_list = [int]

<参数列表1> ::= <参数> , <参数列表2>            
<参数列表1>.param_list = <参数列表2>   <参数列表1>.append(int)

<参数> ::= INT ID                  var_table.insert(ID.name, int, layer, 4)

<语句块> ::= { <内部声明> <语句串> }            
<语句块>.nextlist = <语句串>.nextlist layer--   var_table.pop(layer+1)
    
<内部变量声明> ::= INT ID          var_table.insert(ID.name, int, layer, 4)
    
<语句串> ::= <语句>                <语句串>.nextlist = <语句>.nextlist

<语句串1> ::= <语句><占位符M><语句串2>           
<语句串1>.nextlist = <语句串2>.nextlist backpatch(<语句>.nextlist, M.quad)
    
<语句> ::= <if语句>                <语句>.nextlist = <if语句>.nextlist
    
<语句> ::= <while语句>             <语句>.nextlist = <while语句>.nextlist
    
<语句> ::= <return语句>             <语句>.nextlist = []

<语句> ::= <赋值语句>              <语句>.nextlist = []
    
<赋值语句> ::= ID = <表达式>;       emit(=,<表达式>.name,_,ID.name)
    
<赋值语句> ::= <数组> = <表达式>;   emit(=,<表达式>.name,_,<数组>.name)
    
<return语句> ::= RETURN ;          emit(return, _, _, _)          
    
<return语句> ::= RETURN <表达式> ;     emit(return, <表达式>.name,_,_)
    
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
                                
<表达式> ::= <加法表达式>     
                                <表达式>.name = <加法表达式>.name   
                                <表达式>.truelist = [nextquad]  
                                <表达式>.falselist=[nextquad+1]
                                
<表达式> ::= <加法表达式1> < <加法表达式2>       
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

<加法表达式> ::= <项>            <加法表达式>.name = <项>.name

<加法表达式1> ::= <项> + <加法表达式2>    
<加法表达式1>.name = newTemp()  
emit(+,<项>.name,<加法表达式2>.name,<加法表达式1>.name)

<加法表达式1> ::= <项> - <加法表达式2>    
<加法表达式1>.name = newTemp()  
emit(-,<项>.name,<加法表达式2>.name,<加法表达式1>.name)

<项> ::= <因子>                  <项>.name = <因子>.name
    
<项1> ::= <因子> * <项2>         <项1>.name = newTemp()   
emit(*,<因子>.name,<项2>.name,<项1>.name)
 
<项1> ::= <因子> / <项2>          <项1>.name = newTemp()   
emit(/,<因子>.name,<项2>.name,<项1>.name)

<因子> ::= INTEGER_CONST       <因子>.name = INTEGER_CONST

<因子> ::= ( <表达式> )            <因子>.name = <表达式>.name
    
<因子> ::= ID                           
                            if var_table.find(ID.name) == None error;
                            else  <因子>.name = ID.name
    
<因子> ::= ID ( <实参> )
                            f = func_table.find(ID.name, <实参>.param_list)
                            if f == None error;
                            else
                                push <实参>.param_list  
emit(push, _, _, sp) 
emit(jal,func_table.find(ID.name).entry)
emit(pop, _, _, sp) 
                            if(f.returnType == int)
                                <因子>.name = newTemp()  
emit(=,ID.name(),_,<因子>.name)
                                    
<因子> ::= <数组>             <因子>.name = <数组>.name    

<数组> ::= ID [ <表达式> ]      
<数组>.layer = ID.layer  
<数组>.name = ID.name[<表达式>.name]   
<数组>.size = [int(<表达式>.name)]

<数组1> ::= <数组2> [ <表达式> ]    
<数组1>.name = <数组2>.name + [<表达式>.name]  
<数组1>.size = <数组2>.size +[int(<表达式>.name)]
                              <数组1>.layer = <数组2>.layer

<实参> ::= e                    <实参>.param_list = []

<实参> ::= <实参列表>           <实参>.param_list = <实参列表>.param_list

<实参列表> ::= <表达式>         <实参列表>.param_list = [<表达式>.name]

<实参列表1> ::= <表达式> , <实参列表2>        
<实参列表1>.param_list = <实参列表2>.param_list   
<实参列表1>.append(<表达式>.name) 

<占位符M> ::= e                 M.quad = nextquad

<占位符N> ::= e                 N.nextlist = [nextquad]  emit(j,_,_,_)

<占位符A> ::= e                 layer++

<占位符S> ::= e			  	f = func_table.find(ID.name, <实参>.param_list)
                            if f != None error;
                            func_table.insert()