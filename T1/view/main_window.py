import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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

		addButton = QPushButton('Adicionar', self)
		addButton.setToolTip('Adicionar GR/ER/AF')
		addButton.clicked.connect(self.on_click)
		self.addLayout = QVBoxLayout()
		self.addLayout.addWidget(addButton)
		self.optionAdd.setLayout(self.addLayout)

		editButton = QPushButton('Editar', self)
		editButton.setToolTip('Editar GR/ER/AF')
		editButton.clicked.connect(self.on_click)
		self.editLayout = QVBoxLayout()
		self.editLayout.addWidget(editButton)
		self.optionEdit.setLayout(self.editLayout)

		self.grList = QListWidget(self)
		self.listLayout = QVBoxLayout()
		self.listLayout.addWidget(self.grList)
		self.listofentities.setLayout(self.listLayout)

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
	def add_gr(self):
		self.grList.clear()
		for g in grammars:
			item = QListWidgetItem(self.grList)
			item_widget = QPushButton(str(g), self)
			self.grList.setItemWidget(item, item_widget)
			self.grList.addItem(item)

if __name__ == "__main__":
	m = MainWindow()
