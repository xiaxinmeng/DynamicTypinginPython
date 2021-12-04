# -*- coding: utf-8 -*-
import json
import util
import beniget, gast
import ast
import DUanalysis as du
from operator import itemgetter, attrgetter
import runPysonar as ps
import os
import decide_dynamic_typing as dp
import csv

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  


def run(dirpath):
	# run Pysonar
	# print(dirpath)
	# ps.run(dirpath)
	csvwriter = csv.writer(open(dirpath.replace("dataset","RDTlist")+ ".csv",'a'))
	VDTwriter = csv.writer(open(dirpath.replace("dataset","VDTlist")+ ".csv",'a'))
		
	# inference result. out : /PysonarResult/auto-sklearn.json



	# decide re-assign dynamic typing
	jsonpath = dirpath.replace("dataset","PysonarResult")+".json"
	jsonfile  = json.load(open(jsonpath,'r'))


	dynDic = {}

	for path in jsonfile:

		# print path
		# dlist=[]
		#dlist: list all reassigned identifiers 

		dlist = dp.ReassignDT(path,jsonfile[path])
		if dlist: 
			for item in dlist:
				# try:
				# print(str(item[0]),str(item[1]),str(item[2]),str(item[3]),str(item[4]),item[5],str(item[6]))
				csvwriter.writerow([str(item[0]),str(item[1]),str(item[2]),str(item[3]),str(item[4]),int(item[5]),str(item[6])])

				# except:
				# 	pass
		# print (dlist)
		# for item in dlist:
		# 	print (item)

		rtype = "RDT"
		dynDic = dp.calRDTPair(dlist,dynDic)

		# print(dynDic)
		dynDic = dp.calDynamic(rtype,path, dlist,dynDic)

		# print(dynDic)



		#structure analysis
		# reassigned identifiers in these structures
		# parse AST
		VDTlist = []
		try:
			code =open(path,'r').read()
			root_node = ast.parse(code)




			# analyze structures
			structDic =  dp.analyStruct(path,root_node,dlist)
			# print(structDic)
			# vlist = structDic["If"] + structDic["TryFinally"] + structDic["TryExcept"]
			# vlist： list all identifiers related to specific structure

			vlist = structDic["If"] 
			# print len(vlist)






			# define- use analysis
			module = gast.parse(code)

			# compute the def-use chains at module level
			duc = beniget.DefUseChains()
			duc.visit(module)

			# analysis to find parent of a node
			ancestors = beniget.Ancestors()
			ancestors.visit(module)

			#find Define-use relations, key:use, DUDict[key]:define
			DUDict = du.defUsePair(duc, ancestors)

			#tlist: list total identifiers in this file	
			tmplist = util.totalList(path, jsonfile[path])
			tlist = []
			for item in tmplist:
				tlist.append((str(item[3]),item[5]))

			# travese all identifiers with coonditional structures and exception structures and analyze their define use chain
			# VDTlist: list all variable dynamic typing identifiers 

			vlist = list(set(vlist))
			if vlist:
				print(vlist)
			for iden in vlist:
				definenode = (str(iden[0]),iden[1])
				# print definenode
				chainlist = []
				chainlist.append(definenode)

				singleChainList = dp.getDUchain(definenode,DUDict,chainlist,tlist)
				VDTlist= VDTlist + singleChainList[1:]
				# print "\n"
				# print singleChainList

			# print len(VDTlist)
			# print(dynDic)
		except:
			print("parse ast error")
			pass
		# print(VDTlist)

		if VDTlist: 
			print(path,VDTlist)
			for item in VDTlist:
				# try:
				# print(str(item[0]),str(item[1]),str(item[2]),str(item[3]),str(item[4]),item[5],str(item[6]))
				VDTwriter.writerow([path,str(item[0]),int(item[1])])

		vtype = "VDT"
		dynDic = dp.calDynamic(vtype,path, VDTlist,dynDic)


	# print(dynDic)
	outjson = dirpath.replace("dataset","DTResult")+".json"
	json.dump(dynDic,open(outjson,'w'))


# dirpath = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn' 

# dirlist = ["models"]
# prefix1 = '/home/xxm/Desktop/EMSE/pysonarHTML'


tempdir = []
# for item  in os.listdir('/home/xxm/Desktop/EMSE/DTResult'):
# 	tempdir.append(item.replace(".json",""))
# print(tempdir)


prefix = '/home/xxm/Desktop/EMSE/dataset'
for filename in os.listdir(prefix):
	# print(filename)
# for filename in dirlist:
	# print(prefix+ "/"+filename)

	# try:
	# 	ps.run()
	# except:
	# 	pass
	if filename not in tempdir:
		print(filename)
		run(prefix+ "/"+filename) 
	# try:
	# 	run(prefix+ "/"+filename) 
	# except:
	# 	pass