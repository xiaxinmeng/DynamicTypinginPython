# -*- coding: UTF-8 -*-
import re
import csv
import ast
import os
import json
import scipy.stats as stats


def judgeStruct(iname, ilineno, node):
	for n in ast.walk(node):
		if isinstance(n, ast.Assign):
			# print(dir(n.targets[0]))
			if hasattr(n.targets[0],'id') and hasattr(n.targets[0],'lineno'):
				# print(n.targets[0].lineno)
				if iname == n.targets[0].id and ilineno ==n.targets[0].lineno:
					return True
	return False




def getdynStruct(path):
	# structDic {path{funcdef:[],classdef[]}}
	structDic = {}


	# dtlist  /home/xxm/Desktop/EMSE/dataset/youtube-dl/youtube_dl/extractor/dailymotion.py,.home.xxm.Desktop.EMSE.dataset.youtube-dl.youtube_dl.extractor.dailymotion.DailymotionIE._real_extract,var,f,dict,281,        for f in formats:
	csvreader = csv.reader(open(path,"r"))
	for item in csvreader:	

		path = item[0]
		handler_name = item[3]
		lineno = int(item[5])

		if path not in structDic.keys():
			structDic[path] = {"funcdef":[],"classdef":[]}
		# print(path,handler_name,lineno)

		try:
			code =open(path,'r').read()
			root_node = ast.parse(code)

			# print(ast.dump(root_node))
			for node in ast.walk(root_node):
				if isinstance(node, ast.FunctionDef):
					if judgeStruct(handler_name,lineno, node):
						# print(ast.dump(node))
						# print ("FunctionDef")
						structDic[path]["funcdef"].append(node.name)
						# print ("\n") 

				if isinstance(node, ast.ClassDef):
						# print ("classDef")
					if judgeStruct(handler_name,lineno, node):
						structDic[path]["classdef"].append(node.name)
		except:
			pass
	return structDic

	dynpath = roots.replace("dataset","DTlist")+".csv"
	structDic = getdynStruct(dynpath)
	# print(structDic)

def run():
	dirs  = '/home/xxm/Desktop/EMSE/DTlist'
	for root,dirs,files in os.walk(dirs):
		for file in files:
			print(file)
			dynpath = root + "/" + file
			structDic = getdynStruct(dynpath)
			outpath = dynpath.replace("DTlist","DTScope").replace(".csv",".json")
			json.dump(structDic,open(outpath,'w'))

#run()
