#!/usr/bin/python
# -*- utf-8 -*-

import time
import sys

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
			if A[i - 1] == B[j - 1] and A[i - 1] != '' and B[j - 1] != '':
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
		return lcsV2(A, B)

def column(matrix, i):
    return [row[i] for row in matrix]


def calc_row_status_table(a, b):
	rst = {};
	i = 0;
	for x in range(len(a)):
		res = [0, -1]
		for y in range(i, len(b)):
			lenA = len(a[x])
			lenB = len(b[y])
			# print lenA, lenB
			# t = lcs(a[x], b[y], lenA, lenB)
			t = lcsV3(a[x], b[y])
			if res[0] < t:
				res[0] = t
				res[1] = y
			if t == lenA or t == lenB:
				break
		if res[0] > 0:
			rst[x] = [res[1], res[0]]
			i = res[1] + 1
	return rst

def calc_col_status_table(a, b):
	cst = {};
	i = 0;
	if len(a) > 0:
		for x in range(len(a[0])):
			res = [0, -1]
			if len(b) > 0:
				for y in range(i, len(b[0])):
					lenA = len(column(a, x))
					lenB = len(column(b, y))
					# t = lcs(column(a, x), column(b, y), lenA, lenB)
					t = lcsV3(column(a, x), column(b, y))
					if res[0] < t:
						res[0] = t
						res[1] = y
					if t == lenA or t == lenB:
						break
				if res[0] > 0:
					cst[x] = [res[1], res[0]]
					i = res[1] + 1
	return cst

def calc_row_status(a, b):
	# 0 for normal, 1 for insert, -1 for delete
	row_convert_info = []
	start = time.clock()
	rst = calc_row_status_table(a, b)
	row_ins_A2b = {}
	row_ins_a2A = {}
	row_del = []
	x = -1
	for i in range(len(a)):
		t = rst.get(i, None)
		if t is None:
			row_convert_info.append(-1)
			row_del.append(len(row_convert_info) - 1)
		elif t[0] <= i:
			row_convert_info.append(0)
			x = t[0]
		elif t[0] > i:
			for y in range(x + 1, t[0]):
				row_convert_info.append(1)
				row_ins_A2b[len(row_convert_info) - 1] = y
			row_convert_info.append(0)
			x = t[0]
		row_ins_a2A[i] = len(row_convert_info) - 1
	for j in range(x + 1, len(b)):
		row_convert_info.append(1)
		row_ins_A2b[len(row_convert_info) - 1] = j
	return row_convert_info, rst, row_ins_A2b, row_ins_a2A, row_del


def calc_col_status(a, b):
	# 0 for normal, 1 for insert, -1 for delete
	col_convert_info = []
	cst = calc_col_status_table(a, b)
	# print cst
	col_ins_A2b = {}
	col_ins_a2A = {}
	col_del = []
	x = -1
	if len(a) > 0:
		for i in range(len(a[0])):
			t = cst.get(i, None)
			if t is None:
				col_convert_info.append(-1)
				col_del.append(len(col_convert_info) - 1)
			elif t[0] <= i:
				col_convert_info.append(0)
				x = t[0]
			elif t[0] > i:
				for y in range(x + 1, t[0]):
					col_convert_info.append(1)
					col_ins_A2b[len(col_convert_info) - 1] = y
				col_convert_info.append(0)
				x = t[0]
			col_ins_a2A[i] = len(col_convert_info) - 1
	if len(b) > 0:
		for j in range(x + 1, len(b[0])):
			col_convert_info.append(1)
			col_ins_A2b[len(col_convert_info) - 1] = j
	return col_convert_info, cst, col_ins_A2b, col_ins_a2A, col_del

def get_diff_matrix(a, b):
	t1 = time.clock()
	rs, rst, row_ins_A2b, row_ins_a2A, row_del = calc_row_status(a, b)
	t2 = time.clock()
	elapsed = (t2 - t1)
	print ('calc_row_status time: ', elapsed)
	cs, cst, col_ins_A2b, col_ins_a2A, col_del = calc_col_status(a, b)
	t3 = time.clock()
	elapsed = (t3 - t2)
	print ('calc_col_status time: ', elapsed)
	print ("rs, rst")
	print (rs, rst)
	print ("cs, cst")
	print (cs, cst)
	# cell {value:, color: w for white r for red b for blue y for yellow}
	ret_mat = []
	cell_diff_a2A = {}
	cell_diff_A2a = {}
	cell_diff_a2b = {}
	x = 0
	for i in range(len(rs)):
		row = []
		y = 0
		for j in range(len(cs)):
			cell = {}
			if rs[i] == 0:
				if cs[j] == 0:
					cell["value"] = a[x][y]
					if a[x][y] == b[rst[x][0]][cst[y][0]]:
						cell["color"] = 'w'
					else:
						cell_diff_a2A[(x, y)] = (i, j)
						cell_diff_A2a[(i, j)] = (x, y)
						cell_diff_a2b[(x, y)] = (rst[x][0], cst[y][0])
						cell["color"] = 'y'
				elif cs[j] == -1:
					cell["value"] = a[x][y]
					cell["color"] = 'r'
				elif cs[j] == 1:
					cell["value"] = ''
					cell["color"] = 'b'
			if rs[i] == -1:
				if cs[j] == 0:
					cell["value"] = a[x][y]
					cell["color"] = 'r'
				elif cs[j] == -1:
					cell["value"] = a[x][y]
					cell["color"] = 'r'
				elif cs[j] == 1:
					cell["value"] = ''
					cell["color"] = 'b'
			if rs[i] == 1:
				if cs[j] == 0 or cs[j] == 1:
					cell["value"] = ''
					cell["color"] = 'b'
				elif cs[j] == -1:
					cell["value"] = ''
					cell["color"] = 'r'
			if cs[j] == 0 or cs[j] == -1:
				y = y + 1
			row.append(cell)
		if rs[i] == 0 or rs[i] == -1:
			x = x + 1
		ret_mat.append(row)
	return ret_mat, cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, row_ins_A2b, row_ins_a2A, col_ins_A2b, col_ins_a2A, row_del, col_del

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

# handle cell diff when row or cell is zero
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

def cellData(a, i, flag):
	if flag == 0:
		return a[0][i]
	else:
		return a[i][0]

def myLen(a, flag):
	if flag == 0:
		return len(a[0])
	else:
		return len(a)

def med(a, b, flag):
	a2b = []
	for i in range(myLen(a, flag) + 1):
		a2b.append([])
		for j in range(myLen(b, flag) + 1):
			a2b[i].append({})
			if i == 0 and j == 0:
				a2b[i][j] = {"dis": 0, "from": ''}
			elif i == 0 and j != 0:
				a2b[i][j] = {"dis": j, "from": 'left'}
			elif i != 0 and j == 0:
				a2b[i][j] = {"dis": i, "from": 'top'}
	for i in range(myLen(a, flag)):
		for j in range(myLen(b, flag)):
			x = a2b[i][j+1]["dis"] + 1
			y = a2b[i+1][j]["dis"] + 1
			z = a2b[i][j]["dis"] + 1 if cellData(a, i, flag) != cellData(b, j, flag) else a2b[i][j]["dis"]
			m = min(min(x, y), z)
			a2b[i+1][j+1]["dis"] = m
			if m == x:
				a2b[i+1][j+1]["from"] = 'top'
			elif m == y:
				a2b[i+1][j+1]["from"] = 'left'
			else:
				a2b[i+1][j+1]["from"] = 'TL'
	op = []
	i = myLen(a, flag)
	j = myLen(b, flag)
	while i >= 0 and j >= 0:
		if a2b[i][j]["from"] == 'TL':
			i = i - 1
			j = j - 1
			op.insert(0, 0)
		elif a2b[i][j]["from"] == 'top':
			i = i - 1
			op.insert(0, -1)
		elif a2b[i][j]["from"] == 'left':
			j = j - 1
			op.insert(0, 1)
		else:
			break
	return op

def deltaA2B(a, b, op, flag):
	i, j = 0, 0
	delta = []
	cell_diff_a2b = {}
	A2a = {}
	a2A = {}
	row_ins_A2b = {}
	row_ins_a2A = {}
	col_ins_A2b = {}
	col_ins_a2A = {}
	row_del = []
	col_del = []
	for k in range(len(op)):
		cell = {}
		if op[k] == 0:
			if cellData(a, i, flag) == cellData(b, j, flag):
				cell["value"] = cellData(a, i, flag)
				cell["color"] = 'w'
			else:
				cell["value"] = cellData(a, i, flag)
				cell["color"] = 'y'
				cell_diff_a2b[(0, i) if flag == 0 else (i, 0)] = (0, j) if flag == 0 else (j, 0)
			a2A[(0, i) if flag == 0 else (i, 0)] = (0, k) if flag == 0 else (k, 0)
			A2a[(0, k) if flag == 0 else (k, 0)] = (0, i) if flag == 0 else (i, 0)
			if flag == 0:
				col_ins_a2A[i] = k
			else:
				row_ins_a2A[i] = k
			i = i + 1
			j = j + 1
		elif op[k] == 1:
			cell["value"] = ''
			cell["color"] = 'b'
			if flag == 0:
				col_ins_A2b[k] = j
			else:
				row_ins_A2b[k] = j
			j = j + 1
		elif op[k] == -1:
			cell["value"] = cellData(a, i, flag)
			cell["color"] = 'r'
			a2A[(0, i) if flag == 0 else (i, 0)] = (0, k) if flag == 0 else (k, 0)
			A2a[(0, k) if flag == 0 else (k, 0)] = (0, i) if flag == 0 else (i, 0)
			if flag == 0:
				col_ins_a2A[i] = k
			else:
				row_ins_a2A[i] = k
			i = i + 1
			if flag == 0:
				col_del.append(k)
			else:
				row_del.append(k)
		if flag == 0:
			delta.append(cell)
		else:
			delta.append([cell])
	if flag == 0:
		ret = []
		ret.append(delta)
		delta = ret
	return delta, cell_diff_a2b, a2A, A2a, row_ins_A2b, row_ins_a2A, col_ins_A2b, col_ins_a2A, row_del, col_del

def computeArea(m, n, rows, cols):
	s = m * n
	sr = 0
	sc = 0
	for i in range(len(rows)):
		sr = sr + n
	for i in range(len(cols)):
		sc = sc + m
	print ("computeArea")
	print (s, sr, sc)
	if sr == sc and s == sr and s == sc:
		return (rows, []) if len(rows) < len(cols) else ([], cols)
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
		tmpTable1Data = get_diff_matrix(a, b)
		tmpTable2Data = get_diff_matrix(b, a)
	else:
		tmpTable1Data = deltaA2B(a, b, med(a, b, flag), flag)
		tmpTable2Data = deltaA2B(b, a, med(b, a, flag), flag)

	data["table1"]["data"], cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, row_ins_A2b, row_ins_a2A, col_ins_A2b, col_ins_a2A, row_del_A, col_del_A = tmpTable1Data
	data["table2"]["data"], cell_diff_b2B, cell_diff_B2b, cell_diff_b2a, row_ins_B2a, row_ins_b2B, col_ins_B2a, col_ins_b2B, row_del_B, col_del_B = tmpTable2Data
	dataRowLen = len(data["table1"]["data"])
	dataColLen = 0 if dataRowLen == 0 else len(data["table1"]["data"][0])
	data["cell_diff_A2B"] = get_cell_diff_A2B(cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, cell_diff_b2B, cell_diff_B2b, cell_diff_b2a)
	data["extraCellDiff"] = getExtraCellDiff(a, b) if flag == -1 else []
	row_ins_A = get_ins_A2B(row_ins_A2b, row_ins_a2A, row_ins_B2a, row_ins_b2B)
	col_ins_A = get_ins_A2B(col_ins_A2b, col_ins_a2A, col_ins_B2a, col_ins_b2B)
	u, v = computeArea(dataRowLen, dataColLen, row_ins_A, col_ins_A)
	data["table1"]["row_ins"] = u
	data["table1"]["col_ins"] = v
	
	data["table1"]["row_del"] = row_del_A
	data["table1"]["col_del"] = col_del_A
	data["table2"]["row_ins"] = get_ins_A2B(row_ins_B2a, row_ins_b2B, row_ins_A2b, row_ins_a2A)
	data["table2"]["col_ins"] = get_ins_A2B(col_ins_B2a, col_ins_b2B, col_ins_A2b, col_ins_a2A)
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
	x, cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, row_ins_A2b, row_ins_a2A, col_ins_A2b, col_ins_a2A, row_del_A, col_del_A = deltaA2B(e, f, med(e, f, 0), 0)
	y, cell_diff_b2B, cell_diff_B2b, cell_diff_b2a, row_ins_B2a, row_ins_b2B, col_ins_B2a, col_ins_b2B, row_del_B, col_del_B = deltaA2B(f, e, med(f, e, 0), 0)
	print ("get_cell_diff_A2B")
	print (get_cell_diff_A2B(cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, cell_diff_b2B, cell_diff_B2b, cell_diff_b2a))
	print (get_ins_A2B(row_ins_A2b, row_ins_a2A, row_ins_B2a, row_ins_b2B))
	print (get_ins_A2B(row_ins_B2a, row_ins_b2B, row_ins_A2b, row_ins_a2A))
	print (get_ins_A2B(col_ins_A2b, col_ins_a2A, col_ins_B2a, col_ins_b2B))
	print (get_ins_A2B(col_ins_B2a, col_ins_b2B, col_ins_A2b, col_ins_a2A))
	print (row_del_A, col_del_A)
	print (row_del_B, col_del_B)
	# print calc_col_status(c, d)
	# print calc_col_status(d, c)














