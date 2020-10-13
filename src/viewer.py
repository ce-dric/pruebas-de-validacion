#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QEventLoop, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPalette, QGuiApplication, QIcon
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QWidget, QHBoxLayout, QDialog, QVBoxLayout, QLineEdit, QPushButton

import pyperclip
import os
import time


class QImageViewSync(QWidget):
    def __init__(self, parent):
        super(QImageViewSync, self).__init__(parent)

        self.parent = parent
        self.window = parent
        self.scaleFactor = 0.0

        self.imageLabelLeft = QLabel()
        self.imageLabelLeft.setBackgroundRole(QPalette.Base)
        self.imageLabelLeft.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabelLeft.setScaledContents(True)

        self.scrollAreaLeft = QScrollArea()
        self.scrollAreaLeft.setBackgroundRole(QPalette.Dark)
        self.scrollAreaLeft.setWidget(self.imageLabelLeft)
        self.scrollAreaLeft.setVisible(False)

        self.imageLabelRight = QLabel()
        self.imageLabelRight.setBackgroundRole(QPalette.Base)
        self.imageLabelRight.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabelRight.setScaledContents(True)

        self.scrollAreaRight = QScrollArea()
        self.scrollAreaRight.setBackgroundRole(QPalette.Dark)
        self.scrollAreaRight.setWidget(self.imageLabelRight)
        self.scrollAreaRight.setVisible(False)

        self.centralWidget = QWidget()
        self.layout = QHBoxLayout(self.centralWidget)
        self.layout.addWidget(self.scrollAreaLeft)
        self.layout.addWidget(self.scrollAreaRight)

        self.scrollAreaLeft.verticalScrollBar().valueChanged.connect(
            self.scrollAreaRight.verticalScrollBar().setValue)
        self.scrollAreaLeft.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaRight.horizontalScrollBar().setValue)
        self.scrollAreaRight.verticalScrollBar().valueChanged.connect(
            self.scrollAreaLeft.verticalScrollBar().setValue)
        self.scrollAreaRight.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaLeft.horizontalScrollBar().setValue)

        self.scrollAreaLeft.mouseMoveEvent = self.mouseMoveEventLeft
        self.scrollAreaLeft.mousePressEvent = self.mousePressEventLeft
        self.scrollAreaLeft.mouseReleaseEvent = self.mouseReleaseEventLeft

        self.scrollAreaRight.mouseMoveEvent = self.mouseMoveEventRight
        self.scrollAreaRight.mousePressEvent = self.mousePressEventRight
        self.scrollAreaRight.mouseReleaseEvent = self.mouseReleaseEventRight

        self.imageLabelLeft.setCursor(Qt.OpenHandCursor)
        self.imageLabelRight.setCursor(Qt.OpenHandCursor)

        self.is_load_image_left = False
        self.is_load_image_right = False
        self.log_file_path = '../log.txt'
        self.pressed = False
        self.initialPosX = 0
        self.initialPosY = 0

    def mousePressEventLeft(self, event):
        self.pressed = True
        self.imageLabelLeft.setCursor(Qt.ClosedHandCursor)
        self.initialPosX = self.scrollAreaLeft.horizontalScrollBar().value() + event.pos().x()
        self.initialPosY = self.scrollAreaLeft.verticalScrollBar().value() + event.pos().y()

    def mouseReleaseEventLeft(self, event):
        self.pressed = False
        self.imageLabelLeft.setCursor(Qt.OpenHandCursor)
        self.initialPosX = self.scrollAreaLeft.horizontalScrollBar().value()
        self.initialPosY = self.scrollAreaLeft.verticalScrollBar().value()

    def mouseMoveEventLeft(self, event):
        if self.pressed:
            self.scrollAreaLeft.horizontalScrollBar().setValue(self.initialPosX - event.pos().x())
            self.scrollAreaLeft.verticalScrollBar().setValue(self.initialPosY - event.pos().y())

    def mousePressEventRight(self, event):
        self.pressed = True
        self.imageLabelRight.setCursor(Qt.ClosedHandCursor)
        self.initialPosX = self.scrollAreaRight.horizontalScrollBar().value() + event.pos().x()
        self.initialPosY = self.scrollAreaRight.verticalScrollBar().value() + event.pos().y()

    def mouseReleaseEventRight(self, event):
        self.pressed = False
        self.imageLabelRight.setCursor(Qt.OpenHandCursor)
        self.initialPosX = self.scrollAreaRight.horizontalScrollBar().value()
        self.initialPosY = self.scrollAreaRight.verticalScrollBar().value()

    def mouseMoveEventRight(self, event):
        if self.pressed:
            self.scrollAreaRight.horizontalScrollBar().setValue(self.initialPosX - event.pos().x())
            self.scrollAreaRight.verticalScrollBar().setValue(self.initialPosY - event.pos().y())

    def getPos(self, event):
        msg = '({}, {})'.format(int(event.pos().x() / self.scaleFactor), int(event.pos().y() / self.scaleFactor))
        pyperclip.copy(msg)
        status_msg = '[point] {}'.format(msg)
        self.parent.statusbar.showMessage(status_msg)
        self.writeLog(status_msg)

    def findLocation(self):
        window = FindWindow()

        if window.showModal():
            from_window_x = window.edit_x.text()
            from_window_y = window.edit_y.text()
            centered_x = float(from_window_x) * self.scaleFactor - self.scrollAreaLeft.frameGeometry().width() / 2
            centered_y = float(from_window_y) * self.scaleFactor - self.scrollAreaLeft.frameGeometry().height() / 2
            self.scrollAreaLeft.horizontalScrollBar().setValue(centered_x)
            self.scrollAreaLeft.verticalScrollBar().setValue(centered_y)

            status_msg = '[move] ({}, {})'.format(from_window_x, from_window_y)
            self.parent.statusbar.showMessage(status_msg)
            self.writeLog(status_msg)

    def writeLog(self, message):
        if not os.path.isfile(self.log_file_path):
            print('log file does not exist')
            print('create log file...')
            file_ = open(self.log_file_path, "w")
            file_.close()
            print('file creation : {}'.format(self.log_file_path))

        now = time.localtime()
        with open(self.log_file_path, "a") as file:
            log_ = '{}/{}/{} {}:{} | {}\n'.format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, message)
            file.write(log_)
            file.close()

    def openLeft(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            dir_, file_ = os.path.split(fileName)
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Pruebas de validación", "Cannot load %s." % fileName)
                return

            self.imageLabelLeft.setPixmap(QPixmap.fromImage(image))
            self.imageLabelLeft.mouseDoubleClickEvent = self.getPos
            self.imageLabelLeft.wheelEvent = self.wheel
            self.scaleFactor = 1.0

            self.scrollAreaLeft.setVisible(True)
            self.window.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabelLeft.adjustSize()

            msg = '[left image loaded] {}'.format(file_)
            self.parent.statusbar.showMessage(msg)
            self.writeLog(msg)

            self.is_load_image_left = True
            if self.is_load_image_right:
                self.parent.setWindowTitle(file_)

    def openRight(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            dir_, file_ = os.path.split(fileName)
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Pruebas de validación", "Cannot load %s." % fileName)
                return

            self.imageLabelRight.setPixmap(QPixmap.fromImage(image))
            self.imageLabelRight.mouseDoubleClickEvent = self.getPos
            self.imageLabelRight.wheelEvent = self.wheel
            self.scaleFactor = 1.0

            self.scrollAreaRight.setVisible(True)
            self.window.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabelRight.adjustSize()

            msg = '[right image loaded] {}'.format(file_)
            self.parent.statusbar.showMessage(msg)
            self.writeLog(msg)

            self.is_load_image_right = True
            if self.is_load_image_left:
                self.parent.setWindowTitle(file_)

    def openBoth(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)

        if fileName:
            dir_, file_ = os.path.split(fileName)
            root_dir = os.path.join(dir_, '../')
            image_left = os.path.join(root_dir, 'original', file_)
            image_right = os.path.join(root_dir, 'mask', file_)

            # load left
            image = QImage(image_left)
            if image.isNull():
                QMessageBox.information(self, "Pruebas de validación", "Cannot load %s." % image_left)
                return

            self.imageLabelLeft.setPixmap(QPixmap.fromImage(image))
            self.imageLabelLeft.mouseDoubleClickEvent = self.getPos
            self.imageLabelLeft.wheelEvent = self.wheel
            self.scaleFactor = 1.0

            self.scrollAreaLeft.setVisible(True)

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabelLeft.adjustSize()

            # load right
            image = QImage(image_right)
            if image.isNull():
                QMessageBox.information(self, "Pruebas de validación", "Cannot load %s." % image_right)
                return

            self.imageLabelRight.setPixmap(QPixmap.fromImage(image))
            self.imageLabelRight.mouseDoubleClickEvent = self.getPos
            self.imageLabelRight.wheelEvent = self.wheel
            self.scaleFactor = 1.0

            self.scrollAreaRight.setVisible(True)

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabelRight.adjustSize()

            self.window.fitToWindowAct.setEnabled(True)
            self.updateActions()
            self.parent.setWindowTitle(file_)
            msg = '[both images loaded] {}'.format(file_)
            self.parent.statusbar.showMessage(msg)
            self.writeLog(msg)

    def clear(self):
        self.is_load_image_left = False
        self.is_load_image_right = False

        self.scrollAreaLeft.setVisible(False)
        self.scrollAreaRight.setVisible(False)

        self.parent.setWindowTitle('Pruebas de validación')
        self.parent.statusbar.showMessage('Load images')
        self.writeLog('clear')

    def sleep(self):
        loop = QEventLoop()
        QTimer.singleShot(500, loop.quit)
        loop.exec_()

    def zoomIn(self):
        self.scaleImage(1.25)
        self.parent.statusbar.showMessage('[zoom-in] scale factor : {}'.format(self.scaleFactor))

    def zoomOut(self):
        self.scaleImage(0.8)
        self.parent.statusbar.showMessage('[zoom-out] scale factor : {}'.format(self.scaleFactor))

    def wheel(self, event):
        modifiers = QGuiApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn()
                self.sleep()
            elif event.angleDelta().y() < 0:
                self.zoomOut()
                self.sleep()

    def normalSize(self):
        self.imageLabelLeft.adjustSize()
        self.imageLabelRight.adjustSize()
        self.scaleFactor = 1.0
        self.parent.statusbar.showMessage('[original size] scale factor : {}'.format(self.scaleFactor))

    def about(self):
        QMessageBox.about(self, "Pruebas de validación",
                          "<p>In engineering and its various sub-disciplines, acceptance testing is a test conducted to"
                          " determine if the requirements of a specification or contract are met. "
                          "It may involve chemical tests, physical tests, or performance tests.</p>"
                          "<p>In systems engineering, it may involve black-box testing performed on a system "
                          "(for example: a piece of software, lots of manufactured mechanical parts, "
                          "or batches of chemical products) prior to its delivery.</p>"
                          )

    def updateActions(self):
        self.window.zoomInAct.setEnabled(not self.window.fitToWindowAct.isChecked())
        self.window.zoomOutAct.setEnabled(not self.window.fitToWindowAct.isChecked())
        self.window.normalSizeAct.setEnabled(not self.window.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabelLeft.resize(self.scaleFactor * self.imageLabelLeft.pixmap().size())
        self.imageLabelRight.resize(self.scaleFactor * self.imageLabelRight.pixmap().size())

        self.adjustScrollBar(self.scrollAreaLeft.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollAreaLeft.verticalScrollBar(), factor)
        self.adjustScrollBar(self.scrollAreaRight.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollAreaRight.verticalScrollBar(), factor)

        self.window.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.window.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


class FindWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.pos_y = 100
        self.pos_x = 100
        self.edit_x = QLineEdit()
        self.edit_y = QLineEdit()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('find location')
        self.setGeometry(100, 100, 300, 100)
        layout = QVBoxLayout()
        layout.addStretch(1)
        # x , y
        input_layout = QHBoxLayout()
        label_x = QLabel("x : ")
        self.edit_x.font().setPointSize(15)
        label_y = QLabel("y : ")
        self.edit_y.font().setPointSize(15)
        input_layout.addWidget(label_x)
        input_layout.addWidget(self.edit_x)
        input_layout.addWidget(label_y)
        input_layout.addWidget(self.edit_y)
        layout.addLayout(input_layout)

        # find , cancel
        btn_ok = QPushButton("find")
        btn_ok.clicked.connect(self.onOKButtonClicked)
        btn_cancel = QPushButton("cancel")
        btn_cancel.clicked.connect(self.onCancelButtonClicked)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(btn_ok)
        sub_layout.addWidget(btn_cancel)

        layout.addLayout(sub_layout)
        layout.addStretch(1)
        self.setLayout(layout)

    def onOKButtonClicked(self):
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.imageViewSync = QImageViewSync(self)
        self.setCentralWidget(self.imageViewSync.centralWidget)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Load images')

        self.createActions(self.imageViewSync)
        self.createMenus()

        self.setWindowTitle("Pruebas de validación")
        self.resize(1200, 600)
        self.setWindowIcon(QIcon("../etc/parallel.png"))

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.imageViewSync.scrollAreaLeft.setWidgetResizable(fitToWindow)
        self.imageViewSync.scrollAreaRight.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.imageViewSync.normalSize()

        self.imageViewSync.updateActions()

    def createActions(self, view):
        self.openLeftAct = QAction("&Open Left...", self, shortcut="Ctrl+L", triggered=view.openLeft)
        self.openRightAct = QAction("&Open Right...", self, shortcut="Shift+Ctrl+L", triggered=view.openRight)
        self.openBothAct = QAction("&Open Both...", self, shortcut="Shift+Ctrl+O", triggered=view.openBoth)
        self.clearAct = QAction("&Clear...", self, shortcut="Shift+R", triggered=view.clear)

        self.findAct = QAction("&Find...", self, shortcut="Ctrl+F", triggered=view.findLocation)

        # self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=image.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl+I", enabled=False, triggered=view.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+O", enabled=False, triggered=view.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=view.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self,
                                      enabled=False, checkable=True, shortcut="Ctrl+T", triggered=self.fitToWindow)
        self.aboutAct = QAction("&About", self, triggered=view.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openLeftAct)
        self.fileMenu.addAction(self.openRightAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.openBothAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.clearAct)
        self.fileMenu.addSeparator()
        # self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.findAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())