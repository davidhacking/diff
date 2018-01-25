#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
L[0:2]=[0,1]
L.append在原列表的基础上修改，L+[1]生成新列表
"""

def test_func(l):
	l[0] = 0
	print l

if __name__ == '__main__':
	l = [1, 1, 1]
	print l
	test_func(l)