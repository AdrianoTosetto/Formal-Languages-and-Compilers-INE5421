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

class SimoneTab(QWidget):

	def __init__(self):
		super(QWidget,self).__init__()
		self.regex_edit = QLineEdit() # re
		self.convert_button = QPushButton("Converter")
		self.top_layout = QGridLayout()
		self.top_panel = QWidget()
		self.build_top_panel()
		self.set_click_events()

	def build_top_panel(self):
		self.set_top_layout()
		self.setLayout(self.top_layout)
	def set_top_layout(self):
		self.top_layout.addWidget(self.regex_edit)
		self.top_layout.addWidget(self.convert_button)
	def set_click_events(self):
		self.convert_button.clicked.connect(self.parse_to_automaton)

	def parse_to_automaton(self):
		print("WHAT")