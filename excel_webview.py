#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import PyQt5
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
# from PyQt5.QtWebKitWidgets import QWebView , QWebPage
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngineCore import *
# from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtNetwork import *
import sys
from optparse import OptionParser
import os
 
 
class MyBrowser(QWebEnginePage):
	''' Settings for the browser.'''
 
	def userAgentForUrl(self, url):
		''' Returns a User Agent that will be seen by the website. '''
		return "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
 
class Browser(QWebEngineView):
	def __init__(self):
		# QWebView
		self.view = QWebEngineView.__init__(self)
		#self.view.setPage(MyBrowser())
		self.setWindowTitle('Loading...')
		self.titleChanged.connect(self.adjustTitle)
		#super(Browser).connect(self.ui.webView,QtCore.SIGNAL("titleChanged (const QString&)"), self.adjustTitle)
 
	def load(self,url):  
		self.setUrl(QUrl(url)) 
 
	def adjustTitle(self):
		self.setWindowTitle(self.title())
 
	def disableJS(self):
		settings = QWebEngineSettings.globalSettings()
		settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)

class CallHandler(QObject):
	@pyqtSlot()
	def test(self):
		print('call received')

"""
python call js
def js_callback(result):
	print(result)

def complete_name():
	view.page().runJavaScript('completeAndReturnName();', js_callback)

js call python
https://stackoverflow.com/questions/39544089/how-can-i-access-python-code-from-javascript-in-pyqt-5-7
"""

class CompExcel(QWidget):
	def __init__(self):
		super(CompExcel,self).__init__()
		mainLayout = QVBoxLayout()
		hboxLayout = QHBoxLayout()		
		self.creatChooseFileBox()
		hboxLayout.addWidget(self.chooseFileBox)
		self.createCompView()
		hboxLayout.addWidget(self.compView)
		mainLayout.addLayout(hboxLayout)
		self.setLayout(mainLayout)

	def createCompView(self):
		self.compView = Browser()
		channel = QWebChannel()
		handler = CallHandler()
		channel.registerObject('handler', handler)
		self.compView.page().setWebChannel(channel)
		self.compView.load("file://" + os.getcwd() + "/view_excel.html")
		self.compView.showMaximized()

	def creatChooseFileBox(self):
		self.chooseFileBox = QGroupBox("Vbox layout")
		layout = QVBoxLayout() 
		# nameLabel = QLabel("tile")
		# bigEditor = QTextEdit()
		# bigEditor.setPlainText("this is the text")
		self.btn1 = QPushButton("file1")
		self.btn1.clicked.connect(self.getfile)
		self.btn2 = QPushButton("file2")
		self.btn2.clicked.connect(self.getfile)
		layout.addWidget(self.btn1)
		layout.addWidget(self.btn2)
		self.chooseFileBox.setLayout(layout)

	def getfile(self):
		fname = QFileDialog.getOpenFileName(self, 'Open file', '/Users/david/Downloads',"Excel files (*.xlsx *.xls)")
		print fname


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = CompExcel()
	ex.showMaximized()
	ex.show()
	sys.exit(app.exec_())


# wd = os.getcwd()
# app = QApplication(sys.argv) 
# view = Browser()
# channel = QWebChannel()
# handler = CallHandler()
# channel.registerObject('handler', handler)
# view.page().setWebChannel(channel)

# view.showMaximized()
# view.load("file://" + wd + "/view_excel.html")
# # view.page().runJavaScript("alert('hehe')")

# app.exec_()