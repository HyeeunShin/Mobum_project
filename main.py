from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLayout, QGridLayout
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QToolButton, QLabel
from url import Url

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

        self.resultLabel = QLabel('                  <조회 결과>                ', self)
        self.resultLabel.setAlignment(Qt.AlignVCenter)
        font = self.resultLabel.font()
        font.setFamily('Times New Roman')
        font.setBold(True)
        font.setPointSize(15)
        self.resultLabel.setFont(font)

        searchStoreLayout.addWidget(self.resultLabel, 1, 0)

        self.resultEdit = QTextEdit()
        self.resultEdit.setReadOnly(True)
        self.resultEdit.setAlignment(Qt.AlignCenter)
        self.resultEdit.setFixedWidth(400)
        text_font = self.resultEdit.font()
        text_font.setPointSize(self.resultEdit.fontPointSize() + 10)
        self.resultEdit.setFont(text_font)
        searchStoreLayout.addWidget(self.resultEdit, 2, 0)

        self.newSearchButton = QToolButton()
        self.newSearchButton.setText('Research')
        self.newSearchButton.clicked.connect(self.startSearch)
        searchStoreLayout.addWidget(self.newSearchButton, 3, 1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(searchStoreLayout, 0, 0)
        self.setLayout(mainLayout)
        self.setWindowTitle('Search Store')

        self.startSearch()

    def startSearch(self):
        self.url = Url()
        self.resultEdit.clear()

    def searchClicked(self):
        inputName = self.nameInput.text()
        self.nameInput.clear()

        self.result_lst = self.url.get_data(inputName)
        print(self.result_lst)
        if self.result_lst == False:
            self.errorTxt = ('해당 음식점을 조회할 수 없습니다.')
            self.resultEdit.setPlainText(self.errorTxt)
        else:
            self.showResult(self.result_lst, inputName)


    def showResult(self, data, keyname):
        result_txt = ""

        result_txt += ('해당 업소는 <' + data[0] + '> 입니다.\n' + data[1])

        self.resultEdit.setPlainText(result_txt)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    sStore = SearchStore()
    sStore.show()
    sys.exit(app.exec_())
