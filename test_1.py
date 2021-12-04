# -*- coding: UTF-8 -*-
import re
import csv
import ast
import os
import json
import scipy.stats as stats
import generate_scope as gs



def getClass(classdef):
	classlist = []
	for item in classdef:
		classitem = item.split("class ")[1].split("(")[0]
		classlist.append(classitem)
	return classlist

def getFunc(funcdef):
	funclist = []
	for item in funcdef:
		funcitem = item.split("def ")[1].split("(")[0]
		funclist.append(funcitem)
	return funclist


def getChangeInfoFromCommit(path):
	listchange = []
	contents = open(path,'r').read().split("diff --git")[1:]
	for content in contents:
		# print("-------------------------------")
		# print(content)
		classdef = re.findall("\@\@ class \D\w*\(",content)
		classlist = getClass(classdef)

		funcdef = re.findall("\@\@ def \D\w*\(",content)
		funclist = getFunc(funcdef)

		changefiles = re.findall("\+\+\+ b/\S*\n",content)
		if changefiles:
			changefile = changefiles[0].split("+++ b/")[1].split("\n")[0]
			# print(changefile)
			if changefile.endswith(".py"):
				# print("sddddffffffff")
				listchange.append((changefile,funclist,classlist))
	# print(funcdef)
	# print(funclist)
	# # print(classdef)
	# print(classlist)
	# print(changefile)
	# print(listchange)
	return listchange


def decideDyn(roots, commitlist, structDic):
	isdyn = False
	# print(commitlist)
	for comit in commitlist:
		# print(comit[0])
		file = roots + "/" + comit[0]
		func = comit[1]
		clas = comit[2]
		if file in structDic.keys():
			for f in func:
				if f in structDic[file]["funcdef"]:
					isdyn = True
			for c in clas:
				if c in structDic[file]["classdef"]:
					isdyn = True
			# if len(func) == 0 and len(clas) == 0  and len(structDic[file]["funcdef"]) == 0 and len(structDic[file]["classdef"])==0:

			# 	isdyn = True
	

	return isdyn

# def compareOnce()


def decideCommitDyn(roots):
	dynpath = roots.replace("dataset","DTScope")+".json"
	structDic = json.load(open(dynpath,'r'))
	# print(structDic)


	gitdir = roots.replace("dataset","gitinfo")

	shaDic = {}
	for root,dirs,files in os.walk(gitdir):
		for file in files:
			if file != "log.txt":
				commitpath = root + "/" + file
				sha = file.split(".txt")[0]
				# print(commitpath)
				try:
					commitlist = getChangeInfoFromCommit(commitpath)
					shaDic[sha] = decideDyn(roots,commitlist,structDic)
				except: 
					# print("error")
					pass
	return shaDic

def decideCommitState(statelist):
	if statelist[0] == "success":
		return True
	else:
		return False



def getShaState(roots):

	stateDic = {}
	statepath = roots.replace("dataset","Commits")+".json"
	statefile = json.load(open(statepath,"r"))
	for sha in statefile.keys():
		if statefile[sha][1]:
			stateDic[sha] = decideCommitState(statefile[sha][1])

	return stateDic




# roots = "/home/xxm/Desktop/EMSE/dataset/faceswap"

def calOR(roots):
	shaDic =decideCommitDyn(roots)
	stateDic = getShaState(roots)


	ORdic = {"DTS":0,"DTF":0,"NDTS":0,"NDTF":0}
	for sha in stateDic.keys():
		if sha in shaDic.keys():
			if stateDic[sha] == True and shaDic[sha] == True:
				ORdic["DTS"] = ORdic["DTS"] + 1
			if stateDic[sha] == True and shaDic[sha] == False:
				ORdic["NDTS"] = ORdic["NDTS"] + 1
			if stateDic[sha] == False and shaDic[sha] == True:
				ORdic["DTF"] = ORdic["DTF"] + 1
			if stateDic[sha] == False and shaDic[sha] == False:
				ORdic["NDTF"] = ORdic["NDTF"] + 1

	print(ORdic)
	oddsratio, pvalue = stats.fisher_exact([[ORdic["DTS"],ORdic["DTF"]], [ORdic["NDTS"],  ORdic["NDTF"]]])
	return oddsratio, pvalue



# gs.run()
dirs  = "/home/xxm/Desktop/EMSE/dataset"
for d in os.listdir(dirs):
	roots = dirs + "/" + d
	# print(d)
	oddsratio, pvalue = calOR(roots)

	print(d,"fisher_exact",oddsratio, pvalue)