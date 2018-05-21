import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import functools
import sys
sys.path.append('../')
from globals import *

class MainWindow(QWidget):
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
		self.rightLayout.addWidget(self.editPanel, 0, 1)
		self.rightLayout.setColumnStretch(0,5)
		self.rightLayout.setColumnStretch(1,3)

		self.rightSide.setLayout(self.rightLayout)

		self.generateLeftSide()

		self.center = QLabel()
		self.center.setText(str(grammars[0]))
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
		self.add_gr()
	def showAFs(self):
		self.erList.setHidden(True)
		self.grList.setHidden(True)
		self.afList.setHidden(False)
	def showGRs(self):
		self.erList.setHidden(True)
		self.afList.setHidden(True)
		self.grList.setHidden(False)
	def showERs(self):
		self.grList.setHidden(True)
		self.afList.setHidden(True)
		self.erList.setHidden(False)
	def select_grammar(self, gram):
		self.center.setText(str(gram))

	def add_gr(self):
		self.grList.clear()
		for g in grammars:
			item = QListWidgetItem(self.grList)
			item_widget = GrammarButton(g.name, g)
			item_widget.clicked.connect(functools.partial(self.select_grammar, g))
			self.grList.setItemWidget(item, item_widget)
			self.grList.addItem(item)

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
		self.optionAdd.setStyleSheet("background-color:indigo;")
		self.optionEdit.setStyleSheet("background-color:cyan;")
		self.optionsLayout = QGridLayout()
		self.optionsLayout.setColumnStretch(0,1)
		self.optionsLayout.setColumnStretch(1,1)
		self.optionsLayout.addWidget(self.optionAdd,0,0)
		self.optionsLayout.addWidget(self.optionEdit,0,1)
		self.options.setLayout(self.optionsLayout)

		self.addButton = QPushButton('Adicionar', self)
		self.addButton.setToolTip('Adicionar GR/ER/AF')
		self.addButton.clicked.connect(self.on_click)
		self.addLayout = QVBoxLayout()
		self.addLayout.addWidget(self.addButton)
		self.optionAdd.setLayout(self.addLayout)

		self.editButton = QPushButton('Editar', self)
		self.editButton.setToolTip('Editar GR/ER/AF')
		self.editButton.clicked.connect(self.on_click)
		self.editLayout = QVBoxLayout()
		self.editLayout.addWidget(self.editButton)
		self.optionEdit.setLayout(self.editLayout)

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
		#self.grList.setHidden(True)
		self.afList.setHidden(True)
		self.erList.setHidden(True)
		self.listofentities.setLayout(self.listLayout)

if __name__ == "__main__":
	m = MainWindow()

class GrammarButton(QPushButton):
	def __init__(self, QString, grammar):
		self.grammar = grammar
		super().__init__(QString)
