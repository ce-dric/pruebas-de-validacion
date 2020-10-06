#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QWidget, QHBoxLayout

import os


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
        self.parent.statusbar.showMessage(
            '{} , {}'.format(event.pos().x() / self.scaleFactor, event.pos().y() / self.scaleFactor)
        )

    def openLeft(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            print(fileName)
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Pruebas de validación", "Cannot load %s." % fileName)
                return

            self.imageLabelLeft.setPixmap(QPixmap.fromImage(image))
            self.imageLabelLeft.mouseDoubleClickEvent = self.getPos
            self.scaleFactor = 1.0

            self.scrollAreaLeft.setVisible(True)
            self.window.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabelLeft.adjustSize()

    def openRight(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            print(fileName)
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Pruebas de validación", "Cannot load %s." % fileName)
                return

            self.imageLabelRight.setPixmap(QPixmap.fromImage(image))
            self.imageLabelRight.mouseDoubleClickEvent = self.getPos
            self.scaleFactor = 1.0

            self.scrollAreaRight.setVisible(True)
            self.window.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabelRight.adjustSize()

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

            # for left
            print('left : ', image_left)
            image = QImage(image_left)
            if image.isNull():
                QMessageBox.information(self, "Pruebas de validación", "Cannot load %s." % image_left)
                return

            self.imageLabelLeft.setPixmap(QPixmap.fromImage(image))
            self.imageLabelLeft.mouseDoubleClickEvent = self.getPos
            self.scaleFactor = 1.0

            self.scrollAreaLeft.setVisible(True)

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabelLeft.adjustSize()

            # for right
            print('right : ', image_right)
            image = QImage(image_right)
            if image.isNull():
                QMessageBox.information(self, "Pruebas de validación", "Cannot load %s." % image_right)
                return

            self.imageLabelRight.setPixmap(QPixmap.fromImage(image))
            self.imageLabelRight.mouseDoubleClickEvent = self.getPos
            self.scaleFactor = 1.0

            self.scrollAreaRight.setVisible(True)

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabelRight.adjustSize()

            self.window.fitToWindowAct.setEnabled(True)
            self.updateActions()

    def clear(self):
        self.scrollAreaLeft.setVisible(False)
        self.scrollAreaRight.setVisible(False)
        self.parent.statusbar.showMessage('Ready')

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabelLeft.adjustSize()
        self.imageLabelRight.adjustSize()
        self.scaleFactor = 1.0

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.imageViewSync = QImageViewSync(self)
        self.setCentralWidget(self.imageViewSync.centralWidget)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        self.createActions(self.imageViewSync)
        self.createMenus()

        self.setWindowTitle("Pruebas de validación")
        self.resize(1200, 600)


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
        self.closeAct = QAction("&Close...", self, shortcut="Shift+R", triggered=view.clear)

        # self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=image.close)
        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl+I", enabled=False, triggered=view.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+O", enabled=False, triggered=view.zoomOut)
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=view.normalSize)
        self.fitToWindowAct = QAction("&Fit to Window", self,
                                      enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
        self.aboutAct = QAction("&About", self, triggered=view.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openLeftAct)
        self.fileMenu.addAction(self.openRightAct)
        self.fileMenu.addAction(self.openBothAct)
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addSeparator()
        # self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

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