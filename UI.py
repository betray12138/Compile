from compile import *
import pyqt5_tools
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, qApp
import sys
from PyQt5.QtGui import QIcon
from Lexer import *
from parser_UI import *
from Gen_code import *
from Parse import *
from Semantic_analyse import *
from notation_removal import *
from target import *

'''
function: wait some times without delaying other op
'''
def wait(msec):
    reachtime = QTime.currentTime().addMSecs(msec)
    while QTime.currentTime() < reachtime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)



'''
:params:
    toolbarlist: save all of the icon , in order to detect trigger conveniently
    commentError: save the error information in the process of commentError 
    lexer_content: save the text used to execute Lexer operation
    input_content: save the text read from the file 
    execute_pos: save the pos(step) in the operation of Lexer operation
    input_row: save the number of row about the input text
    Lexer: obtain the content about err_list and tokenlist
    Parser: obtain the content about ParserTree
'''

'''
toolbarList index
'''
ICON_OPEN_FILE = 0
ICON_COMMENT_CHECK = 1
ICON_RUN_ALL = 2
ICON_RUN_SINGLE = 3
ICON_RUN_MANY = 4
ICON_STOP = 5
ICON_PARSER = 6
ICON_SAVE = 7
ICON_GEN_INTER = 8
ICON_GEN_OBJECT = 9
'''
Time_GAP
'''
TIME_GAP = 10

class MyCompile(Ui_MainWindow, QMainWindow):
    def __init__(self, MainWindow, parent=None):
        super(MyCompile, self).__init__()
        self.mainwindow = MainWindow
        self.mainwindow.setFixedSize(1200, 900)
        self.setupUi(self.mainwindow)
        self.toolbarList = []
        self.commentError = CommentError()
        self.lexer_content = ''
        self.input_content = ''
        self.execute_pos = 1
        self.input_row = 1
        self.Lexer = Lexer('11111')
        self.Parser = ''
        self.init_ui()

    def init_ui(self):
        # window background
        self.switch_pic('bg.jpg')

        # textBrowser
        self.change_bg_text('bg.jpg')
        self.textBrowser.hide()

        # textEdit   input-forbidden at the beginning
        self.textEdit.setFocusPolicy(QtCore.Qt.NoFocus)


        self.status_bar_change()
        self.init_tool_bar()

        # connect 机制
        # ----button open triggered
        self.open.triggered.connect(self.file_path_input)

        # ----button input triggered
        self.focus.triggered.connect(self.open_textedit)

        # ----button save triggered
        self.actionsave.triggered.connect(self.save_information)

        # ----button single_step triggered
        self.single_step.triggered.connect(self.run_lexer_single_step)

        # ----button many_steps triggered
        self.many_steps.triggered.connect(self.run_lexer_many_steps)

        # ----button run_all triggered
        self.run_all.triggered.connect(self.run_lexer_all_steps)

        # ----button clear_all triggered
        self.clear_all.triggered.connect(self.clear_all_process)

        # ----button parser triggered
        self.actiondo_parser_analysis.triggered.connect(self.parser_process)

        # ----button gen_inter_code triggered
        self.actiondo_gen_inter_code.triggered.connect(self.gen_inter_process)

        # ----button gen_object_code triggered
        self.actiongen_object_code.triggered.connect(self.gen_object_code)

        # ----icon file triggered
        self.toolbarList[ICON_OPEN_FILE].triggered.connect(self.file_path_input)

        # ----icon comment check
        self.toolbarList[ICON_COMMENT_CHECK].triggered.connect(self.comment_check)

        # ----icon all step triggered
        self.toolbarList[ICON_RUN_ALL].triggered.connect(self.run_lexer_all_steps)

        # ----icon single_step triggered
        self.toolbarList[ICON_RUN_SINGLE].triggered.connect(self.run_lexer_single_step)

        # ----icon many steps triggered
        self.toolbarList[ICON_RUN_MANY].triggered.connect(self.run_lexer_many_steps)

        # ----icon stop triggered
        self.toolbarList[ICON_STOP].triggered.connect(self.stop_step_op)

        # ----icon Parser triggered
        self.toolbarList[ICON_PARSER].triggered.connect(self.parser_process)

        # ----icon Save triggered
        self.toolbarList[ICON_SAVE].triggered.connect(self.save_information)

        # ----icon Gen_inter_code triggered
        self.toolbarList[ICON_GEN_INTER].triggered.connect(self.gen_inter_process)

        # ----icon gen_object_code triggered
        self.toolbarList[ICON_GEN_OBJECT].triggered.connect(self.gen_object_code)
    '''
    function: open the input function of self.textEdit
    '''
    def open_textedit(self):
        self.textEdit.setFocus()

    '''
    function: show the reminding message on status bar according to the input no
    '''
    def status_bar_change(self, no=0):
        if no == 0:
            self.statusbar.showMessage('Ready')
        elif no == 1:
            self.statusbar.showMessage('Comment check has been finished successfully')
        elif no == 2:
            self.statusbar.showMessage('File open successfully')
        elif no == 3:
            self.statusbar.showMessage('File open meet Error')
        elif no == 4:
            self.statusbar.showMessage('Single step has been finished successfully')
        elif no == 5:
            self.statusbar.showMessage('all of the steps has been finished successfully')
        elif no == 6:
            self.statusbar.showMessage('Exit step operation')
        elif no == 7:
            self.statusbar.showMessage('Many steps have been finished successfully')
        elif no == 8:
            self.statusbar.showMessage('The lexer process has been finished successfully')
        elif no == 9:
            self.statusbar.showMessage("The clear all process has been done")
        elif no == 10:
            self.statusbar.showMessage('The information has been saved')
        elif no == 11:
            self.statusbar.showMessage('The Parser process finish successfully')
        elif no == 12:
            self.statusbar.showMessage('The Parser process meet failure')
        elif no == 13:
            self.statusbar.showMessage('The Semantic Analyse process meet failure')
        elif no == 14:
            self.statusbar.showMessage('The Semantic Analyse process finish successfully')
        elif no == 15:
            self.statusbar.showMessage('The Object code generating process finish successfully')

    '''
    function: finish the initial operation of tool bar
    '''
    def init_tool_bar(self):
        #tools bar
        open = QAction(QIcon('file.jpg'), 'open file', self.mainwindow)
        self.toolBar.addAction(open)
        self.toolbarList.append(open)

        #separator next-----comment_check
        self.toolBar.addSeparator()
        comment = QAction(QIcon('comment.jpg'), 'comment check', self.mainwindow)
        self.toolBar.addAction(comment)
        self.toolbarList.append(comment)

        #separator next-----lexer  run_all run_single run_many
        self.toolBar.addSeparator()
        lexer_run_all = QAction(QIcon('lexer_all.jpg'), 'run all', self.mainwindow)
        self.toolBar.addAction(lexer_run_all)
        self.toolbarList.append(lexer_run_all)
        lexer_run_single = QAction(QIcon('lexer_single.jpg'), 'run single', self.mainwindow)
        self.toolBar.addAction(lexer_run_single)
        self.toolbarList.append(lexer_run_single)
        lexer_run_many = QAction(QIcon('lexer_many.jpg'), 'run many', self.mainwindow)
        self.toolBar.addAction(lexer_run_many)
        self.toolbarList.append(lexer_run_many)
        stop = QAction(QIcon('stop.jpg'), 'stop', self.mainwindow)
        self.toolBar.addAction(stop)
        self.toolbarList.append(stop)

        # separator next-----Parser
        self.toolBar.addSeparator()
        parser = QAction(QIcon('parser.jpg'), 'do parser analysis', self.mainwindow)
        self.toolBar.addAction(parser)
        self.toolbarList.append(parser)

        # separator next-----Save
        self.toolBar.addSeparator()
        save = QAction(QIcon('save.jpg'), 'save the text', self.mainwindow)
        self.toolBar.addAction(save)
        self.toolbarList.append(save)

        # separator next---- Inter_code gen
        self.toolBar.addSeparator()
        gen_inter_code = QAction(QIcon('code.png'), 'gen intermediate code', self.mainwindow)
        self.toolBar.addAction(gen_inter_code)
        self.toolbarList.append(gen_inter_code)

        # separator next----- Object code gen
        self.toolBar.addSeparator()
        gen_object_code = QAction(QIcon('object.jpg'), 'gen object code', self.mainwindow)
        self.toolBar.addAction(gen_object_code)
        self.toolbarList.append(gen_object_code)

    '''
    function: Clear all button triggered 
    '''
    def clear_all_process(self):
        if self.execute_pos > 1:
            QMessageBox.information(self, "Remind", "Please exit the STEP condition first and retry")
            return 0
        self.execute_pos = 1
        self.textout.setText('')
        self.textBrowser.setText('')
        self.textBrowser.hide()
        self.open_textedit()
        self.status_bar_change(9)

    '''
    function: finish the input of the file path and obtain the content and show it onto the TextEdit
    '''
    def file_path_input(self):
        if self.execute_pos > 1:
            QMessageBox.information(self, "Remind", "Please exit the STEP condition first and retry")
            return 0
        ok = False
        file_path, ok = QFileDialog.getOpenFileName(self, "Choose File", '', 'C-Files(*.*)')
        if ok:
            try:
                open_file = open(file_path, 'r').read()
            except:
                self.status_bar_change(3)
                QMessageBox.critical(self, "Wrong", "Can't find the input file, please retry");
            else:
                self.textEdit.setFocus()
                self.textEdit.setTextColor(Qt.black)
                self.textEdit.setText(open_file)          #put the content into the textEdit
                self.status_bar_change(2)

    '''
    function: finish the process of comment check, get the self.lexer_content and update the statusbar
    '''
    def comment_check(self):
        if self.execute_pos > 1:
            QMessageBox.information(self, "Remind", "Please exit the STEP condition first and retry")
            return 0
        check_test = self.textEdit.toPlainText()
        self.input_content = check_test
        if check_test == '':
            QMessageBox.critical(self, "Wrong", "No input, please check and retry")
            return 0
        self.textBrowser.setText('')                     # reset every time
        self.commentError.clear()
        self.lexer_content = notation_removal(check_test, self.commentError)
        error_list = self.commentError.pop_out()
        for i in range(len(error_list)):
            self.textBrowser.append(error_list[i])
        self.textBrowser.show()
        if len(error_list):
            QMessageBox.critical(self, "Wrong", "Has notation Error, please check and retry")
            return 0
        self.status_bar_change(1)
        self.input_row = 1
        for i in range(len(self.input_content)):    # self.input_row indicate the file row
            if self.input_content[i] == '\n':
                self.input_row += 1
        return 1


    '''
    function: finish the lexer about single step ,enter the STEP condition, show the error and show the Token
    '''
    def run_lexer_single_step(self):
        if self.execute_pos == 1:
            if not self.comment_check():
                return 0
            self.textout.setText('')
            self.enter_step()
        token_list, err_list = self.exe_lexer()
        # check the input file unchangeable
        tmp_text = self.textEdit.toPlainText()
        # origin file has been modified
        if self.input_content != tmp_text:
            QMessageBox.critical(self, "Wrong", "The content has been modified")
            self.execute_pos = 1
            self.exit_step()
            self.textout.setText('')
            self.input_text_return_black(tmp_text, self.textout.toPlainText())
            self.textout.setText('')
            return 0

        # check the input file finished
        if self.execute_pos > self.input_row:
            self.exit_step()
            self.input_text_return_black(self.input_content, self.textout.toPlainText())
            self.execute_pos = 1
            self.status_bar_change(5)
            self.textout.setText('')
            return 0

        vertical_bar = self.textout.verticalScrollBar().value()
        origin_text = self.textout.toPlainText()
        self.textout.setTextColor(Qt.black)
        self.textout.setText(origin_text)
        self.textout.verticalScrollBar().setValue(vertical_bar)
        self.textout.setTextColor(Qt.blue)
        self.show_token_list(self.execute_pos, self.execute_pos, token_list)
        self.show_err_list(self.execute_pos, err_list)
        self.highlight_execute_step()
        self.textout.setTextColor(Qt.black)

        self.status_bar_change(4)
        return 1

    '''
    function: finish the lexer about many steps ,enter the STEP condition, show the error and show the Token
    '''
    def run_lexer_many_steps(self):
        if self.execute_pos == 1:
            if not self.comment_check():
                return 0
            self.textout.setText('')
        token_list, err_list = self.exe_lexer()
        # check the input file unchangeable
        tmp_text = self.textEdit.toPlainText()
        # origin file has been modified
        if self.input_content != tmp_text:
            QMessageBox.critical(self, "Wrong", "The content has been modified")
            self.execute_pos = 1
            self.exit_step()
            self.input_text_return_black(tmp_text, self.textout.toPlainText())
            self.textout.setText('')
            return 0

        input_steps = QInputDialog()
        steps, ok = input_steps.getInt(self, "input_steps", "Please input the execute steps", 1, 1, self.input_row-self.execute_pos+2)
        if not ok:
            return 0
        if self.execute_pos == 1:
            self.enter_step()

        vertical_bar = self.textout.verticalScrollBar().value()
        origin_text = self.textout.toPlainText()
        self.textout.setTextColor(Qt.black)
        self.textout.setText(origin_text)
        self.textout.verticalScrollBar().setValue(vertical_bar)
        self.textout.setTextColor(Qt.blue)
        for i in range(steps):
            # check the input file finished
            if self.execute_pos > self.input_row:
                self.exit_step()
                self.input_text_return_black(self.input_content, self.textout.toPlainText())
                self.execute_pos = 1
                self.status_bar_change(5)
                self.textout.setTextColor(Qt.black)
                self.textout.setText('')
                return 0
            self.show_token_list(self.execute_pos, self.execute_pos, token_list)
            self.show_err_list(self.execute_pos, err_list)
            self.highlight_execute_step()
        self.status_bar_change(7)
        self.textout.setTextColor(Qt.black)
        return 1


    '''
    function: finish the lexer about all steps ,show the error and show the Token
    '''
    def run_lexer_all_steps(self):
        if self.execute_pos > 1:
            QMessageBox.information(self, "Remind", "Please exit the STEP condition first and retry")
            return 0
        elif not self.comment_check():
            return 0
        token_list, err_list = self.exe_lexer()
        for i in range(1, self.input_row+1):
            self.show_err_list(i, err_list)
        self.status_bar_change(8)
        self.textout.setText('')
        self.show_token_list(1, self.input_row, token_list)
        self.open_textedit()


    '''
    function: flag the single step or many steps into the lexer operation and show it onto the textEdit
              update the self.execute_pos and find the ERROR about modifying
    '''
    def highlight_execute_step(self, highlight=Qt.red):
        cnt = 0
        tmp_text = self.textEdit.toPlainText()

        vertical_bar = self.textEdit.verticalScrollBar().value()
        self.textEdit.setText('')

        for i in range(len(tmp_text)):
            if cnt == self.execute_pos-1:
                self.textEdit.setTextColor(highlight)
            else:
                self.textEdit.setTextColor(Qt.black)
            self.textEdit.insertPlainText(tmp_text[i])
            if tmp_text[i] == '\n':
                cnt += 1
        self.execute_pos += 1
        self.textEdit.verticalScrollBar().setValue(vertical_bar)
        return 1

    '''
    function: enter debug condition and change the surface
    '''
    def enter_step(self):
        wait(TIME_GAP)
        self.switch_pic('debug1.jpg')
        self.change_bg_text('debug1.jpg')
        wait(TIME_GAP)
        self.switch_pic('debug2.jpg')
        self.change_bg_text('debug2.jpg')
        wait(TIME_GAP)
        self.switch_pic('debug3.jpg')
        self.change_bg_text('debug3.jpg')
        wait(TIME_GAP)
        self.switch_pic('debug.jpg')
        self.change_bg_text('debug.jpg')

    '''
    function: exit debug condition and change the surface
    '''
    def exit_step(self):
        wait(TIME_GAP)
        self.switch_pic('debug3.jpg')
        self.change_bg_text('debug3.jpg')
        wait(TIME_GAP)
        self.switch_pic('debug2.jpg')
        self.change_bg_text('debug2.jpg')
        wait(TIME_GAP)
        self.switch_pic('debug1.jpg')
        self.change_bg_text('debug1.jpg')
        wait(TIME_GAP)
        self.switch_pic('bg.jpg')
        self.change_bg_text('bg.jpg')

    '''
    function: make the color of input text and textout text return black
    '''
    def input_text_return_black(self, message, textout_message):
        vertical_bar = self.textEdit.verticalScrollBar().value()
        self.textEdit.setTextColor(Qt.black)
        self.textEdit.setText(message)
        self.textEdit.verticalScrollBar().setValue(vertical_bar)
        textout_vertical_bar = self.textout.verticalScrollBar().value()
        self.textout.setTextColor(Qt.black)
        self.textout.setText(textout_message)
        self.textout.verticalScrollBar().setValue(textout_vertical_bar)

    '''
    function: stop the operation of step process
    '''
    def stop_step_op(self):
        if self.execute_pos == 1:
            QMessageBox.information(self, "Remind", "You have not been into the step operation")
            return
        self.exit_step()
        self.input_text_return_black(self.textEdit.toPlainText(), self.textout.toPlainText())    #the origin content may be changed
        self.execute_pos = 1
        self.status_bar_change(6)
        self.textout.setText('')

    '''
    function: switch the background of window
    '''
    def switch_pic(self, path):
        window_bg = QtGui.QPalette()
        window_bg.setBrush(QPalette.Background, QtGui.QBrush(QtGui.QPixmap(path)))
        self.mainwindow.setPalette(window_bg)

    '''
    function: change the bg of textEdit and textBrowser
    '''
    def change_bg_text(self, path):
        self.textEdit.setStyleSheet('background-image:url(' + path + ')')
        self.textBrowser.setStyleSheet('background-image:url(' + path + ')')
        self.textout.setStyleSheet('background-image:url(' + path + ')')


    '''
    function: show the tokenlist content from row1 to row2 on self.textout
    '''
    def show_token_list(self, row1, row2, tokenlist):
        match_str_low = 'position=' + str(row1) + ':'
        match_str_high = 'position=' + str(row2) + ':'
        lower = -1
        higher = -1
        # lower can be assigned once while higher can be assigned many times
        i = 0
        for i in range(len(tokenlist)):
            if str(tokenlist[i]).rfind(match_str_low) != -1 and lower == -1:
                lower = i
            if str(tokenlist[i]).rfind(match_str_high) != -1:
                higher = i

        if lower == higher and lower == -1:
            ''' can't find fit condition'''
            return
        if lower == higher and lower == 0:
            higher = len(tokenlist) - 1
        for i in range(lower, higher+1):
            self.textout.append(str(tokenlist[i]))

    '''
    function: show the err_list content about row on self.textBrowser
    '''
    def show_err_list(self, row, err_list):
        match_str = 'line: ' + str(row) + ' column'
        lower = -1
        higher = -1
        for i in range(1, len(err_list), 2):
            if str(err_list[i]).rfind(match_str) != -1 and lower == -1:
                lower = i-1
            if str(err_list[i]).rfind(match_str) != -1:
                higher = i-1
        if lower == higher and lower == -1:
            return
        for i in range(lower, higher+1, 2):
            self.textBrowser.append(str(err_list[i]) + ' ' + str(err_list[i+1]))

    '''
    function: execute the Lexer process, obtain the err_list and token_list
    '''
    def exe_lexer(self):
        self.Lexer = Lexer(self.lexer_content)
        token_list = self.Lexer.get_all_tokens()
        err_list = self.Lexer.getErrList()
        return token_list, err_list

    '''
    function: do all of the parser process
    '''
    def parser_process(self):
        if self.execute_pos > 1:
            QMessageBox.information(self, "Remind", "Please exit the STEP condition first and retry")
            return 0
        elif not self.comment_check():
            return 0
        token_list, err_list = self.exe_lexer()
        for i in range(1, self.input_row + 1):
            self.show_err_list(i, err_list)
        self.status_bar_change(8)


        if len(err_list):
            return 0
        self.Parser = Parse()
        self.Parser.parse_process(token_list)
        parse_err_list = self.Parser.get_err_list()

        if len(parse_err_list):
            for i in parse_err_list:
                self.textBrowser.append(i)
            self.status_bar_change(12)
            QMessageBox.critical(self, 'Wrong', 'Parser Process failed, please correct and retry')
            return 0

        self.status_bar_change(11)
        self.textout.setText('')
        self.show_token_list(1, self.input_row, token_list)
        self.open_textedit()
        my_parser_tree = MyParserTree('ParseTree.png', self.mainwindow)
        my_parser_tree.show()
        return 1

    '''
    function: do all of the intermediate-code-generation process
    '''
    def gen_inter_process(self):
        if self.execute_pos > 1:
            QMessageBox.information(self, "Remind", "Please exit the STEP condition first and retry")
            return 0
        elif not self.comment_check():
            return 0
        token_list, err_list = self.exe_lexer()
        for i in range(1, self.input_row + 1):
            self.show_err_list(i, err_list)
        self.status_bar_change(8)


        if len(err_list):
            return 0
        self.Parser = Parse()
        self.Parser.parse_process(token_list)

        if len(self.Parser.get_err_list()):
            for i in self.Parser.get_err_list():
                self.textBrowser.append(i)
            self.status_bar_change(12)
            QMessageBox.critical(self, 'Wrong', 'Parser Process failed, please correct and retry')
            return 0

        if len(self.Parser.semantic_analyser.get_err_list()):
            for i in self.Parser.semantic_analyser.get_err_list():
                self.textBrowser.append(i)
            self.status_bar_change(13)
            QMessageBox.critical(self, 'Wrong', 'Semantic Process failed, please correct and retry')
            return 0

        self.status_bar_change(11)
        self.textout.setText('')
        self.show_token_list(1, self.input_row, token_list)
        self.open_textedit()
        my_parser_tree = MyParserTree('ParseTree.png', self.mainwindow)
        my_parser_tree.show()

        myinter = Myinter_Code(self.Parser.semantic_analyser.get_emit_code(), self.mainwindow)
        myinter.show()
        self.status_bar_change(14)
        return 1

    '''
    function: do all of the object-code-generation process
    '''
    def gen_object_code(self):
        if not self.gen_inter_process():
            return
        target = TARGET(self.Parser.semantic_analyser.get_emit_code(), self.Parser.semantic_analyser.var_table, self.Parser.semantic_analyser.info_table)

        with open("object.asm", "w") as f:
            for i in target.get_object_code():
                print(i, end='\n', file=f)
        self.status_bar_change(15)
        QMessageBox.information(self, "Info", "The .ASM file is generated successfully, please check in object.asm")
        return

    '''
    function : save the information in self.textEdit
    '''
    def save_information(self):
        if self.textEdit.toPlainText() == '':
            QMessageBox.information(self, "Remind", "You have not load the content in the text window")
            return
        if self.execute_pos > 1:
            QMessageBox.information(self, "Remind", "Please exit the STEP condition first and retry")
            return
        ok = False
        file_path, ok = QFileDialog.getOpenFileName(self, "Choose File", '', 'C-Files(*.*)')
        if not ok:
            return
        try:
            file = open(file_path, 'w', encoding='utf-8')
        except:
            QMessageBox.critical(self, 'Wrong', " can't open the file successfully")
            return
        file.write(self.textEdit.toPlainText())
        file.close()
        self.status_bar_change(10)


if __name__ =='__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.show()
    my = MyCompile(MainWindow)
    sys.exit(app.exec_())