import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton,QLabel

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
		self.leftLayout.setRowStretch(1, 1)
		self.leftLayout.setRowStretch(2, 8)
		self.leftLayout.addWidget(self.options,0,0)
		self.leftLayout.addWidget(self.entities,1,0)
		self.leftLayout.addWidget(self.listofentities,2,0)


		self.mainLayout = QGridLayout()
		self.mainLayout.setColumnStretch(0, 1)
		self.mainLayout.setColumnStretch(1, 3)
		self.mainLayout.addWidget(self.leftSide,0,0)
		self.mainLayout.addWidget(self.rightSide,0,1) 
		self.setLayout(self.mainLayout)
		self.leftSide.setLayout(self.leftLayout)
		self.show()
		sys.exit(self.app.exec_())




if __name__ == "__main__":
	m = MainWindow()