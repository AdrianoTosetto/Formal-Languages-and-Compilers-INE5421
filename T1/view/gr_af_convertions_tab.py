import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import functools

class ConvertionTab(QWidget):
	def __init__(self):
		super(QWidget, self).__init__(parent=None)
		self.convert_gr_af_layout = QGridLayout()
		self.convert_af_gr_layout = QGridLayout()
		self.convert_gr_af_panel = QWidget()
		self.convert_af_gr_panel = QWidget()

		self.gr_name = QLineEdit()
		self.af_name = QLineEdit()

		self.gr_convert = QPushButton("Converter para AF")
		self.af_convert = QPushButton("Converter para GR")

		self.main_layout = QGridLayout()
		
		self.set_click_events()

		self.set_policy_buttons()

		self.set_panels()


	def set_panels(self):
		self.convert_gr_af_layout.addWidget(self.gr_name)
		self.convert_gr_af_layout.addWidget(self.gr_convert)

		self.convert_af_gr_layout.addWidget(self.af_name)
		self.convert_af_gr_layout.addWidget(self.af_convert)

		self.convert_gr_af_panel.setLayout(self.convert_gr_af_layout)
		self.convert_af_gr_panel.setLayout(self.convert_af_gr_layout)

		self.main_layout.addWidget(self.convert_af_gr_panel)
		self.main_layout.addWidget(self.convert_gr_af_panel)

		self.setLayout(self.main_layout)
	def set_policy_buttons(self):
		self.gr_convert.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.af_convert.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.gr_name.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.af_name.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
	def set_click_events(self):
		self.gr_convert.clicked.connect(self.convert_to_af)
		self.af_convert.clicked.connect(self.convert_to_gr)

	def convert_to_af(self):
		print("converter gr para af")
	def convert_to_gr(self):
		print("converter af para gr")

