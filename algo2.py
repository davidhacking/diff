#!/usr/bin/python
# -*- utf-8 -*-

import time
import sys
import algo

def cmp(a, b):
		return (a > b) - (a < b)

def lcs(A, B, lenA, lenB):
	result = 0
	if lenA == 0 or lenB == 0:
		result
	elif A[0] == B[0]:
		result = 1 + lcs(A[1:lenA], B[1:lenB], lenA - 1, lenB - 1)
	else:
		result = max(lcs(A, B[1:lenB], lenA, lenB - 1), lcs(A[1:lenA], B, lenA - 1, lenB))
	return result

def lcsV2(A, B):
	sup = []
	m = len(A) + 1
	n = len(B) + 1
	for i in range(m):
		sup.append([])
		for j in range(n):
			sup[i].append(0)
	for i in range(1, m):
		for j in range(1, n):
			if A[i - 1] == B[j - 1]:
				sup[i][j] = sup[i - 1][j - 1] + 1
			elif sup[i - 1][j] >= sup[i][j - 1]:
				sup[i][j] = sup[i - 1][j]
			else:
				sup[i][j] = sup[i][j - 1]
	return sup[m - 1][n - 1]

def lcsV3(A, B):

	if cmp(A, B) == 0:
		return len(A)
	else:
		lcsValue = lcsV2(A, B)
		return lcsValue

def transformMatrix(a):
	am = len(a)
	an = 0 if am <= 0 else len(a[0])
	aTransMat = []
	for i in range(an):
		aTransMat.append([row[i] for row in a])
	return aTransMat

def calcColMapTable(a, b):
	return calcRowMapTable(transformMatrix(a), transformMatrix(b))

def calcRowMapTable(a, b):
	"""
	key: value
	row number in a: row number in b
	"""
	rowMapTable = {}
	rowLcsTable = []
	am = len(a)
	an = 0 if am <= 0 else len(a[0])
	bm = len(b)
	bn = 0 if bm <= 0 else len(b[0])
	if am <= 0 or bm <= 0:
		return rowMapTable
	dp = []
	for i in range(am):
		rowLcsTable.append([])
		dp.append([])
		for j in range(bm):
			lcsValue = lcsV3(a[i], b[j])
			rowLcsTable[i].append(lcsValue)
			dp[i].append({})
	# print("rowLcsTable", rowLcsTable)
	maxValueForword = rowLcsTable[0][0]
	dp[0][0] = {"value": maxValueForword, "from": ''}
	for i in range(1, am):
		if rowLcsTable[i][0] <= maxValueForword:
			dp[i][0] = {"value": maxValueForword, "from": 'top'}
		else:
			maxValueForword = rowLcsTable[i][0]
			dp[i][0] = {"value": maxValueForword, "from": ''}
	maxValueForword = rowLcsTable[0][0]
	for j in range(1, bm):
		if rowLcsTable[0][j] <= maxValueForword:
			dp[0][j] = {"value": maxValueForword, "from": 'left'}
		else:
			maxValueForword = rowLcsTable[0][j]
			dp[0][j] = {"value": maxValueForword, "from": ''}
	for i in range(1, am):
		for j in range(1, bm):
			tmpVlaue = dp[i-1][j-1]["value"] + rowLcsTable[i][j]
			maxValue = max(max(dp[i-1][j]["value"], dp[i][j-1]["value"]), tmpVlaue)
			dp[i][j]["value"] = maxValue
			if maxValue == dp[i-1][j]["value"]:
				dp[i][j]["from"] = 'top'
			elif maxValue == dp[i][j-1]["value"]:
				dp[i][j]["from"] = 'left'
			else:
				dp[i][j]["from"] = 'TL'
	# print("dp", dp)
	i = am - 1
	j = bm - 1
	while True:
		if dp[i][j]["from"] == '':
			if rowLcsTable[i][j] > 0:
				rowMapTable[i] = j
			# print i, j
			break
		elif dp[i][j]["from"] == 'top':
			i = i - 1
		elif dp[i][j]["from"] == 'left':
			j = j - 1
		else:
			# print i, j, dp[i][j], rowLcsTable[i][j], "in else"
			if rowLcsTable[i][j] > 0:
				rowMapTable[i] = j
			i = i - 1
			j = j - 1

	return rowMapTable

def colMed(a, b, colMapTable):
	return rowMed(transformMatrix(a), transformMatrix(b), colMapTable)

def rowMed(a, b, rowMapTable):
	a2b = []
	row_ins_A2b, row_ins_a2A = {}, {}
	op = []
	row_del = []
	for i in range(len(a) + 1):
		a2b.append([])
		for j in range(len(b) + 1):
			a2b[i].append({})
			if i == 0 and j == 0:
				a2b[i][j] = {"dis": 0, "from": ''}
			elif i == 0 and j != 0:
				a2b[i][j] = {"dis": j, "from": 'left'}
			elif i != 0 and j == 0:
				a2b[i][j] = {"dis": i, "from": 'top'}
	for i in range(len(a)):
		for j in range(len(b)):
			x = a2b[i][j+1]["dis"] + 1
			y = a2b[i+1][j]["dis"] + 1
			z = a2b[i][j]["dis"] if rowMapTable.get(i, None) == j else a2b[i][j]["dis"] + 2
			m = min(min(x, y), z)
			a2b[i+1][j+1]["dis"] = m
			if m == x:
				a2b[i+1][j+1]["from"] = 'top'
			elif m == y:
				a2b[i+1][j+1]["from"] = 'left'
			else:
				a2b[i+1][j+1]["from"] = 'TL'
	path = []
	i = len(a)
	j = len(b)
	while i >= 0 and j >= 0:
		if a2b[i][j]["from"] == 'TL':
			path.insert(0, (i, j))
			i = i - 1
			j = j - 1
		elif a2b[i][j]["from"] == 'top':
			path.insert(0, (i, j))
			i = i - 1
		elif a2b[i][j]["from"] == 'left':
			path.insert(0, (i, j))
			j = j - 1
		else:
			break
	for k in range(len(path)):
		if a2b[path[k][0]][path[k][1]]["from"] == 'TL':
			op.append(0)
		elif a2b[path[k][0]][path[k][1]]["from"] == 'top':
			op.append(-1)
			row_del.append(k)
		elif a2b[path[k][0]][path[k][1]]["from"] == 'left':
			op.append(1)
			row_ins_A2b[k] = path[k][1]
		row_ins_a2A[path[k][0]] = k
	return op, row_ins_A2b, row_ins_a2A, row_del


def diffA2B(a, b):
	t1 = time.clock()
	colMapTable = calcColMapTable(a, b)
	t2 = time.clock()
	# print("calcColMapTable time: ", t2 - t1)
	rowMapTable = calcRowMapTable(a, b)
	t3 = time.clock()
	# print("calcRowMapTable", t3 - t2)
	rowOp, row_ins_A2b, row_ins_a2A, row_del = rowMed(a, b, rowMapTable)
	t4 = time.clock()
	# print("rowMed: ", t4 - t3)
	colOp, col_ins_A2b, col_ins_a2A, col_del = colMed(a, b, colMapTable)
	t5 = time.clock()
	# print("colMed: ", t5 - t4)
	# cell {value:, color: w for white r for red b for blue y for yellow}
	retMat = []
	cell_diff_a2A, cell_diff_A2a, cell_diff_a2b = {}, {}, {}
	x = 0
	t6 = time.clock()
	for i in range(len(rowOp)):
		row = []
		y = 0
		for j in range(len(colOp)):
			cell = {}
			if rowOp[i] == 0:
				if colOp[j] == 0:
					cell["value"] = a[x][y]
					if a[x][y] == b[rowMapTable[x]][colMapTable[y]]:
						cell["color"] = 'w'
					else:
						cell_diff_a2A[(x, y)] = (i, j)
						cell_diff_A2a[(i, j)] = (x, y)
						cell_diff_a2b[(x, y)] = (rowMapTable[x], colMapTable[y])
						cell["color"] = 'y'
				elif colOp[j] == -1:
					cell["value"] = a[x][y]
					cell["color"] = 'r'
				elif colOp[j] == 1:
					cell["value"] = ''
					cell["color"] = 'b'
			if rowOp[i] == -1:
				if colOp[j] == 0:
					cell["value"] = a[x][y]
					cell["color"] = 'r'
				elif colOp[j] == -1:
					cell["value"] = a[x][y]
					cell["color"] = 'r'
				elif colOp[j] == 1:
					cell["value"] = ''
					cell["color"] = 'b'
			if rowOp[i] == 1:
				if colOp[j] == 0 or colOp[j] == 1:
					cell["value"] = ''
					cell["color"] = 'b'
				elif colOp[j] == -1:
					cell["value"] = ''
					cell["color"] = 'r'
			if colOp[j] == 0 or colOp[j] == -1:
				y = y + 1
			row.append(cell)
		if rowOp[i] == 0 or rowOp[i] == -1:
			x = x + 1
		retMat.append(row)
	# print("last for circle: ", t6 - t5)
	return retMat, cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, row_ins_A2b, row_ins_a2A, col_ins_A2b, col_ins_a2A, row_del, col_del

def get_cell_diff_A2B(cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, cell_diff_b2B, cell_diff_B2b, cell_diff_b2a):
	cell_diff_A2B = []
	for k, v in cell_diff_a2b.items():
		try:
			x = cell_diff_a2A[k]
			y = cell_diff_b2B[v]
			cell_diff_A2B.append([[x[0], x[1]], [y[0], y[1]]])
		except KeyError:
			pass
	return cell_diff_A2B

def getExtraCellDiff(a, b):
	extraCellDiff = []
	am, bm = len(a), len(b)
	an = 0 if am <= 0 else len(a[0])
	bn = 0 if bm <= 0 else len(b[0])

	if am < bm or an < bn:
		for i in range(len(b)):
			for j in range(len(b[0])):
				if b[i][j] is not None and b[i][j] != '' and (i >= am or j >= an):
					extraCellDiff.append([[i, j], [i, j]])
	if bm < am or bn < an:
		for i in range(len(a)):
			for j in range(len(a[0])):
				if a[i][j] is not None and a[i][j] != '' and (i >= bm or j >= bn):
					extraCellDiff.append([[i, j], [i, j]])
	return extraCellDiff

def get_ins_A2B(ins_A2b, ins_a2A, ins_B2a, ins_b2B):
	# print ins_A2b, ins_a2A, ins_B2a, ins_b2B
	ins_A2B = []
	for k, v in ins_A2b.items():
		ins_A2B.append([k, ins_b2B[v]])
	return ins_A2B

def computeArea(m, n, rows, cols):
	s = m * n
	sr = 0
	sc = 0
	for i in range(len(rows)):
		sr = sr + n
	for i in range(len(cols)):
		sc = sc + m
	# print ("computeArea")
	# print (s, sr, sc)
	if sr == sc and s == sr and s == sc:
		return (rows, []) if len(rows) <= len(cols) else ([], cols)
	else:
		return (rows, cols)

def getCompareData(a, b, f1name, f2name, fn):
	data = {}
	data["table1"] = {}
	data["table1"]["name"] = f1name + '[' + fn + ']'
	data["table2"] = {}
	data["table2"]["name"] = f2name + '[' + fn + ']'

	# use min edit distance to compare the row one or column one
	flag = -1
	if len(a) == 1 and len(b) == 1:
		flag = 0
	elif (len(a) > 0 and len(a[0]) == 1) and (len(b) > 0 and len(b[0]) == 1):
		flag = 1

	if flag == -1:
		tmpTable1Data = diffA2B(a, b)
		tmpTable2Data = diffA2B(b, a)
	else:
		tmpTable1Data = algo.deltaA2B(a, b, algo.med(a, b, flag), flag)
		tmpTable2Data = algo.deltaA2B(b, a, algo.med(b, a, flag), flag)

	data["table1"]["data"], cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, row_ins_A2b, row_ins_a2A, col_ins_A2b, col_ins_a2A, row_del_A, col_del_A = tmpTable1Data
	data["table2"]["data"], cell_diff_b2B, cell_diff_B2b, cell_diff_b2a, row_ins_B2a, row_ins_b2B, col_ins_B2a, col_ins_b2B, row_del_B, col_del_B = tmpTable2Data
	
	dataRowLen = len(data["table1"]["data"])
	dataColLen = 0 if dataRowLen == 0 else len(data["table1"]["data"][0])

	data["cell_diff_A2B"] = get_cell_diff_A2B(cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, cell_diff_b2B, cell_diff_B2b, cell_diff_b2a)
	data["extraCellDiff"] = getExtraCellDiff(a, b)
	
	row_ins_A = get_ins_A2B(row_ins_A2b, row_ins_a2A, row_ins_B2a, row_ins_b2B)
	col_ins_A = get_ins_A2B(col_ins_A2b, col_ins_a2A, col_ins_B2a, col_ins_b2B)
	u, v = computeArea(dataRowLen, dataColLen, row_ins_A, col_ins_A)
	x, y = computeArea(dataRowLen, dataColLen, row_del_A, col_del_A)
	data["table1"]["row_ins"] = u
	data["table1"]["col_ins"] = v
	data["table2"]["row_ins"] = get_ins_A2B(row_ins_B2a, row_ins_b2B, row_ins_A2b, row_ins_a2A)
	data["table2"]["col_ins"] = get_ins_A2B(col_ins_B2a, col_ins_b2B, col_ins_A2b, col_ins_a2A)

	data["table1"]["row_del"] = x
	data["table1"]["col_del"] = y
	data["table2"]["row_del"] = row_del_B
	data["table2"]["col_del"] = col_del_B
	return data

a = [
		['a', 'b', 'c'],
		['d', 'e', 'f'],
		['g', 'h', 'i'],
	]
b = [
		['a', 'b', 'c'],
		['d', 'e', 'f'],
		['x', 'y', 'j'],
	]


c = [
		['Col-1', 'Col-2', 'Col-3', 'Col-4', 'Col-5', 'Col-6'],
		['v-1-1', 'v-1-2', 'v-1-3', 'v-1-4', 'v-1-5', 'v-1-6'],
		['v-2-1', 'v-2-2', 'v-2-3', 'v-2-4', 'v-2-5', 'v-2-6'],
		['v-3-1', 'v-3-2', 'v-3-3', 'v-3-4', 'v-3-5', 'v-3-6'],
		['v-4-1', 'v-4-2', 'v-4-3', 'v-4-4', 'v-4-5', 'v-4-6'],
		['v-5-1', 'v-5-2', 'v-5-3', 'v-5-4', 'v-5-5', 'v-5-6']
	]


d = [
		['Col-1', 'Col-2', 'Col-3', 'Col-4', 'Col-5', 'Col-7'],
		['v-1-1', 'v-1-2', 'v-1-3', 'v-1-4', 'v-1-5', 'v-1-7'],
		['v-2-1', 'v-2-2', 'v-9-3', 'v-8-4', 'v-2-5', 'v-2-7'],
		['v-3-1', 'v-3-2', 'v-3-3', 'v-3-4', 'v-7-5', 'v-3-7'],
		['v-5-1', 'v-5-2', 'v-5-3', 'v-5-4', 'v-5-5', 'v-5-7'],
		['v-6-1', 'v-6-2', 'v-6-3', 'v-6-4', 'v-6-5', 'v-6-7'],
	]

e = [[u'A', u'B', u'C', u'D', u'A', u'B', u'D']]

f = [[u'B', u'B', u'C', u'', u'A', u'B', u'C', u'D', u'A', u'B', u'', u'A', u'B', u'C', u'D', u'A', u'B', u'C', u'D', u'A', u'B', u'D', u'E']]


if __name__ == "__main__":
	print("cd", getCompareData(c, d, '', '', ''))
	print()
	print("ef", getCompareData(e, f, '', '', ''))













