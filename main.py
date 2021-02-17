import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QGroupBox, QLineEdit, QPushButton,
                             QGridLayout, QTableWidget, QHBoxLayout, QAbstractItemView,
                             QLabel, QTableWidgetItem)
from PyQt5.QtCore import pyqtSlot
from formulaparser import parse_formula
import atomicMassGetter

class WidgetChemMassCalc(QDialog):
    def __init__(self, parent=None):
        super(WidgetChemMassCalc, self).__init__(parent)
        self.createTopGroupBox()
        self.createBottomGroupBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topGroupBox, 0, 0, 1, 1)
        mainLayout.addWidget(self.bottomGroupBox, 1, 0, 1, 1)
        self.setLayout(mainLayout)

        self.setFixedWidth(460)
        self.setFixedHeight(800)

        self.setWindowTitle("Moleküler Ağırlık Hesaplayıcı")
    
    def createTopGroupBox(self):
        self.topGroupBox = QGroupBox("Formül")
        
        self.formulaLineEdit = QLineEdit()
        calculateButton = QPushButton("Hesapla")
        calculateButton.clicked.connect(self.calculate)
        
        layout = QGridLayout()
        layout.addWidget(self.formulaLineEdit, 0, 0, 1, 1)
        layout.addWidget(calculateButton, 0, 1, 1, 1)        
        self.topGroupBox.setLayout(layout)

    def getMassPercent(self, elementName, formulaHash):
        totalMass = 0
        for name, quantity in formulaHash.items():
            totalMass += atomicMassGetter.get(name)*quantity
        percent = (atomicMassGetter.get(elementName)*formulaHash[elementName])/totalMass*100
        return percent

    def prepareTableRows(self, formulaLen):
        tableRowLen = self.tableWidget.rowCount()
        if formulaLen == tableRowLen - 1:
            return

        print(formulaLen, tableRowLen)

        if formulaLen >= tableRowLen:
            for i in range(tableRowLen, formulaLen + 1):
                self.tableWidget.insertRow(i)
        else:
            for i in range(formulaLen, tableRowLen + 2):
                self.tableWidget.removeRow(i)
    
    @pyqtSlot()
    def calculate(self):
        formula = self.formulaLineEdit.text()
        formulaHash = parse_formula(formula)

        self.prepareTableRows(len(formulaHash))
        
        totalMass = 0
        rowIndex = 1
        for elementName, elementQuantity in formulaHash.items():
            massPercent = self.getMassPercent(elementName, formulaHash)
            moleMass = atomicMassGetter.get(elementName)
            elementTotalMoleMass = moleMass * elementQuantity

            totalMass += elementTotalMoleMass
            
            self.tableWidget.setItem(rowIndex, 0, QTableWidgetItem(str(elementQuantity)))
            self.tableWidget.setItem(rowIndex, 1, QTableWidgetItem(elementName))
            self.tableWidget.setItem(rowIndex, 2, QTableWidgetItem(format(moleMass, ".4f")))
            self.tableWidget.setItem(rowIndex, 3, QTableWidgetItem(format(massPercent, ".4f")))
            self.tableWidget.setItem(rowIndex, 4, QTableWidgetItem(format(elementTotalMoleMass, ".4f")))
            
            rowIndex += 1

        self.moleMassLineEdit.setText(format(totalMass, ".4f"))
        
    def createBottomGroupBox(self):
        self.bottomGroupBox = QGroupBox("Hesaplama Sonuçları")

        self.tableWidget = QTableWidget(1,5)
        self.tableWidget.setSelectionMode(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setColumnWidth(0, 40)
        self.tableWidget.setColumnWidth(1, 60)
        self.tableWidget.setColumnWidth(3, 119)
        self.tableWidget.setColumnWidth(4, 97)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("#"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Atom"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Mol Kütlesi"))
        self.tableWidget.setItem(0, 3, QTableWidgetItem("Total Kütle Yüzdesi"))
        self.tableWidget.setItem(0, 4, QTableWidgetItem("Total Kütle"))

        
        labelWidget = QLabel("Molekülün Mol Kütlesi")
        self.moleMassLineEdit = QLineEdit()
        
        layout = QGridLayout()
        layout.addWidget(self.tableWidget, 0, 0, 1, 10)
        layout.addWidget(labelWidget, 6, 0, 1, 1)
        layout.addWidget(self.moleMassLineEdit, 6, 2, 1, 2)
            
        self.bottomGroupBox.setLayout(layout)
        
      
def main():
    app = QApplication(sys.argv)
    chemMassCalc = WidgetChemMassCalc()
    chemMassCalc.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
