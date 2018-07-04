import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import functools
import sys
sys.path.append('../')
from globals import *
from context_free_grammar import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5 import *
from tests.read_tests_files import ReadTestsFiles
hey = "haha"

'''
	Autoria: Adriano Tosetto, Giulio Simão
'''

class FileParser:

	@staticmethod
	def get_grammars_from_file(filename):
		grammars_obj = []
		file = open(filename)
		rawstr = file.read()

		rawgrammars = rawstr.split("new_grammar")
		rawgrammars = rawgrammars[1:len(rawgrammars)]
		for rawgrammar in rawgrammars:
			rawgrammar = ''.join((rawgrammar.strip(), '\n'))
			rawgrammar_temp1 = rawgrammar.split('\n', 1)
			#print(rawgrammar_temp1[0])
			grammars_obj.append(ReadTestsFiles.raw_string_to_grammar(rawgrammar_temp1[1], rawgrammar_temp1[0][0:len(rawgrammar_temp1[0])-1]))
			print(rawgrammar_temp1[0])
		return grammars_obj
	@staticmethod
	def save_grammars_to_file(filename, grammars):
		open(filename, 'w').close()
		f = open(filename, "+a")
		for grammar in grammars:
			str_grammar = str(grammar)
			str_grammar = ("\nnew_grammar\n"+grammar.name+":\n" + str_grammar).strip() + '\n'
			print(grammar.name)
			f.write(str_grammar)

class MainWindow(QWidget):
	jesus = "-"
	jesus1 = "-"
	logtxt = ""
	def __init__(self):
		self.app = QApplication(sys.argv)
		super().__init__()
		self.resize(1200, 800)
		self.move(300, 300)
		self.setWindowTitle('Simple')
		self.show()

		self.leftSide = QWidget()
		self.rightSide = QWidget()
		self.leftSide.setStyleSheet("background-color:#404040;")
		self.rightSide.setStyleSheet("background-color:silver;")
		self.displayScreen = QWidget()
		self.editPanel = QWidget()
		self.displayScreen.setStyleSheet("background-color:light-gray;")
		self.editPanel.setStyleSheet("background-color:silver;")
		self.rightLayout = QGridLayout()
		self.rightLayout.addWidget(self.displayScreen, 0, 0)
		#self.rightLayout.addWidget(self.editPanel, 0, 1)
		self.center = QWidget()
		self.centerLayout = QGridLayout()
		self.centerLayout.addWidget(self.center, 0, 0)
		self.centerLayout.setRowStretch(0,5)
		self.centerLayout.setRowStretch(1,3)
		self.display = QTextEdit()
		self.display.setDisabled(True)
		self.display.setText('Selecione uma GLC')
		self.display.setStyleSheet("background-color:white;")
		self.displayLayout = QVBoxLayout()
		self.displayLayout.addWidget(self.display)
		self.log = QTextEdit()
		self.log.setText('')
		self.log.setStyleSheet("background-color:white;")
		self.logLayout = QVBoxLayout()
		self.logLayout.addWidget(self.log)
		self.centerLayout.addWidget(self.display,0,0)
		self.centerLayout.addWidget(self.log,1,0)
		self.displayScreen.setLayout(self.centerLayout)

		Globals.selected = Grammar([])

		self.MyTableWidget = MyTableWidget(self.rightSide)
		self.MyTableWidget.tab1.updateGR.connect(self.update_grammar)
		self.MyTableWidget.tab1.addGR.connect(self.update_gr)
		self.rightLayout.addWidget(self.MyTableWidget,0,1)
		self.rightSide.setLayout(self.rightLayout)
		self.rightLayout.setColumnStretch(0,3)
		self.rightLayout.setColumnStretch(1,2)

		self.generateLeftSide()
		self.initialize()



		self.mainLayout = QGridLayout()
		self.mainLayout.setColumnStretch(0, 1)
		self.mainLayout.setColumnStretch(1, 3)
		self.mainLayout.addWidget(self.leftSide,0,0)
		self.mainLayout.addWidget(self.rightSide,0,1)
		self.setLayout(self.mainLayout)
		self.leftSide.setLayout(self.leftLayout)
		self.show()
		sys.exit(self.app.exec_())

	@pyqtSlot()
	def log_update(self):
		self.log.setText(self.MyTableWidget.tab4.jesus)
	def log_sentences(self):
		self.log.setText(MainWindow.logtxt)
	def on_click(self):
		print('PyQt5 button click')
	def showAFs(self):
		self.erList.setHidden(True)
		self.grList.setHidden(True)
		self.afList.setHidden(False)
		Globals.displayed = 3
	def showGRs(self):
		self.erList.setHidden(True)
		self.afList.setHidden(True)
		self.grList.setHidden(False)
		Globals.displayed = 1
	def showERs(self):
		self.grList.setHidden(True)
		self.afList.setHidden(True)
		self.erList.setHidden(False)
		Globals.displayed = 2
	def select_grammar(self, gram):
		self.update_gr()
		self.display.setText(gram.name + ":\n" + str(gram))
		self.log.setText(str(gram))
		Globals.selected = gram
		nts = gram.get_non_terminals()
		prods = []
		for nt in nts:
			nt_productions = gram.prod_dict[nt]
			for prod in nt_productions:
				prods.append(Production(nt, prod))
		self.MyTableWidget.update(nts, prods, gram.name)
	def addStuff(self):
		self.add_gr()
	def update_stuff(self):
		self.update_gr()
	def deleteStuff(self):
		grams = []
		for g in Globals.grammars:
			if g.name != Globals.selected.name:
				grams.append(g)
		Globals.grammars = grams
		self.update_gr()
		self.display.setText('')
		Globals.selected = None
	def initialize(self):
		Globals.grammars = FileParser.get_grammars_from_file("../tests/bd.txt")
		self.add_gr()
	def add_gr(self):
		newG = Grammar([Production('S', '&')])
		names = [gr.name for gr in Globals.grammars]
		while newG in Globals.grammars:
			for name in names:
				if newG.name == name:
					newG.name += "'"
					break
		Globals.grammars.append(newG)
		Globals.selected = newG
		self.select_grammar(Globals.selected)

	def update_grammar(self, gName):
		newG = ReadTestsFiles.raw_string_to_grammar(self.log.toPlainText())
		newG.name = gName
		grams = []
		for g in Globals.grammars:
			if g.name != Globals.selected.name:
				grams.append(g)
			else:
				grams.append(newG)
		Globals.grammars = grams
		Globals.selected = newG
		self.update_gr()
		self.select_grammar(newG)
	def update_gr(self):
		self.grList.clear()
		for g in Globals.grammars:
			item = QListWidgetItem(self.grList)
			item_widget = GrammarButton(g.name, g)
			item_widget.clicked.connect(functools.partial(self.select_grammar, g))
			self.grList.setItemWidget(item, item_widget)
			self.grList.addItem(item)
	def saveContext(self):
		FileParser.save_grammars_to_file("../tests/bd.txt", Globals.grammars)

	def generateRightSide(self):
		self.optionsGR = QWidget()
	def generateLeftSide(self):
		self.options = QWidget()
		self.listofentities = QWidget()
		self.options.setStyleSheet("background-color:silver;")
		self.listofentities.setStyleSheet("background-color:silver;")
		self.leftLayout = QGridLayout()
		self.leftLayout.setRowStretch(0, 3)
		self.leftLayout.setRowStretch(1, 30)
		self.leftLayout.addWidget(self.options,0,0)
		self.leftLayout.addWidget(self.listofentities,1,0)

		self.optionAdd = QWidget()
		self.optionDelete = QWidget()
		self.optionSave = QWidget()
		self.optionAdd.setStyleSheet("background-color:silver;")
		self.optionDelete.setStyleSheet("background-color:silver;")
		self.optionSave.setStyleSheet("background-color:silver;")
		self.optionsLayout = QGridLayout()
		self.optionsLayout.setColumnStretch(0,1)
		self.optionsLayout.setColumnStretch(1,1)
		self.optionsLayout.setColumnStretch(2,1)
		self.optionsLayout.addWidget(self.optionAdd,0,0)
		self.optionsLayout.addWidget(self.optionDelete,0,1)
		self.optionsLayout.addWidget(self.optionSave,0,2)
		self.options.setLayout(self.optionsLayout)

		self.addButton = QPushButton('Adicionar', self)
		self.addButton.setToolTip('Adicionar GLC')
		self.addButton.clicked.connect(self.addStuff)
		self.addLayout = QVBoxLayout()
		self.addLayout.addWidget(self.addButton)
		self.optionAdd.setLayout(self.addLayout)

		self.deleteButton = QPushButton('Deletar', self)
		self.deleteButton.setToolTip('Deletar GLC')
		self.deleteButton.clicked.connect(self.deleteStuff)
		self.deleteLayout = QVBoxLayout()
		self.deleteLayout.addWidget(self.deleteButton)
		self.optionDelete.setLayout(self.deleteLayout)

		self.saveButton = QPushButton('Gravar', self)
		self.saveButton.setToolTip('Gravar GLCs em um arquivo ;^)')
		self.saveButton.clicked.connect(self.saveContext)
		self.saveLayout = QVBoxLayout()
		self.saveLayout.addWidget(self.saveButton)
		self.optionSave.setLayout(self.saveLayout)

		self.grList = QListWidget(self)
		self.afList = QListWidget(self)
		self.erList = QListWidget(self)
		self.listLayout = QVBoxLayout()
		self.listLayout.addWidget(self.grList)
		self.update_gr()
		self.listofentities.setLayout(self.listLayout)

class GrammarButton(QPushButton):
	def __init__(self, QString, grammar):
		self.grammar = grammar
		super().__init__(QString)

class AutomatonButton(QPushButton):
	def __init__(self, QString, automaton):
		self.automaton = automaton
		super().__init__(QString)


class MyTableWidget(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		self.layout = QVBoxLayout(self)
		self.tabs = QTabWidget()
		self.tab1 = addGrammarTab(["S"], [["&"]], "G1")

		self.tabs.addTab(self.tab1,"")

        #self.tab1.layout = QVBoxLayout(self)
        #self.pushButton1 = QPushButton("PyQt5 button")
        #self.tab1.layout.addWidget(self.pushButton1)
        #self.tab1.setLayout(self.tab1.layout)

		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)
	def update(self, nts, prods, name):
		print(nts)
		print(prods)
		self.nt_line_edit = nts
		self.nt_line_prod = prods
		self.new_gr_name = name
		self.tab1.setProdWidgets(self.new_gr_name)
		#self.tab1.line = len(nts)
		print("auhauhaua=", end="")
		print(self.tab1.line)
	@pyqtSlot()
	def on_click(self):
		print("\n")
		for currentQTableWidgetItem in self.tableWidget.selectedItems():
			print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class addGrammarTab(QWidget):
	updateGR = QtCore.pyqtSignal(str)
	addGR = QtCore.pyqtSignal(Grammar)
	def __init__(self, listNT = None, listProd=None, nameGR = ''):
		super(QWidget, self).__init__()
		self.nt_line_edit = listNT # nao-terminais da gramatica
		self.arrow_labels = [] # nao esta sendo usado
		self.prod_nt_line_edit = listProd # producoes do nao-terminal correspondente
		self.remv_prods_button = [] # nao esta sendo usado
		self.new_gr_name = nameGR

		self.line = 0
		self.layout = QGridLayout()
		self.top_layout = QGridLayout()
		self.top_layout.setColumnStretch(0,1)
		self.top_layout.setColumnStretch(1,1)
		self.top_layout.setColumnStretch(2,6)
		self.top_layout.setColumnStretch(3,1)
		self.setProdWidgets(self.new_gr_name)
		self.top = QWidget()
		self.top.setLayout(self.top_layout)
		self.sarea = QScrollArea()
		self.sarea.setWidget(self.top)
		self.sarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.sarea.setWidgetResizable(True)
		self.bottom_layout = QGridLayout()
		self.add_grammar = QPushButton("Save grammar")
		self.add_prod    = QPushButton("Make proper")
		self.remove_left = QPushButton("Remove left recursion")
		self.add_prod.clicked.connect(self.add_production)
		self.add_grammar.clicked.connect(self.save_grammar)
		self.remove_left.clicked.connect(self.remove_recursion)
		self.setPolicyButtons()
		self.bottom_layout.addWidget(self.add_grammar, 0, 0)
		self.bottom_layout.addWidget(self.add_prod, 0, 1)
		self.bottom_layout.addWidget(self.remove_left, 0, 2)
		self.bottom = QWidget()
		self.bottom.setLayout(self.bottom_layout)
		self.bottom.setStyleSheet("background-color:silver;")

		self.layout.addWidget(self.sarea,0,0)
		self.layout.addWidget(self.bottom,1,0)

		self.layout.setRowStretch(0,9)
		self.layout.setRowStretch(1,1)
		self.setLayout(self.layout)

	def remove_recursion(self):
		newG = Globals.selected.remove_left_recursion()
		gName = newG.name
		i=0
		while Grammar([], gName) in Globals.grammars:
			i+=1
			gName = newG3.name + str(i)
		Globals.grammars.append(newG)
		self.addGR.emit(newG)
	def setProdWidgets(self, gName):
		for i in reversed(range(self.top_layout.count())):
			self.top_layout.itemAt(i).widget().setParent(None)
		self.new_gr_name = gName
		self.top_layout.addWidget(QLabel("Nome:"), 0, 0)
		self.top_layout.addWidget(QLineEdit(gName), 0, 1)

		self.top_layout.addWidget(QLabel("Vazia?"), 1, 0)
		self.top_layout.addWidget(QLabel(str(Globals.selected.isEmpty())), 1, 1)

		self.top_layout.addWidget(QLabel("Finita?"), 2, 0)
		self.top_layout.addWidget(QLabel(str(Globals.selected.isFinite())), 2, 1)

		self.top_layout.addWidget(QLabel("N_F:"), 3, 0)
		self.top_layout.addWidget(QLabel(str(Globals.selected.get_NF())), 3, 1)

		self.top_layout.addWidget(QLabel("V_i:"), 4, 0)
		self.top_layout.addWidget(QLabel(str(Globals.selected.get_VI())), 4, 1)

		self.top_layout.addWidget(QLabel("N_e:"), 5, 0)
		self.top_layout.addWidget(QLabel(str(Globals.selected.getNE())), 5, 1)

		i = 6

		for nt in Globals.selected.get_non_terminals():
			self.top_layout.addWidget(QLabel("N("+nt+"):"), i, 0)
			self.top_layout.addWidget(QLabel(str(Globals.selected.get_NA(nt))), i, 1)
			i+=1

		for nt in Globals.selected.get_non_terminals():
			self.top_layout.addWidget(QLabel("FIRST("+nt+"):"), i, 0)
			self.top_layout.addWidget(QLabel(str(Globals.selected.getFirst(nt))), i, 1)
			i+=1

		for nt in Globals.selected.get_non_terminals():
			self.top_layout.addWidget(QLabel("FOLLOW("+nt+"):"), i, 0)
			self.top_layout.addWidget(QLabel(str(Globals.selected.getFollow(nt))), i, 1)
			i+=1

		for nt in Globals.selected.get_non_terminals():
			self.top_layout.addWidget(QLabel("FIRST-NT("+nt+"):"), i, 0)
			self.top_layout.addWidget(QLabel(str(Globals.selected.getFirstNT(nt))), i, 1)
			i+=1

		self.top_layout.addWidget(QLabel("Fatorada?"), i, 0)
		self.top_layout.addWidget(QLabel(str(Globals.selected.is_factored())), i, 1)
		i+=1

		self.top_layout.addWidget(QLabel("Possui RE?"), i, 0)
		self.top_layout.addWidget(QLabel(str(Globals.selected.detect_all_left_recursion_for_all())), i, 1)
		i+=1

		if Globals.selected.detect_all_left_recursion_for_all():
			for nt in Globals.selected.get_non_terminals():
				if Globals.selected.detect_all_left_recursion(nt):
					self.top_layout.addWidget(QLabel("RE por "+nt+":"), i, 0)
					if Globals.selected.detect_direct_left_recursion(nt) and not Globals.selected.detect_indirect_left_recursion(nt):
						self.top_layout.addWidget(QLabel("direta"), i, 1)
					elif not Globals.selected.detect_direct_left_recursion(nt) and Globals.selected.detect_indirect_left_recursion(nt):
						self.top_layout.addWidget(QLabel("indireta"), i, 1)
					elif Globals.selected.detect_direct_left_recursion(nt) and Globals.selected.detect_indirect_left_recursion(nt):
						self.top_layout.addWidget(QLabel("direta e indireta"), i, 1)
					i+=1

	def get_productions(self):
		newNT = []
		newProd = []
		for i in range(1, self.line):
			newNT.append(self.top_layout.itemAtPosition(i,0).widget().text())
		for i in range(1, self.line):
			prodByNT = []
			prod = ''
			for c in self.top_layout.itemAtPosition(i,2).widget().text():
				if c is '|':
					prodByNT.append(prod)
					prod = ''
					continue
				elif c is ' ':
					continue
				prod = prod + c
			prodByNT.append(prod)
			newProd.append(prodByNT)

		self.nt_line_edit = newNT
		self.prod_nt_line_edit = newProd
	def setPolicyButtons(self):
		self.add_grammar.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.add_prod.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.remove_left.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
	def add_production(self):
		newG = Globals.selected.make_epsilon_free()
		print(newG)
		newG1 = newG.remove_simple_productions()
		print(newG1)
		newG2 = newG1.remove_infertile_symbols()
		print(newG2)
		newG3 = newG2.remove_unreachable_symbols()
		print(newG3)
		newG3.name = Globals.selected.name + " (proper)"
		grams = []
		i = 0
		gName = newG.name + str(i)
		while Grammar([], gName) in Globals.grammars:
			i+=1
			gName = newG.name + str(i)
		Globals.grammars.append(newG)
		gName = newG1.name + str(i)
		while Grammar([], gName) in Globals.grammars:
			i+=1
			gName = newG1.name + str(i)
		Globals.grammars.append(newG1)
		gName = newG2.name + str(i)
		while Grammar([], gName) in Globals.grammars:
			i+=1
			gName = newG2.name + str(i)
		Globals.grammars.append(newG2)
		gName = newG3.name + str(i)
		while Grammar([], gName) in Globals.grammars:
			i+=1
			gName = newG3.name + str(i)
		Globals.grammars.append(newG3)
		self.addGR.emit(newG)
		self.addGR.emit(newG1)
		self.addGR.emit(newG2)
		self.addGR.emit(newG3)
		#self.line+=1
	def remove_prod_button_clicked(self, line):
		#if len(Globals.selected.productions) <= 1:
			#return None
		print("linha = " + str(line))
		print(self.nt_line_edit.pop(line))
		print(self.prod_nt_line_edit.pop(line))
		#print(self.nt_line_edit)
		#print(self.prod_nt_line_edit)
		self.setProdWidgets(self.nt_line_edit, self.prod_nt_line_edit, self.new_gr_name)

	def save_grammar(self):
		gName = self.top_layout.itemAtPosition(0,1).widget().text()
		grams = []
		i = 0
		if gName == '':
			gName = "G" + str(i)
			while Grammar([], gName) in Globals.grammars:
				i+=1
				gName = "G" + str(i)
		self.updateGR.emit(gName)
		self.setProdWidgets(gName)
		'''
			aqui voce pega tudo o que esta escrito nas caixas de texto e atualiza o
			self.nt_line_edit e self.nt_line_prod e adiciona a gramatica que foi colocada.
			Precisa do QLineEdit para o nome da gramatica. Pensei em fazer o seguinte: se o nome nao
			estiver na lista de gramaticas, ele salva uma nova. Se estiver, ele atualiza.
			A gramatica seleciona aparece na edição assim que ocorrer o click
		'''
		print('saving')

class RemoveProdButton(QPushButton):
	def __init__(self, text, line):
		super().__init__(text)
		self.line = line

if __name__ == "__main__":
	m = MainWindow()
