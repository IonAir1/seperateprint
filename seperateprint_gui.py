from PyQt5 import QtCore, QtGui, QtWidgets
import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal


class ProcessThread(QThread):
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self):
        process = subprocess.Popen(
            self.args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )
        # Read stdout line by line, flush events to ensure signals are processed
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                self.output_signal.emit(line)
                QtCore.QThread.msleep(10)  # allow event loop to process signals
        process.stdout.close()
        # Read stderr at the end
        error = process.stderr.read()
        if error:
            self.error_signal.emit(error)
        process.stderr.close()
        process.wait()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 360)
        MainWindow.setMinimumSize(QtCore.QSize(300, 200))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileSelect = QtWidgets.QGroupBox(self.centralWidget)
        self.fileSelect.setObjectName("fileSelect")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.fileSelect)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.fileText = QtWidgets.QLineEdit(self.fileSelect)
        self.fileText.setObjectName("fileText")
        self.horizontalLayout_7.addWidget(self.fileText)
        self.file_button = QtWidgets.QPushButton(self.fileSelect)
        self.file_button.setObjectName("file_button")
        self.horizontalLayout_7.addWidget(self.file_button)
        self.file_button.clicked.connect(self.openFileDialog)
        self.verticalLayout.addWidget(self.fileSelect)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.discardButton = QtWidgets.QCheckBox(self.centralWidget)
        self.discardButton.setObjectName("discardButton")
        self.gridLayout.addWidget(self.discardButton, 2, 4, 1, 1)
        self.limitSpinbox = QtWidgets.QSpinBox(self.centralWidget)
        self.limitSpinbox.setMinimumSize(QtCore.QSize(60, 0))
        self.limitSpinbox.setObjectName("limitSpinbox")
        self.limitSpinbox.setMinimum(1)
        self.limitSpinbox.setMaximum(255)
        self.limitSpinbox.setValue(10)
        self.gridLayout.addWidget(self.limitSpinbox, 2, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 5, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 2, 1, 1)
        self.dpiSpinbox = QtWidgets.QSpinBox(self.centralWidget)
        self.dpiSpinbox.setMinimumSize(QtCore.QSize(60, 0))
        self.dpiSpinbox.setObjectName("dpiSpinbox")
        self.dpiSpinbox.setMinimum(10)
        self.dpiSpinbox.setMaximum(1200)
        self.dpiSpinbox.setValue(300)
        self.gridLayout.addWidget(self.dpiSpinbox, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.progressText = QtWidgets.QLabel(self.centralWidget)
        self.progressText.setObjectName("progressText")
        self.horizontalLayout_6.addWidget(self.progressText)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem5)
        self.startButton = QtWidgets.QPushButton(self.centralWidget)
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.startButtonClicked)
        self.horizontalLayout_6.addWidget(self.startButton)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Seperate Print"))
        self.fileSelect.setTitle(_translate("MainWindow", "PDF File"))
        self.file_button.setText(_translate("MainWindow", "Select"))
        self.label_6.setText(_translate("MainWindow", "Rendered DPI"))
        self.discardButton.setText(_translate("MainWindow", "Discard Empty Pages"))
        self.label_7.setText(_translate("MainWindow", "Color Limit"))
        self.progressText.setText(_translate("MainWindow", "Waiting for input..."))
        self.startButton.setText(_translate("MainWindow", "Start"))


    def openFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select PDF File",
            "",
            "PDF Files (*.pdf);;All Files (*)",
            options=options
        )
        if fileName:
            self.fileText.setText(fileName)


    def startButtonClicked(self):
        input_path = self.fileText.text()
        limit = self.limitSpinbox.value()
        dpi = self.dpiSpinbox.value()
        discard_empty = self.discardButton.isChecked()

        args = [
            'python', 'seperateprint.py', input_path, str(limit), str(dpi), str(discard_empty)
        ]
        self.progressText.setText("Processing...")
        self.newProcess = ProcessThread(args)
        self.newProcess.output_signal.connect(self.changeProgressText)
        self.newProcess.error_signal.connect(self.showErrorText)
        self.newProcess.start()

    def changeProgressText(self, text):
        self.progressText.setText(text)

    def showErrorText(self, text):
        self.progressText.setText("Error: " + text)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
