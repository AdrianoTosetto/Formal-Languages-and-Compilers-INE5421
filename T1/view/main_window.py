import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import functools
import sys
sys.path.append('../')
from globals import *
from regular_grammar import *
from operations_with_grammars import *
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5 import *
from nd_add_automaton_tab import *
hey = "haha"

class MainWindow(QWidget):
	jesus = "-"
	jesus1 = "-"
	updateAFD = QtCore.pyqtSignal(Automaton)
	updateAFND = QtCore.pyqtSignal(NDAutomaton)
	def __init__(self):
		self.app = QApplication(sys.argv)
		super().__init__()
		self.resize(1200, 800)
		self.move(300, 300)
		self.setWindowTitle('Simple')
		self.show()

		self.leftSide = QWidget()
		self.rightSide = QWidget()
		self.leftSide.setStyleSheet("background-color:blue;")
		self.rightSide.setStyleSheet("background-color:red;")
		self.displayScreen = QWidget()
		self.editPanel = QWidget()
		self.displayScreen.setStyleSheet("background-color:purple;")
		self.editPanel.setStyleSheet("background-color:pink;")
		self.rightLayout = QGridLayout()
		self.rightLayout.addWidget(self.displayScreen, 0, 0)
		#self.rightLayout.addWidget(self.editPanel, 0, 1)
		self.rightLayout.setColumnStretch(0,5)
		self.rightLayout.setColumnStretch(1,3)
		self.MyTableWidget = MyTableWidget(self.rightSide)
		self.MyTableWidget.tab1.updateGR.connect(self.select_grammar)
		self.MyTableWidget.tab3.updateGR.connect(self.select_grammar)
		self.updateAFD.connect(self.MyTableWidget.tab2.showAutomaton)
		self.updateAFND.connect(self.MyTableWidget.tab4.showAutomaton)
		self.MyTableWidget.tab2.saveAF.connect(self.select_automaton)
		self.rightLayout.addWidget(self.MyTableWidget,0,1)
		self.rightSide.setLayout(self.rightLayout)

		self.generateLeftSide()

		self.center = QLabel()
		self.center.setText(str(Globals.grammars[0]))
		self.center.setStyleSheet("background-color:white;")
		self.centerLayout = QVBoxLayout()
		self.centerLayout.addWidget(self.center)
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
		self.center.setText(str(gram))
		Globals.selected = copy.deepcopy(gram)
		nts = gram.get_non_terminals()
		prods = []
		for nt in nts:
			prods.append(gram.get_productions_from(nt))
		self.MyTableWidget.update(nts, prods, gram.name)
	def select_automaton(self, aut):
		self.update_af()
		self.center.setText(str(aut))
		Globals.selected = copy.deepcopy(aut)
		if type(Globals.selected) == type(Automaton({}, {}, State(''))):
			self.updateAFD.emit(Globals.selected)
		else:
			self.updateAFND.emit(Globals.selected)
		'''nts = gram.get_non_terminals()
		prods = []
		for nt in nts:
			prods.append(gram.get_productions_from(nt))
		self.MyTableWidget.update(nts, prods)'''
	def addStuff(self):
		if Globals.displayed == 1:
			self.add_gr()
		elif Globals.displayed == 2:
			print("Adicionadas ERs")
		elif Globals.displayed == 3:
			self.add_af()
		else:
			print("Erro")
	def update_stuff(self):
		if Globals.displayed == 1:
			self.update_gr()
		elif Globals.displayed == 2:
			print("Atualizadas ERs")
		elif Globals.displayed == 3:
			self.update_af()
		else:
			print("Erro")
	def deleteStuff(self):
		if Globals.selected != None:
			if type(Globals.selected) == type(Grammar([])):
				grams = []
				for g in Globals.grammars:
					if g.name != Globals.selected.name:
						grams.append(g)
				Globals.grammars = grams
				self.update_gr()
			if type(Globals.selected) == type(Automaton([],[], State(""))):
				auts = []
				for a in Globals.automata:
					if a.name != Globals.selected.name:
						auts.append(a)
				Globals.automata = auts
				self.update_af()
		self.center.setText('')
		Globals.selected = None

	def add_gr(self):
		newG = Grammar([Production('S', '&')], add = True)
		Globals.selected = newG
		self.update_gr()

	def update_gr(self):
		self.grList.clear()
		for g in Globals.grammars:
			item = QListWidgetItem(self.grList)
			item_widget = GrammarButton(g.name, g)
			item_widget.clicked.connect(functools.partial(self.select_grammar, g))
			self.grList.setItemWidget(item, item_widget)
			self.grList.addItem(item)

	def add_af(self):
		q0 = State("q0", True)
		newM = Automaton([q0], [q0], q0, add = True)
		Globals.selected = newM
		self.update_af()

	def update_af(self):
		self.afList.clear()
		for a in Globals.automata:
			item = QListWidgetItem(self.afList)
			item_widget = AutomatonButton(a.name, a)
			item_widget.clicked.connect(functools.partial(self.select_automaton, a))
			self.afList.setItemWidget(item, item_widget)
			self.afList.addItem(item)

	def generateRightSide(self):
		self.optionsAF = QWidget()
		self.optionsGR = QWidget()
		self.optionsER = QWidget()

		self.afLayout = QGridLayout()
	def generateLeftSide(self):
		self.options = QWidget()
		self.entities = QWidget()
		self.listofentities = QWidget()
		self.options.setStyleSheet("background-color:green;")
		self.entities.setStyleSheet("background-color:brown;")
		self.listofentities.setStyleSheet("background-color:orange;")
		self.leftLayout = QGridLayout()
		self.leftLayout.setRowStretch(0, 3)
		self.leftLayout.setRowStretch(1, 4)
		self.leftLayout.setRowStretch(2, 30)
		self.leftLayout.addWidget(self.options,0,0)
		self.leftLayout.addWidget(self.entities,1,0)
		self.leftLayout.addWidget(self.listofentities,2,0)

		self.optionAdd = QWidget()
		self.optionEdit = QWidget()
		self.optionDelete = QWidget()
		self.optionAdd.setStyleSheet("background-color:indigo;")
		self.optionEdit.setStyleSheet("background-color:cyan;")
		self.optionDelete.setStyleSheet("background-color:fuchsia;")
		self.optionsLayout = QGridLayout()
		self.optionsLayout.setColumnStretch(0,1)
		self.optionsLayout.setColumnStretch(1,1)
		self.optionsLayout.setColumnStretch(2,1)
		self.optionsLayout.addWidget(self.optionAdd,0,0)
		self.optionsLayout.addWidget(self.optionEdit,0,1)
		self.optionsLayout.addWidget(self.optionDelete,0,2)
		self.options.setLayout(self.optionsLayout)

		self.addButton = QPushButton('Adicionar', self)
		self.addButton.setToolTip('Adicionar GR/ER/AF')
		self.addButton.clicked.connect(self.addStuff)
		self.addLayout = QVBoxLayout()
		self.addLayout.addWidget(self.addButton)
		self.optionAdd.setLayout(self.addLayout)

		self.editButton = QPushButton('Editar', self)
		self.editButton.setToolTip('Editar GR/ER/AF')
		self.editButton.clicked.connect(self.on_click)
		self.editLayout = QVBoxLayout()
		self.editLayout.addWidget(self.editButton)
		self.optionEdit.setLayout(self.editLayout)

		self.deleteButton = QPushButton('Deletar', self)
		self.deleteButton.setToolTip('Deletar GR/ER/AF')
		self.deleteButton.clicked.connect(self.deleteStuff)
		self.deleteLayout = QVBoxLayout()
		self.deleteLayout.addWidget(self.deleteButton)
		self.optionDelete.setLayout(self.deleteLayout)

		self.showGR = QWidget()
		self.showER = QWidget()
		self.showAF = QWidget()
		self.showGR.setStyleSheet("background-color:crimson;")
		self.showER.setStyleSheet("background-color:magenta;")
		self.showAF.setStyleSheet("background-color:darkgreen;")
		self.entitiesLayout = QGridLayout()
		self.entitiesLayout.setColumnStretch(0,1)
		self.entitiesLayout.setColumnStretch(1,1)
		self.entitiesLayout.setColumnStretch(2,1)
		self.entitiesLayout.addWidget(self.showGR,0,0)
		self.entitiesLayout.addWidget(self.showER,0,1)
		self.entitiesLayout.addWidget(self.showAF,0,2)
		self.entities.setLayout(self.entitiesLayout)

		self.grButton = QPushButton('GR', self)
		self.grButton.setToolTip('Exibir GRs')
		self.grButton.clicked.connect(self.showGRs)
		self.grLayout = QVBoxLayout()
		self.grLayout.addWidget(self.grButton)
		self.showGR.setLayout(self.grLayout)

		self.afButton = QPushButton('AF', self)
		self.afButton.setToolTip('Exibir AFs')
		self.afButton.clicked.connect(self.showAFs)
		self.afLayout = QVBoxLayout()
		self.afLayout.addWidget(self.afButton)
		self.showAF.setLayout(self.afLayout)

		self.erButton = QPushButton('ER', self)
		self.erButton.setToolTip('Exibir ERs')
		self.erButton.clicked.connect(self.showERs)
		self.erLayout = QVBoxLayout()
		self.erLayout.addWidget(self.erButton)
		self.showER.setLayout(self.erLayout)

		self.grList = QListWidget(self)
		self.afList = QListWidget(self)
		self.erList = QListWidget(self)
		self.listLayout = QVBoxLayout()
		self.listLayout.addWidget(self.grList)
		self.listLayout.addWidget(self.erList)
		self.listLayout.addWidget(self.afList)
		self.update_gr()
		self.update_af()
		self.grList.setHidden(True)
		self.afList.setHidden(True)
		self.erList.setHidden(True)
		self.listofentities.setLayout(self.listLayout)

		self.add_gr()

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
		self.tab2 = addAutomatonTab()
		self.tab3 = GrammarOperationsTab()
		self.tab4 = addNDAutomatonTab()
		self.tabs.resize(300,200)

		self.tabs.addTab(self.tab1,"Add GR")
		self.tabs.addTab(self.tab2,"Add AF")
		self.tabs.addTab(self.tab3,"GR Operations")
		self.tabs.addTab(self.tab4,"Add NAF")

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
		self.bottom.setStyleSheet("background-color:white;")

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


class addAutomatonTab(QWidget):
	saveAF = QtCore.pyqtSignal(Automaton)
	def __init__(self):
		super(QWidget,self).__init__()
		self.initial_state_radio_group = QButtonGroup()
		self.transition_table_ui = AutomatonTable() # layout transition table
		self.transition_table = TransitionTable() # real transition table
		self.layout = QGridLayout()
		self.transition_table_ui.setRowCount(1)
		self.transition_table_ui.setColumnCount(0)
		self.transition_table_ui.setAcceptDrops(True)
		self.transition_table_ui.setItem(0,0, StateTableItem("q0"))

		#self.transition_table_ui.move(0,0)


		self.add_automaton_button = QPushButton("Adicionar")
		self.create_transition_table_button = \
			QPushButton("Criar tabela") # botao para criar a tabela com o alfabeto inserido
		self.add_automaton_button.clicked.connect(self.save_automaton)
		self.bottom_layout = QGridLayout()
		self.bottom_layout.addWidget(self.create_transition_table_button,0,0)
		self.create_transition_table_button.clicked.connect(self.create_transition_table)
		self.bottom_layout.addWidget(self.add_automaton_button, 0,1)
		self.bottom_panel = QWidget()
		self.bottom_panel.setLayout(self.bottom_layout)

		self.top_layout = QGridLayout()
		self.add_remove_state_layout = QGridLayout()
		self.add_remove_panel = QWidget()
		self.top_panel = QWidget()
		self.edit_name = QLineEdit()
		self.edit_name.setDragEnabled(True)
		self.edit_alphabet = QLineEdit()
		self.list_symbol  = QListWidget()
		self.remove_symbol_button = QPushButton("Remover símbolo")
		self.remove_symbol_button.clicked.connect(self.remove_symbol)
		self.add_symbol_button = QPushButton("Adicionar símbolo")
		self.add_symbol_button.clicked.connect(self.add_new_symbol)
		self.add_remove_symbol_panel = QWidget()
		self.add_remove_symbol_layout = QGridLayout()
		self.add_remove_symbol_layout.addWidget(self.add_symbol_button, 0,0)
		self.add_remove_symbol_layout.addWidget(self.remove_symbol_button, 1, 0)
		self.add_remove_symbol_panel.setLayout(self.add_remove_symbol_layout)

		self.add_new_state = QPushButton("Adicionar estado")
		self.remove_state_button = QPushButton("Remover estado selecionado")
		self.add_remove_state_layout.addWidget(self.add_new_state, 0,0)
		self.add_remove_state_layout.addWidget(self.remove_state_button, 1, 0)
		self.add_remove_panel.setLayout(self.add_remove_state_layout)
		self.top_layout.addWidget(self.add_remove_symbol_panel, 0, 0)
		self.top_layout.addWidget(self.list_symbol, 0, 1)
		self.top_layout.addWidget(self.add_remove_panel, 1,0)
		self.setPolicyEdits()
		self.setPolicyButtons()
		self.top_layout.setColumnStretch(0, 1)
		self.top_layout.setColumnStretch(1, 2)


		self.list_states = StateList()
		self.list_states.setDragEnabled(True)
		self.list_states.itemChanged.connect(self.itemChanged)
		self.list_symbol.itemChanged.connect(self.symbol_changed)
		item = StateItem("q0")
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		self.list_states.addItem(item)
		#self.list_states.setCurrentItem(item)

		self.list_states.itemSelectionChanged.connect(self.selectChanged)
		self.top_layout.addWidget(self.list_states, 1,1)
		self.list_states.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.top_panel.setStyleSheet("background:green;")
		self.top_panel.setLayout(self.top_layout)
		self.layout.setRowStretch(0, 1)
		self.layout.setRowStretch(1, 5)
		self.layout.addWidget(self.top_panel,0,0)
		self.layout.addWidget(self.transition_table_ui, 1, 0)
		self.layout.addWidget(self.bottom_panel, 2, 0)
		self.setLayout(self.layout)
		self.set_button_events()
		self.set_edits_events()
		self.i = 0
		self.last_selected = None
		self.transition_table_ui.setVerticalHeaderItem(0, StateTableItem("q0"))
		self.set_placeholders()
		self.alphabet = []
		#self.showAutomaton(Globals.automata[0])

	def add_new_symbol(self):
		symbols = [str(self.list_symbol.item(i).text()) for i in range(self.list_symbol.count())]
		c_ord = -1
		for s in symbols:
			if (c_ord < ord(s)):
				c_ord = ord(s)

		new_symbol = chr(c_ord+1)
		item = SymbolItem(new_symbol)
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		self.list_symbol.addItem(item)
		column = self.transition_table_ui.columnCount() - 2
		self.transition_table_ui.insertColumn(column)
		self.transition_table_ui.setHorizontalHeaderItem(column, QTableWidgetItem(new_symbol))

		rowCount = self.transition_table_ui.rowCount()

		for i in range(0, rowCount):
			self.transition_table_ui.setItem(i, column , QTableWidgetItem("-"))
	def remove_symbol(self):
		item = self.list_symbol.selectedItems()[0]
		print(item.text())
		column_count = self.transition_table_ui.columnCount()

		for i in range(0, column_count):
			if self.transition_table_ui.horizontalHeaderItem(i).text() == item.text():
				self.transition_table_ui.removeColumn(i)
				break
		self.list_symbol.takeItem(self.list_symbol.currentRow())
	def setPolicyEdits(self):
		self.edit_name.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.edit_alphabet.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
	def setPolicyButtons(self):
		self.add_new_state.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.remove_state_button.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
	def set_placeholders(self):
		self.edit_name.setPlaceholderText("Digite o nome do automato")
		self.edit_alphabet.setPlaceholderText("Digite o alfabeto")
	def set_button_events(self):
		self.add_new_state.clicked.connect(self.create_state)
		self.remove_state_button.clicked.connect(self.remove_state)
	def set_edits_events(self):
		self.edit_alphabet.textEdited.connect(self.alphabet_changed)
	def generate_table(self, alphabet, states_names):
		print()

	def create_state(self):
		self.i += 1
		item = StateItem("q" + str(self.i))
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		self.list_states.addItem(item)
		count = self.transition_table_ui.rowCount()
		column_count = len(self.alphabet)
		self.transition_table_ui.setRowCount(count+1)
		self.transition_table_ui.setVerticalHeaderItem(count, StateTableItem("q" + str(self.i)))
		for i in range(0, len(self.alphabet)):
			self.transition_table_ui.setItem(count,i,QTableWidgetItem("-"))

		rb = QRadioButton()
		cb = QCheckBox()
		self.initial_state_radio_group.addButton(rb)
		self.transition_table_ui.setCellWidget(count,column_count,rb)
		self.transition_table_ui.setCellWidget(count,column_count+1,cb)

	def remove_state(self):
		item = self.list_states.takeItem(self.list_states.row(self.list_states.selectedItems()[0]))
		row_count = self.transition_table_ui.rowCount()
		column_count = self.transition_table_ui.columnCount()

		for i in range(0, row_count):
			for j in range(0, column_count - 2):
				try:
					if self.transition_table_ui.item(i, j).text() == item.text():
						self.transition_table_ui.item(i, j).setText("-")
				except:
					print("Problema com " + str((i,j)))
		for i in range(0, row_count):
			if self.transition_table_ui.verticalHeaderItem(i).text() == item.text():
					self.transition_table_ui.removeRow(i)
					return
	def itemChanged(self, item):
		print(item.oldName + " mudou para " + item.text())
		row_count = self.transition_table_ui.rowCount()
		column_count = self.transition_table_ui.columnCount()
		# este for muda o header da tabela
		for i in range(0, row_count):
			try:
				if self.transition_table_ui.verticalHeaderItem(i).text() == item.oldName:
					print("haha")
					self.transition_table_ui.setVerticalHeaderItem(i, StateTableItem(item.text()))
			except:
				pass
		for i in range(0, row_count):
			for j in range(0, column_count):
				try:
					if self.transition_table_ui.item(i, j).text() == item.oldName:
						self.transition_table_ui.item(i,j).setText(item.text())
				except:
					pass


		item.oldName = item.text()
		MainWindow.jesus = item.text()
	def symbol_changed(self, item):
			approval_change = True
			items = [self.list_symbol.item(i) for i in range(self.list_symbol.count())]
			items = list(set(items) - {self.list_symbol.selectedItems()[0]})

			for i in items:
				if item.text() == i.text():
					print("IGUAL")
					approval_change = False
					break
			if approval_change:
				column_count = self.transition_table_ui.columnCount()
				for i in range(0, column_count):
					if self.transition_table_ui.horizontalHeaderItem(i).text() == item.oldName:
						self.transition_table_ui.horizontalHeaderItem(i).setText(item.text())
						print("OFUND")
				item.oldName = item.text()
			else:
				item.setText(item.oldName)
	def selectChanged(self):
		'''
			no momento, este método não tem uso algum
		'''
		print("quem mudou= " + self.list_states.selectedItems()[0].text())
		self.last_selected = self.list_states.selectedItems()[0]
		MainWindow.jesus = self.list_states.selectedItems()[0].text()
		print(MainWindow.jesus)

	def create_transition_table(self):
		raw_text = self.edit_alphabet.text()
		alphabet = raw_text.split(",")
		alphabet = sorted(list(set(alphabet)), key=str.lower)
		self.transition_table_ui.setColumnCount(len(alphabet) + 2)
		self.setColsLabels(alphabet)
		self.alphabet = alphabet
		header = self.transition_table_ui.horizontalHeader()
		for i in range(0, self.transition_table_ui.columnCount()):
			header.setSectionResizeMode(i, QHeaderView.Stretch)
		row_count = self.transition_table_ui.rowCount()
		column_count = self.transition_table_ui.columnCount() - 2
		for i in range(0, row_count):
			for j in range(0, column_count):
				self.transition_table_ui.setItem(i,j,QTableWidgetItem("(" + str(i) + "," + str(j) + ")"))
		initial_state_radio_group = QButtonGroup()
		for i in range(0, row_count):
			r = QRadioButton()
			c = QCheckBox()
			self.initial_state_radio_group.addButton(r)
			self.transition_table_ui.setCellWidget(i,column_count,QRadioButton())
			self.transition_table_ui.setCellWidget(i,column_count+1,c)

	def setColsLabels(self, labels):
		i = 0
		for label in labels:
			self.transition_table_ui.setHorizontalHeaderItem(i, StateTableItem(label))
			#self.transition_table_ui.setColumnWidth(i, 1)
			i+=1

		self.transition_table_ui.setHorizontalHeaderItem(i, StateTableItem("Inicial"))
		self.transition_table_ui.setHorizontalHeaderItem(i+1, StateTableItem("Final"))
	def alphabet_changed(self):
		print(self.alphabet)
		text = self.edit_alphabet.text()

		self.transition_table_ui.insertColumn(1)
		return
		if len(text) == 1:
			return
		if text[len(text)-1] == ",":
			new_text = text[0:len(text)-1]
			old_column_count = self.transition_table_ui.columnCount()
			self.transition_table_ui.setColumnCount(old_column_count - 3)
		else:
			new_text = text[0:len(text) - 1] + "," + text[len(text) - 1]
			old_column_count = self.transition_table_ui.columnCount()
			self.transition_table_ui.setColumnCount(old_column_count - 2)
			self.transition_table_ui.setColumnCount(old_column_count + 1)
			self.setColsLabels(new_text.split(","))
		self.edit_alphabet.setText(new_text)
		#self.showAutomaton(Globals.selected)

	def showAutomaton(self, af):
		self.list_states.clear()
		self.list_symbol.clear()
		self.edit_alphabet.setText(','.join(map(str, af.Σ)) )
		self.alphabet = af.Σ
		self.transition_table_ui.setRowCount(len(af.states))
		self.transition_table_ui.setColumnCount(len(af.Σ) + 2)
		self.setColsLabels(af.Σ)
		states_list = list(af.states)
		self.initial_state_radio_group = QButtonGroup()
		for i in range(0, len(af.Σ)):
			item = SymbolItem(af.Σ[i])
			item.setFlags(item.flags() | Qt.ItemIsEditable)
			self.list_symbol.addItem(item)
		for i in range(0, len(states_list)):
			s = states_list[i]
			item = StateItem(s.name)
			item.setFlags(item.flags() | Qt.ItemIsEditable)
			self.list_states.addItem(item)
			self.transition_table_ui.setVerticalHeaderItem(i, StateTableItem(s.name))
			cb = QCheckBox()
			rb = QRadioButton()
			self.initial_state_radio_group.addButton(rb)
			if s.isAcceptance:
				cb.setChecked(True)
			if s == af.initialState:
				rb.setChecked(True)
			self.transition_table_ui.setCellWidget(i, len(af.Σ)+1, cb)
			self.transition_table_ui.setCellWidget(i, len(af.Σ), rb)

		for i in range(0, len(states_list)):
			s = states_list[i]
			for t in s.transitions:
				self.set_transition_cell(s.name, t.target_state.name, t.symbol)

	def set_transition_cell(self, state, target, symbol):
		row = -1
		column = -1
		for i in range(0, self.transition_table_ui.columnCount()):
			if self.transition_table_ui.horizontalHeaderItem(i).text() == symbol:
				print("coluna = " + str(i))
				column = i
		for i in range(0, self.transition_table_ui.rowCount()):
			if self.transition_table_ui.verticalHeaderItem(i).text() == state:
				print("linha = " + str(i))
				row = i
		print((row,column))
		self.transition_table_ui.setItem(row, column, QTableWidgetItem(target))
	def save_automaton(self):
		states = set()
		finalStates = set()
		initialState = None
		newΣ = []
		for j in range(0, self.transition_table_ui.columnCount() - 2):
			newΣ.append(self.transition_table_ui.horizontalHeaderItem(j).text())
		for i in range(0, self.transition_table_ui.rowCount()):
			newS = State(self.transition_table_ui.verticalHeaderItem(i).text(), self.transition_table_ui.cellWidget(i, self.transition_table_ui.columnCount() - 1).checkState() == 2)
			states.add(newS)
			if newS.isAcceptance:
				finalStates.add(newS)
			if self.transition_table_ui.cellWidget(i, len(newΣ) + 1).isChecked():
				initialState = newS
		for i in range(0, self.transition_table_ui.rowCount()):
			for s in states:
				if self.transition_table_ui.verticalHeaderItem(i).text() == s.name:
					for j in range(0, self.transition_table_ui.columnCount() - 2):
						for ns in states:
							if ns.name == self.transition_table_ui.item(i,j).text():
								s.add_transition(Transition(self.transition_table_ui.horizontalHeaderItem(j).text(), ns))

		auts = []
		newA = Automaton(states, finalStates, initialState, newΣ, Globals.selected.name)
		for a in Globals.automata:
			if a.name != Globals.selected.name:
				auts.append(a)
			else:
				auts.append(newA)
		Globals.automata = auts
		Globals.selected = newA
		self.saveAF.emit(Globals.selected)


class GrammarOperationsTab(QWidget):
	updateGR = QtCore.pyqtSignal(Grammar)
	def __init__(self):
		super(QWidget, self).__init__()

		self.line = 0
		self.layout = QGridLayout()
		self.layout.setRowStretch(0,1)
		self.layout.setRowStretch(1,1)
		self.layout.setRowStretch(2,1)
		self.top = QWidget()
		self.top.setStyleSheet("background-color:pink;")
		self.top_layout = QGridLayout()
		self.top_layout.setRowStretch(0,1)
		self.top_layout.setRowStretch(1,1)
		self.top_layout.setRowStretch(2,1)
		self.top_layout.setRowStretch(3,1)
		self.top_op1 = QWidget()
		self.top_op1.setStyleSheet("background-color:purple;")
		self.top_op1_layout = QGridLayout()
		self.top_op1_layout.setColumnStretch(0,1)
		self.top_op1_layout.setColumnStretch(1,1)
		self.top_op1label = QLabel()
		self.top_op1label.setText("GR 1:")
		self.top_op1edit = QLineEdit()
		self.top_op1_layout.addWidget(self.top_op1label,0,0)
		self.top_op1_layout.addWidget(self.top_op1edit,0,1)
		self.top_op1.setLayout(self.top_op1_layout)
		self.top_op2 = QWidget()
		self.top_op2.setStyleSheet("background-color:purple;")
		self.top_op2_layout = QGridLayout()
		self.top_op2_layout.setColumnStretch(0,1)
		self.top_op2_layout.setColumnStretch(1,1)
		self.top_op2label = QLabel()
		self.top_op2label.setText("GR 2:")
		self.top_op2edit = QLineEdit()
		self.top_op2_layout.addWidget(self.top_op2label,0,0)
		self.top_op2_layout.addWidget(self.top_op2edit,0,1)
		self.top_op2.setLayout(self.top_op2_layout)
		self.top_operation = QLabel()
		self.top_operation.setAlignment(Qt.AlignCenter)
		self.top_operation.setText("concatenada com")
		self.top_operation.setStyleSheet("background-color:orange;")
		self.top_done = QPushButton("Pronto")
		self.top_done.clicked.connect(self.add_concatenation)
		self.top_layout.addWidget(self.top_op1,0,0)
		self.top_layout.addWidget(self.top_op2,2,0)
		self.top_layout.addWidget(self.top_operation,1,0)
		self.top_layout.addWidget(self.top_done,3,0)
		self.top.setLayout(self.top_layout)

		self.mid = QWidget()
		self.mid.setStyleSheet("background-color:pink;")
		self.mid_layout = QGridLayout()
		self.mid_layout.setRowStretch(0,1)
		self.mid_layout.setRowStretch(1,1)
		self.mid_layout.setRowStretch(2,1)
		self.mid_layout.setRowStretch(3,1)
		self.mid_op1 = QWidget()
		self.mid_op1.setStyleSheet("background-color:purple;")
		self.mid_op1_layout = QGridLayout()
		self.mid_op1_layout.setColumnStretch(0,1)
		self.mid_op1_layout.setColumnStretch(1,1)
		self.mid_op1label = QLabel()
		self.mid_op1label.setText("GR 1:")
		self.mid_op1edit = QLineEdit()
		self.mid_op1_layout.addWidget(self.mid_op1label,0,0)
		self.mid_op1_layout.addWidget(self.mid_op1edit,0,1)
		self.mid_op1.setLayout(self.mid_op1_layout)
		self.mid_op2 = QWidget()
		self.mid_op2.setStyleSheet("background-color:purple;")
		self.mid_op2_layout = QGridLayout()
		self.mid_op2_layout.setColumnStretch(0,1)
		self.mid_op2_layout.setColumnStretch(1,1)
		self.mid_op2label = QLabel()
		self.mid_op2label.setText("GR 2:")
		self.mid_op2edit = QLineEdit()
		self.mid_op2_layout.addWidget(self.mid_op2label,0,0)
		self.mid_op2_layout.addWidget(self.mid_op2edit,0,1)
		self.mid_op2.setLayout(self.mid_op2_layout)
		self.mid_operation = QLabel()
		self.mid_operation.setAlignment(Qt.AlignCenter)
		self.mid_operation.setText("unida com")
		self.mid_operation.setStyleSheet("background-color:orange;")
		self.mid_done = QPushButton("Pronto")
		self.mid_done.clicked.connect(self.add_union)
		self.mid_layout.addWidget(self.mid_op1,0,0)
		self.mid_layout.addWidget(self.mid_op2,2,0)
		self.mid_layout.addWidget(self.mid_operation,1,0)
		self.mid_layout.addWidget(self.mid_done,3,0)
		self.mid.setLayout(self.mid_layout)

		self.bot = QWidget()
		self.bot.setStyleSheet("background-color:pink;")
		self.bot_layout = QGridLayout()
		self.bot_layout.setRowStretch(0,1)
		self.bot_layout.setRowStretch(1,1)
		self.bot_layout.setRowStretch(2,1)
		self.bot_op1 = QWidget()
		self.bot_op1.setStyleSheet("background-color:purple;")
		self.bot_op1_layout = QGridLayout()
		self.bot_op1_layout.setColumnStretch(0,1)
		self.bot_op1_layout.setColumnStretch(1,1)
		self.bot_op1label = QLabel()
		self.bot_op1label.setText("GR:")
		self.bot_op1edit = QLineEdit()
		self.bot_op1_layout.addWidget(self.bot_op1label,0,0)
		self.bot_op1_layout.addWidget(self.bot_op1edit,0,1)
		self.bot_op1.setLayout(self.bot_op1_layout)
		self.bot_operation = QLabel()
		self.bot_operation.setAlignment(Qt.AlignCenter)
		self.bot_operation.setText("fechada")
		self.bot_operation.setStyleSheet("background-color:orange;")
		self.bot_done = QPushButton("Pronto")
		self.bot_done.clicked.connect(self.add_kleene)
		self.bot_layout.addWidget(self.bot_op1,0,0)
		self.bot_layout.addWidget(self.bot_operation,1,0)
		self.bot_layout.addWidget(self.bot_done,2,0)
		self.bot.setLayout(self.bot_layout)

		self.layout.addWidget(self.top,0,0)
		self.layout.addWidget(self.mid,1,0)
		self.layout.addWidget(self.bot,2,0)

		self.setLayout(self.layout)
	def add_concatenation(self):
		g_1 = None
		g_2 = None
		for g1 in Globals.grammars:
			if g1.name == self.top_op1edit.text():
				g_1 = g1
		for g2 in Globals.grammars:
			if g2.name == self.top_op2edit.text():
				g_2 = g2
		if g_1 != None and g_2 != None:
			newG = grammar_concatenation(g_1, g_2)
			if newG in Globals.grammars:
				newG.name = newG.name + "'"
			Globals.grammars.append(newG)
			Globals.selected = newG
			self.updateGR.emit(Globals.selected)

	def add_union(self):
		g_1 = None
		g_2 = None
		for g1 in Globals.grammars:
			if g1.name == self.mid_op1edit.text():
				g_1 = g1
		for g2 in Globals.grammars:
			if g2.name == self.mid_op2edit.text():
				g_2 = g2
		if g_1 != None and g_2 != None:
			newG = grammar_union(g_1, g_2)
			if newG in Globals.grammars:
				newG.name = newG.name + "'"
			Globals.grammars.append(newG)
			Globals.selected = newG
			self.updateGR.emit(Globals.selected)
	def add_kleene(self):
		g_1 = None
		for g1 in Globals.grammars:
			if g1.name == self.bot_op1edit.text():
				g_1 = g1
		if g_1 != None:
			newG = grammar_kleene_star(g_1)
			if newG in Globals.grammars:
				newG.name = newG.name + "'"
			Globals.grammars.append(newG)
			Globals.selected = newG
			self.updateGR.emit(Globals.selected)


class StateList(QListWidget):
	def __init__(self):
		super(QListWidget, self).__init__()
class StateItem(QListWidgetItem):
	def __init__(self, text):
		super().__init__(text)
		self.oldName = text
class SymbolItem(QListWidgetItem):
	def __init__(self, text):
		super().__init__(text)
		self.oldName = text
	def __hash__(self):
		return id(self)

class StateTableItem(QTableWidgetItem):
	def __init__(self, text):
		super(QTableWidgetItem, self).__init__(text)
	def dropEvent(self, event):
		print("misc")

class AutomatonTable(QTableWidget):
	def __init__(self):
		super(QTableWidget, self).__init__()
		self.setAcceptDrops(True)
	def dropEvent(self, event):
		position = event.pos()
		x = self.rowAt(position.y())
		y = self.columnAt(position.x())
		self.item(x,y).setText(MainWindow.jesus)
		event.accept()
	def dragEnterEvent(self, event):
		print('ender')
		event.accept()
	def keyPressEvent(self, event):
		print("deletado")
class TransitionTable:
	def __init__(self):
		print('something')


class AutomataOperationsTab(QWidget):
	def __init__(self, parent=None):
		super(QWidget, self).__init__(parent)
		self.layout = QVBoxLayout(self)
		self.tabs = QTabWidget()
		self.tab1 = QWidget()
		self.tab2 = QWidget()
		self.tabs.resize(300,200)

		self.tabs.addTab(self.tab1,"Union")
		self.tabs.addTab(self.tab2,"Concatenation")

		self.tab1.layout = QVBoxLayout(self)
		self.pushButton1 = QPushButton("PyQt5 button")
		self.tab1.layout.addWidget(self.pushButton1)
		self.tab1.setLayout(self.tab1.layout)

		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)
	@pyqtSlot()
	def on_click(self):
		print("\n")
		for currentQTableWidgetItem in self.tableWidget.selectedItems():
			print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class UnionTab(QWidget):
	def __init__(self):
		super(QWidget,self).__init__()
		self.top_panel = QWidget()
		self.bottom_panel = QWidget()
		self.button_af1 = QPushButton()
		self.button_af2 = QPushButton()
		self.top_layout = QGridLayout()
		self.bottom_layout = QGridLayout()
		self.set_top_panel()
	def set_top_panel(self):
		self.top_layout.addWidget(self.button_af1, 0, 0)
		self.top_layout.addWidget(self.button_af2, 1, 0)


class Edit(QLineEdit):
	def __init__(self, parent=None):
		QLineEdit.__init__(self, parent)

	def keyPressEvent(self, event):
		if type(event) == QtGui.QKeyEvent:
			#self.setText (chr(event.key()).lower())
			event.accept()
		else:
			event.ignore()
