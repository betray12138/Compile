# pretreat to remove the notation
# parameter：
#          src_code
# ret      dst_code     has been solved


# update the lock area    -update the error-found    -correct the problem of wrong position in real file

class CommentError(object):
    def __init__(self):
        self.comment_error = []

    def push_in(self, message):
        length = len(self.comment_error)
        if length == 0 or message != self.comment_error[length-1]:
            self.comment_error.append(message)

    def pop_out(self):
        output_list = self.comment_error
        return output_list

    def clear(self):
        self.comment_error = []

def notation_removal(src_code, comment_error):
    # remove the space and \t head and tail
    src_code = src_code.strip(" \t")
    code_len = len(src_code)
    dst_code = ''
    i = 0
    lock = 0                # use to make sure the lock area
    row = 1                 # define the count of row
    num_enter = 0           # use to record the number of \n
    flag = False                # use to symbolize whether find the */ or not
    while i < code_len:
        if i + 1 < code_len and i >= lock:
            if src_code[i] == '/' and src_code[i+1] == '/':
                # solve the condition with //
                while i != code_len and src_code[i] != '\n':
                    i += 1
                    
            elif src_code[i] == '/' and src_code[i+1] == '*':
                # solve the condition with /* */
                point = i              # use pointer to sign
                i = i+2
                if i == code_len:      # to prevent overflow
                    i = point
                else:
                    while i <= code_len-2 and not(src_code[i] == '*' and src_code[i+1] == '/'):
                        i += 1
                        if src_code[i] == '\n':
                            num_enter += 1
                    if i == code_len-1:
                        lock = i
                        i = point      # hasn't found the */ ,use pointer to recover
                    else:
                        i += 2
                        flag = True
        if flag:             # find the right match for /* ,update the row and dst_str
            dst_code += num_enter*'\n'
            row += num_enter
            num_enter = 0

        if i < code_len-1 and ((src_code[i] == '*' and src_code[i+1] == '/') or (src_code[i] == '/' and src_code[i+1] == '*')):
            comment_error.push_in('Error! illegal comment on row {}'.format(row))
            # print('Error! illegal comment on row {}'.format(row))
        if i < code_len:
            dst_code += src_code[i]
            if src_code[i] == '\n':
                row += 1
        i += 1

    return dst_code

'''
def main():
    lines=[]
    while True:
        try:
            lines.append(input())
        except:                   #use ctrl+c to trigger interrupt
            break
    code=''
    for j in range (len(lines)-1):
        code+=lines[j]
        code+='\n'
    code=code.strip("\n")
    dst_code=notation_removal(code)
    print(dst_code)


main()
'''