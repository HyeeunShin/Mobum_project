from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableView
from PyQt5.QtWidgets import QLayout, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QToolButton, QLabel
from url import Url
from dataFrame import pandasModel

class SearchStore(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.nameInput = QLineEdit()
        searchStoreLayout = QGridLayout()
        self.nameInput.setFixedHeight(30)

        searchStoreLayout.addWidget(self.nameInput, 0, 0)

        self.searchButton = QToolButton()
        self.searchButton.setText('조회하기')
        self.searchButton.setFixedSize(100, 30)
        self.searchButton.clicked.connect(self.searchClicked)
        searchStoreLayout.addWidget(self.searchButton, 0, 1)

        self.resultLabel = QLabel('<조회 결과>', self)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        font = self.resultLabel.font()
        font.setFamily('Times New Roman')
        font.setBold(True)
        font.setPointSize(15)
        self.resultLabel.setFont(font)

        searchStoreLayout.addWidget(self.resultLabel, 1, 0)

        self.dataView = QTableView()
        self.url = Url()
        self.default_data = self.url.get_link()
        searchStoreLayout.addWidget(self.dataView, 2, 0)
        self.model = pandasModel(self.default_data)
        self.dataView.setModel(self.model)
        font = self.dataView.font()
        font.setPointSize(font.pointSize() + 5)
        self.dataView.resizeColumnsToContents()

        self.newSearchButton = QToolButton()
        self.newSearchButton.setText('처음으로')
        self.newSearchButton.clicked.connect(self.startSearch)
        self.newSearchButton.setFixedSize(100, 40)

        searchStoreLayout.addWidget(self.newSearchButton, 4, 1)


        mainLayout = QGridLayout()
        mainLayout.addLayout(searchStoreLayout, 0, 0)
        self.setLayout(mainLayout)
        self.setWindowTitle('모범음식점 조회하기')

    def startSearch(self):
        self.nameInput.clear()
        self.model = pandasModel(self.default_data)
        self.dataView.setModel(self.model)

    def searchClicked(self):
        inputName = self.nameInput.text()
        self.nameInput.clear()

        if inputName == '':
            reply = QMessageBox.warning(self, 'Message', '업소명을 입력하세요.',
                                          QMessageBox.Ok, QMessageBox.Ok)
            if reply == QMessageBox.Ok:
                self.startSearch()

        result = self.url.get_data(inputName)
        model = pandasModel(result)
        self.dataView.setModel(model)
        self.dataView.resizeColumnsToContents()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    sStore = SearchStore()
    sStore.setGeometry(500, 150, 1000, 600)
    sStore.show()
    sys.exit(app.exec_())
