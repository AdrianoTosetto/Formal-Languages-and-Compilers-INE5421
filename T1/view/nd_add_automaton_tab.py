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

class addNDAutomatonTab(QWidget):
	saveAF = QtCore.pyqtSignal(Automaton)
	def __init__(self):
		super(QWidget,self).__init__()
		self.initial_state_radio_group = QButtonGroup()
		self.transition_table_ui = NDAutomatonTable() # layout transition table
		self.transition_table = TransitionTable() # real transition table
		self.layout = QGridLayout()
		self.transition_table_ui.setRowCount(1)
		self.transition_table_ui.setColumnCount(0)
		self.transition_table_ui.setAcceptDrops(True)
		self.transition_table_ui.setItem(0,0, StateTableItem("q0"))
		jesus1 = "-"
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
		NDAutomatonTable.jesus1 = item.text()
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
		NDAutomatonTable.jesus1 = self.list_states.selectedItems()[0].text()
		print("jesus = " + NDAutomatonTable.jesus1)

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
			for t in s.ndtransitions:
				str_states_names = ""
				for ts in t.target_states:
					str_states_names += ts.name
				self.set_transition_cell(s.name, str_states_names, t.symbol)

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


class NDAutomatonTable(QTableWidget):
	def __init__(self):
		super(QTableWidget, self).__init__()
		self.setAcceptDrops(True)
	def dropEvent(self, event):
		position = event.pos()
		x = self.rowAt(position.y())
		y = self.columnAt(position.x())
		self.item(x,y).setText(self.item(x,y).text() + "," + NDAutomatonTable.jesus1)
		event.accept()
	def dragEnterEvent(self, event):
		print('ender')
		event.accept()
	def keyPressEvent(self, event):
		print("deletado")
class TransitionTable:
	def __init__(self):
		print('something')


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