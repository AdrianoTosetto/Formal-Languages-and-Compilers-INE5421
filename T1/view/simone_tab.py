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
from operations_with_automata import *
from structures import *

class SimoneTab(QWidget):
	saveER = QtCore.pyqtSignal(str)
	saveDS = QtCore.pyqtSignal()
	def __init__(self):
		super(QWidget,self).__init__()
		self.regex_edit = QLineEdit() # re
		self.transition_table_composition = QTableWidget()
		self.convert_button = QPushButton("Converter")
		self.save_er = QPushButton("Salvar")
		self.top_layout = QGridLayout()
		self.top_panel = QWidget()
		self.build_top_panel()
		self.main_layout = QGridLayout()
		self.bottom_layout = QGridLayout()
		self.bottom_panel = QWidget()
		self.set_bottom_panel()


		self.set_bottom_panel()
		self.set_main_layout()
		self.set_click_events()
	def set_main_layout(self):
		self.main_layout.addWidget(self.top_panel)
		self.main_layout.addWidget(self.bottom_panel)
		self.setLayout(self.main_layout)
	def build_top_panel(self):
		self.set_top_layout()
		self.top_panel.setLayout(self.top_layout)
	def set_top_layout(self):
		self.top_layout.addWidget(self.regex_edit)
		self.top_layout.addWidget(self.convert_button)
		self.top_layout.addWidget(self.save_er)
	def set_click_events(self):
		self.convert_button.clicked.connect(self.parse_to_automaton)
		self.save_er.clicked.connect(self.save_exp)

	def set_bottom_panel(self):
		self.set_bottom_layout()
		self.bottom_panel.setLayout(self.bottom_layout)
	def set_bottom_layout(self):
		self.bottom_layout.addWidget(self.transition_table_composition)
	def save_exp(self):
		print("WHAT")
		new_er = self.regex_edit.text()
		new_ers = []
		for e in Globals.expressions:
			if e != Globals.selected:
				new_ers.append(e)
			else:
				new_ers.append(new_er)
		Globals.expressions = new_ers
		Globals.selected = new_er
		self.saveER.emit(Globals.selected)
	def parse_to_automaton(self):
		print("NANI")
		if type(Globals.selected) == type('') or type(Globals.selected) == type(""):
			print(Globals.selected)
			ds_result = RegExp(Globals.selected).to_automaton()
			print(ds_result)
		Globals.automata.append(ds_result)
		self.saveDS.emit()
	def set_edit_er(self, regex):
		self.regex_edit.setText(regex)