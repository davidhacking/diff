#!/usr/bin/python
# -*- utf-8 -*-

def lcs(A, B):
	result = 0
	if len(A) is 0 or len(B) is 0:
		result
	elif A[0] == B[0]:
		result = 1 + lcs(A[1:len(A)], B[1:len(B)])
	else:
		result = max(lcs(A, B[1:len(B)]), lcs(A[1:len(A)], B))
	return result


def column(matrix, i):
    return [row[i] for row in matrix]


def calc_row_status_table(a, b):
	rst = {};
	i = 0;
	for x in range(len(a)):
		res = [0, -1]
		for y in range(i, len(b)):
			t = lcs(a[x], b[y])
			if res[0] < t:
				res[0] = t
				res[1] = y
		if res[0] > 0:
			rst[x] = [res[1], res[0]]
			i = res[1] + 1
	return rst

def calc_col_status_table(a, b):
	rst = {};
	i = 0;
	if len(a) > 0:
		for x in range(len(a[0])):
			res = [0, -1]
			if len(b) > 0:
				for y in range(i, len(b[0])):
					t = lcs(column(a, x), column(b, y))
					if res[0] < t:
						res[0] = t
						res[1] = y
				if res[0] > 0:
					rst[x] = [res[1], res[0]]
					i = res[1] + 1
	return rst

def calc_row_status(a, b):
	# 0 for normal, 1 for insert, -1 for delete
	row_convert_info = []
	rst = calc_row_status_table(a, b)
	row_ins_A2b = {}
	row_ins_a2A = {}
	row_del = []
	x = 0
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
	print cst
	col_ins_A2b = {}
	col_ins_a2A = {}
	col_del = []
	x = 0
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
	rs, rst, row_ins_A2b, row_ins_a2A, row_del = calc_row_status(a, b)
	cs, cst, col_ins_A2b, col_ins_a2A, col_del = calc_col_status(a, b)
	print rs, rst
	print cs, cst
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
	for k, v in cell_diff_A2a.items():
		t = cell_diff_b2B[cell_diff_a2b[v]]
		cell_diff_A2B.append([[k[0], k[1]], [t[0], t[1]]])
	return cell_diff_A2B

def get_ins_A2B(ins_A2b, ins_a2A, ins_B2a, ins_b2B):
	print ins_A2b, ins_a2A, ins_B2a, ins_b2B
	ins_A2B = []
	for k, v in ins_A2b.items():
		ins_A2B.append([k, ins_b2B[v]])
	return ins_A2B

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
		['Col-1', 'Col-2', 'Col-3', 'Col-4', 'Col-5', 'Col-6', 'Col-1', 'Col-2', 'Col-3', 'Col-4', 'Col-5', 'Col-6'],
		['v-1-1', 'v-1-2', 'v-1-3', 'v-1-4', 'v-1-5', 'v-1-6', 'v-1-1', 'v-1-2', 'v-1-3', 'v-1-4', 'v-1-5', 'v-1-6'],
		['v-2-1', 'v-2-2', 'v-2-3', 'v-2-4', 'v-2-5', 'v-2-6', 'v-2-1', 'v-2-2', 'v-2-3', 'v-2-4', 'v-2-5', 'v-2-6'],
		['v-3-1', 'v-3-2', 'v-3-3', 'v-3-4', 'v-3-5', 'v-3-6', 'v-3-1', 'v-3-2', 'v-3-3', 'v-3-4', 'v-3-5', 'v-3-6'],
		['v-4-1', 'v-4-2', 'v-4-3', 'v-4-4', 'v-4-5', 'v-4-6', 'v-4-1', 'v-4-2', 'v-4-3', 'v-4-4', 'v-4-5', 'v-4-6'],
		['v-5-1', 'v-5-2', 'v-5-3', 'v-5-4', 'v-5-5', 'v-5-6', 'v-5-1', 'v-5-2', 'v-5-3', 'v-5-4', 'v-5-5', 'v-5-6']
	]


d = [
		['Col-1', 'Col-2', 'Col-3', 'Col-4', 'Col-5', 'Col-7'],
		['v-1-1', 'v-1-2', 'v-1-3', 'v-1-4', 'v-1-5', 'v-1-7'],
		['v-2-1', 'v-2-2', 'v-9-3', 'v-8-4', 'v-2-5', 'v-2-7'],
		['v-3-1', 'v-3-2', 'v-3-3', 'v-3-4', 'v-7-5', 'v-3-7'],
		['v-5-1', 'v-5-2', 'v-5-3', 'v-5-4', 'v-5-5', 'v-5-7'],
		['v-6-1', 'v-6-2', 'v-6-3', 'v-6-4', 'v-6-5', 'v-6-7'],
	]


if __name__ == "__main__":
	x, cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, row_ins_A2b, row_ins_a2A, col_ins_A2b, col_ins_a2A, row_del_A, col_del_A = get_diff_matrix(d, c)
	y, cell_diff_b2B, cell_diff_B2b, cell_diff_b2a, row_ins_B2a, row_ins_b2B, col_ins_B2a, col_ins_b2B, row_del_B, col_del_B = get_diff_matrix(c, d)
	print get_cell_diff_A2B(cell_diff_a2A, cell_diff_A2a, cell_diff_a2b, cell_diff_b2B, cell_diff_B2b, cell_diff_b2a)
	print get_ins_A2B(row_ins_A2b, row_ins_a2A, row_ins_B2a, row_ins_b2B)
	print get_ins_A2B(row_ins_B2a, row_ins_b2B, row_ins_A2b, row_ins_a2A)
	print get_ins_A2B(col_ins_A2b, col_ins_a2A, col_ins_B2a, col_ins_b2B)
	print get_ins_A2B(col_ins_B2a, col_ins_b2B, col_ins_A2b, col_ins_a2A)
	print row_del_A, col_del_A
	print row_del_B, col_del_B
	# print calc_col_status(c, d)
	# print calc_col_status(d, c)














