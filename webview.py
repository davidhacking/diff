#!/usr/bin/python
 
import PyQt5
from PyQt5.QtCore import QUrl 
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *
from PyQt5.QtWebEngineCore import *
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

wd = os.getcwd()
app = QApplication(sys.argv) 
view = Browser()
view.showMaximized()
view.load("file://" + wd + "/test.html")
app.exec_()