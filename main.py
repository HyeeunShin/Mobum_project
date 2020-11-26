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

        self.resultLabel = QLabel('                <조회 결과>                ', self)
        self.resultLabel.setAlignment(Qt.AlignVCenter)
        font = self.resultLabel.font()
        font.setFamily('Times New Roman')
        font.setBold(True)
        font.setPointSize(15)
        self.resultLabel.setFont(font)

        searchStoreLayout.addWidget(self.resultLabel, 1, 0)

        self.typeEdit = QTextEdit()
        self.typeEdit.setReadOnly(True)
        self.typeEdit.setAlignment(Qt.AlignCenter)
        text_font = self.typeEdit.font()
        text_font.setPointSize(text_font.pointSize() )
        self.typeEdit.setFont(text_font)
        searchStoreLayout.addWidget(self.typeEdit, 2, 0)

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


    def searchClicked(self):
        inputName = self.nameInput.text()
        self.nameInput.clear()

        self.result_lst = self.url.get_data(inputName)
        print(self.result_lst)
        try:
            if self.result_lst[0] == '모범음식점':
                self.mobum_text = ("상호명 '" + str(inputName) + "'" + "은 모범음식점 업소 입니다.")
                self.add_text = ("주소: " + str(self.result_lst[0]))
                self.tell_text = ("전화번호: " + str(self.result_lst[2]))
            else:
                self.mobum_text = ("상호명 '" + str(inputName) + "'" + "은 모범음식점이 취소된 업소입니다.")
                self.add_text = ("주소: " + str(self.result_lst[0]))
                self.tell_text = ("모범음식점 취소 사유는 다음과 같습니다,: " + self.result_lst[2])

            self.typeEdit.setText(self.mobum_text)
            self.typeEdit.setText(self.add_text)
            self.typeEdit.setText(self.tell_text)

        except IndexError as e:
            self.text = ('해당 음식점을 조회할 수 없습니다.')
            self.typeEdit.setText(self.text)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    sStore = SearchStore()
    sStore.show()
    sys.exit(app.exec_())
