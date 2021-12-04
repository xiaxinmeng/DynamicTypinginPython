# -*- coding: utf-8 -*-
import json
import util
import beniget, gast
import ast
import DUanalysis as du
from operator import itemgetter, attrgetter


# jsonpath = '/home/xxm/Desktop/EMSE/PysonarResult/auto-sklearn.json'
# jsonfile  = json.load(open(jsonpath,'r'))

# print(jsonfile)

# out：[(path,scope,category,name,itype,lineno,content)]


def ReassignDT(inpath,jsonfile):
	dynamiclist = []
	path = inpath
	for scope in jsonfile.keys():
		for category in jsonfile[scope].keys():
			for name in jsonfile[scope][category].keys():
				typekeys = jsonfile[scope][category][name].keys()
				if "?" in typekeys:
					typekeys.remove("?")
				if len(typekeys ) >  1:
					for itype in typekeys:
						for item in jsonfile[scope][category][name][itype]:
							lineno = item[0]
							content = item[1]
							dynamiclist.append((path,scope,category,name,itype,lineno,content))
	return dynamiclist



def calRDTPair(dynamiclist,	RDTcountDic ):

	RDTDic = {}
	for item in dynamiclist:
		path,scope,category,name,itype,lineno,content = item[0],item[1],item[2],item[3],item[4],item[5],item[6]
		if path in RDTDic.keys():
			if scope in RDTDic[path].keys():
				if category in RDTDic[path][scope].keys():
					if name in RDTDic[path][scope][category].keys():
						RDTDic[path][scope][category][name].append((itype,lineno))
					else:
						RDTDic[path][scope][category][name] = [(itype,lineno)]
				else:
					RDTDic[path][scope][category] = {name:[(itype,lineno)]} 
							
			else: 
				RDTDic[path][scope]= {category:{name:[(itype,lineno)]}} 
		else:			
			RDTDic[path]={scope:{category:{name:[(itype,lineno)]}}}


	for path in RDTDic.keys():
		count = 0
		for scope in  RDTDic[path].keys():
			for category in RDTDic[path][scope].keys():
				count = count + len(RDTDic[path][scope][category].keys())
		RDTcountDic[path] = {"RDTPair":count}
	return RDTcountDic




# dtype: "RDT" ,dlist:dynamic list
# out:{u'/home/xxm/Desktop/EMSE/dataset/auto-sklearn/autosklearn/evaluation/train_evaluator.py': {'RDT': 8}}
def calDynamic(dtype,path,dlist,dynDic):
	# if not dlist:
	# 	if path in dynDic.keys():
	# 		dynDic[path][dtype] = 0
	# 	else:
	# 		dynDic[path] = {dtype:0}			
	# else:
	for item in dlist:
		if path in dynDic.keys():
			if dtype in dynDic[path].keys():
				dynDic[path][dtype] = dynDic[path][dtype] + 1
			else:
				dynDic[path][dtype] = 1
		else:
			dynDic[path] = {dtype:1}
	return dynDic
	# print dynDic

# rtype = "RDT"
# rdynDic = rDynamic(rtype,dlist)
# print(dynDic)



def vDynamic(dtype,dlist):
	dynDic = {}
	for item in dlist:
		path = item[0]
		if path in dynDic.keys():
			if "RDT" in dynDic[path].keys():
				dynDic[path][dtype] = dynDic[path]["RDT"] + 1
			else:
				dynDic[path][dtype] = 1
		else:
			dynDic[path] = {dtype:1}
	return dynDic



def judgeStruct(iname, ilineno, node):
	for n in ast.walk(node):
		if isinstance(n, ast.Assign):
			# print(dir(n.targets[0]))
			if hasattr(n.targets[0],'id') and hasattr(n.targets[0],'lineno'):
				# print(n.targets[0].lineno)
				if iname == n.targets[0].id and ilineno ==n.targets[0].lineno:
					return True
	return False


def analyStruct(inpath, root_node, dlist):
	structDic = {"If":[],"FunctionDef":[],"ClassDef":[],"For":[],"While":[],"Try":[],"TryExcept":[],"TryFinally":[]}
	iflist = []
	path = inpath

	for item in dlist:

		handler_name = item[3]

		lineno = item[5]

		# print(ast.dump(root_node))
		for node in ast.walk(root_node):

			if isinstance(node, ast.If):
				# print ("If")
				if judgeStruct(handler_name,lineno, node):
					structDic["If"].append((handler_name,lineno))
			if isinstance(node, ast.FunctionDef):
				if judgeStruct(handler_name,lineno, node):
					# print(item)
					# print ("FunctionDef")
					structDic["FunctionDef"].append((handler_name,lineno))
					# print ("\n") 

			if isinstance(node, ast.ClassDef):
					# print ("classDef")
				if judgeStruct(handler_name,lineno, node):
					structDic["ClassDef"].append((handler_name,lineno))
					# print ("\n") 

			if isinstance(node, ast.For):
					# print ("For")
				if judgeStruct(handler_name,lineno, node):
					structDic["For"].append((handler_name,lineno))

			if isinstance(node, ast.While):
					# print ("While")
				if judgeStruct(handler_name,lineno, node):
					structDic["While"].append((handler_name,lineno))
					# print ("\n") 

			# if isinstance(node, ast.Try):
			# 		# print ("TryExcept")
			# 	if judgeStruct(handler_name,node):
			# 		structDic["Try"].append((handler_name,lineno))

			if isinstance(node, ast.TryExcept):
					# print ("TryExcept")
				if judgeStruct(handler_name,lineno, node):
					structDic["TryExcept"].append((handler_name,lineno))


			if isinstance(node, ast.TryFinally):
				# print ("TryFinally")
				if judgeStruct(handler_name,lineno, node):
					structDic["TryFinally"].append((handler_name,lineno))
	return structDic

# iflist = analyStruct(dlist)["If"] + analyStruct(dlist)["TryFinally"] + analyStruct(dlist)["TryExcept"]
# print iflist





def probagate(use,dlist):
	define = None
	for item in dlist:
		if item[1] == use[1] and item[0] != use[0]:
			define = item
	return define

# print probagate(("SAS",0),dlist)

def getDUchain(definenode,DUDict,dulist,dlist):

	f= False
	for use in DUDict:
		if DUDict[use] == definenode:
			# dulist.append("new")
			dulist.append(use)
			if probagate(use,dlist) is not None:
				dulist.append(probagate(use,dlist))
				getDUchain(probagate(use,dlist),DUDict,dulist,dlist)

	return dulist


 	

