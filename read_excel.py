#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd as xl


class ExcelReader:

	def __init__(self, file):
		self.pointSheetObj = []
		self.sheet_names = []
		self.file = file
		self._matrix = {}
		self.work_book = None


	def get_sheets_names(self):
		if len(self.sheet_names) > 0:
			return self.sheet_names

		self.work_book = xl.open_workbook(self.file)
		dir(self.work_book.sheet_by_name(self.work_book.sheet_names()[0]))
		self.sheet_names = self.work_book.sheet_names()
		return self.sheet_names

	def get_sheet_matrix(self, name):
		if name not in self.get_sheets_names():
			return None

		t = self._matrix.get(name, None)
		if t is not None and len(t) > 0:
			return t

		sheet = self.work_book.sheet_by_name(name)
		self._matrix[name] = []
		for row in range (sheet.nrows):
			_row = []
			for col in range (sheet.ncols):
				_row.append(sheet.cell_value(row,col))
			self._matrix[name].append(_row)
		return self._matrix[name]

if __name__ == '__main__':
	er = ExcelReader('/Users/david/Downloads/excel1.xlsx')
	print (er.get_sheets_names())
	print (er.get_sheet_matrix('Sheet1'))











	
