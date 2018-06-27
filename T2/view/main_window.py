import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import functools
import sys
sys.path.append('../')
#from globals import *
#import context_free_grammar
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5 import *
hey = "haha"

'''
	Autoria: Adriano Tosetto, Giulio Simão
'''

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
		self.rightSide.setStyleSheet("background-color:gray;")
		self.displayScreen = QWidget()
		self.editPanel = QWidget()#addGrammarTab(["S"], [["&"]], "G1")
		self.displayScreen.setStyleSheet("background-color:light-gray;")
		self.editPanel.setStyleSheet("background-color:light-gray;")
		self.rightLayout = QGridLayout()
		self.rightLayout.addWidget(self.displayScreen, 0, 0)
		#self.rightLayout.addWidget(self.editPanel, 0, 1)
		self.MyTableWidget = MyTableWidget(self.rightSide)
		self.rightLayout.addWidget(self.editPanel, 0, 1)
		self.rightLayout.setColumnStretch(0,5)
		self.rightLayout.setColumnStretch(1,2)
		self.generateLeftSide()

		self.center = QWidget()
		self.centerLayout = QGridLayout()
		self.centerLayout.addWidget(self.center, 0, 0)
		self.centerLayout.setRowStretch(0,5)
		self.centerLayout.setRowStretch(1,3)
		self.display = QTextEdit()
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
	'''def select_grammar(self, gram):
		self.update_gr()
		self.display.setText(gram.name + ":\n" + str(gram))
		Globals.selected = gram
		nts = gram.get_non_terminals()
		prods = []
		for nt in nts:
			prods.append(gram.get_productions_from(nt))
		self.MyTableWidget.update(nts, prods, gram.name)
	def deleteStuff(self):
		grams = []
		for g in Globals.grammars:
			if g.name != Globals.selected.name:
				grams.append(g)
		Globals.grammars = grams
		self.update_gr()
		self.display.setText('')
		Globals.selected = None'''
	def add_gr(self):
		newG = Grammar({Production('S', '&')})
		names = [gr.name for gr in Globals.grammars]
		while newG in Globals.grammars:
			for name in names:
				if newG.name == name:
					newG.name += "'"
					break
		Globals.grammars.append(newG)
		Globals.selected = newG
		self.update_gr()

	'''def update_gr(self):
		self.grList.clear()
		for g in Globals.grammars:
			item = QListWidgetItem(self.grList)
			item_widget = GrammarButton(g.name, g)
			item_widget.clicked.connect(functools.partial(self.select_grammar, g))
			self.grList.setItemWidget(item, item_widget)
			self.grList.addItem(item)'''

	def generateRightSide(self):
		self.optionsAF = QWidget()
		self.optionsGR = QWidget()
		self.optionsER = QWidget()
		self.afLayout = QGridLayout()
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
		self.optionAdd.setStyleSheet("background-color:silver;")
		self.optionDelete.setStyleSheet("background-color:silver;")
		self.optionsLayout = QGridLayout()
		self.optionsLayout.setColumnStretch(0,1)
		self.optionsLayout.setColumnStretch(1,1)
		self.optionsLayout.addWidget(self.optionAdd,0,0)
		self.optionsLayout.addWidget(self.optionDelete,0,1)
		self.options.setLayout(self.optionsLayout)

		self.addButton = QPushButton('Adicionar', self)
		self.addButton.setToolTip('Adicionar GLC')
		#self.addButton.clicked.connect(self.addStuff)
		self.addLayout = QVBoxLayout()
		self.addLayout.addWidget(self.addButton)
		self.optionAdd.setLayout(self.addLayout)

		self.deleteButton = QPushButton('Deletar', self)
		self.deleteButton.setToolTip('Deletar GLC')
		#self.deleteButton.clicked.connect(self.deleteStuff)
		self.deleteLayout = QVBoxLayout()
		self.deleteLayout.addWidget(self.deleteButton)
		self.optionDelete.setLayout(self.deleteLayout)

		self.grList = QListWidget(self)
		self.listLayout = QVBoxLayout()
		self.listLayout.addWidget(self.grList)
		#self.update_gr()
		self.listofentities.setLayout(self.listLayout)

		#self.add_gr()

if __name__ == "__main__":
	m = MainWindow()

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
		self.tabs.resize(300,200)

		self.tabs.addTab(self.tab1,"Edit GLC")

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
		self.tab1.setProdWidgets(self.nt_line_edit, self.nt_line_prod, self.new_gr_name)
		#self.tab1.line = len(nts)
		print("auhauhaua=", end="")
		print(self.tab1.line)
	@pyqtSlot()
	def on_click(self):
		print("\n")
		for currentQTableWidgetItem in self.tableWidget.selectedItems():
			print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class addGrammarTab(QWidget):
	updateGR = QtCore.pyqtSignal(Grammar)
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
		self.setProdWidgets(self.nt_line_edit, self.prod_nt_line_edit, self.new_gr_name)
		self.top = QWidget()
		self.top.setLayout(self.top_layout)
		self.sarea = QScrollArea()
		self.sarea.setWidget(self.top)
		self.sarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.sarea.setWidgetResizable(True)
		self.bottom_layout = QGridLayout()
		self.add_grammar = QPushButton("Save grammar")
		self.add_prod    = QPushButton("Add prod")
		self.add_prod.clicked.connect(self.add_production)
		self.add_grammar.clicked.connect(self.save_grammar)
		self.setPolicyButtons()
		self.bottom_layout.addWidget(self.add_grammar, 0, 0)
		self.bottom_layout.addWidget(self.add_prod, 0, 1)
		self.bottom = QWidget()
		self.bottom.setLayout(self.bottom_layout)
		self.bottom.setStyleSheet("background-color:silver;")

		self.layout.addWidget(self.sarea,0,0)
		self.layout.addWidget(self.bottom,1,0)

		self.layout.setRowStretch(0,9)
		self.layout.setRowStretch(1,1)
		self.setLayout(self.layout)
	def setProdWidgets(self, listNT, listProd, gName):
		if len(listNT) < 1 or len(listProd) < 1:
			return None
		for p in listProd:
			if len(p) < 1:
				return None
		self.nt_line_edit = listNT
		self.prod_nt_line_edit = listProd
		self.new_gr_name = gName
		for i in reversed(range(self.top_layout.count())):
		    self.top_layout.itemAt(i).widget().setParent(None)
		self.top_layout.addWidget(QLabel("Nome:"), 0, 0)
		self.top_layout.addWidget(QLineEdit(gName), 0, 1)
		i = 1
		self.nt_line_edit = listNT
		self.prod_nt_line_edit = listProd
		for nt in listNT:
			p = QLineEdit(nt)
			#p.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
			self.top_layout.addWidget(p, i, 0)

			strProd = ""
			for ii in range(0, len(listProd[i-1]) - 1):
				strProd += listProd[i-1][ii] + "|"
			strProd += listProd[i-1][len(listProd[i-1]) - 1]
			p1 = QLineEdit(strProd)
			#p1.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)

			self.top_layout.addWidget(p1,i, 2)

			label_arrow = QLabel("->")
			self.top_layout.addWidget(label_arrow, i, 1)

			btn_remove = RemoveProdButton("Remover", i)
			print("nt = " + nt + " line " + str(i-1))
			btn_remove.clicked.connect(functools.partial(self.remove_prod_button_clicked, btn_remove.line))
			self.top_layout.addWidget(btn_remove, i, 3)
			i+=1
		self.line = i
		print("linhas " + str(self.line))
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
	def add_production(self):
		self.nt_line_edit.append("")
		self.prod_nt_line_edit.append([""])
		for i in reversed(range(self.top_layout.count())):
		    self.top_layout.itemAt(i).widget().setParent(None)
		self.setProdWidgets(self.nt_line_edit, self.prod_nt_line_edit, self.new_gr_name)
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
		if len(self.nt_line_edit) != len(self.prod_nt_line_edit):
			return None
		#print(self.nt_line_edit)
		#print(self.prod_nt_line_edit)
		newName = self.top_layout.itemAtPosition(0,1).widget().text()
		self.new_gr_name = newName
		self.get_productions()
		prods = []
		for i in range(0, len(self.nt_line_edit)):
			for p in self.prod_nt_line_edit[i]:
				if len(p) is 2:
					if p[-1] in self.nt_line_edit:
						prods.append(Production(self.nt_line_edit[i], p))
				else:
					prods.append(Production(self.nt_line_edit[i], p))
		grams = []
		if Grammar([], newName) in Globals.grammars:
			newG = Grammar(prods, Globals.selected.name)
		else:
			newG = Grammar(prods, newName)
		for g in Globals.grammars:
			if g.name != Globals.selected.name:
				grams.append(g)
			else:
				grams.append(newG)
		Globals.grammars = grams
		Globals.selected = newG
		self.updateGR.emit(Globals.selected)
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
	mw = MainWindow()
