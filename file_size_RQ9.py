import json
import scipy.stats as stats

import os


def runDT(dynamicfile):
	dynDic	= json.load(open(dynamicfile,'r'))  

	sizelist = []
	RDTlist =[]
	VDTlist =[]
	DTlist = []

	for file in dynDic.keys():
		RDT = 0
		VDT = 0
		try:
			fsize = 0
			for index, line in enumerate(open(file,'r')):
				fsize += 1
		except:
			continue


		RDT = dynDic[file]["RDT"]
  		# print(RDT)
		RDTlist.append(RDT)
		if "VDT" in dynDic[file].keys():
			VDT = dynDic[file]["VDT"]
			VDTlist.append(VDT)	
		if RDT+VDT ==0:
			pass
					# DTlist.append(1)
		else:	
			DTlist.append(RDT+VDT)
			sizelist.append(fsize)

	# print(len(sizelist),sizelist)

	# print(RDTlist)
	# print(VDTlist)
	# print(len(DTlist),DTlist)
	# # smooth
	# smooth(OR_raw_data)
	# print("Dynamic typing,file_size")
	i = 0 
	while i < len(DTlist) -1 :

		# print(DTlist[i],sizelist[i])
		i = i + 1
		# print(sizelist)
	spear,spvalue = stats.spearmanr(DTlist,sizelist)
	pccs,pvalue = stats.pearsonr(DTlist,sizelist)
	return pccs,pvalue,spear,spvalue


def runRDT(dynamicfile):
	dynDic	= json.load(open(dynamicfile,'r'))  

	sizelist = []
	RDTlist =[]
	VDTlist =[]
	DTlist = []

	for file in dynDic.keys():
		RDT = 0
		VDT = 0
		try:
			fsize = 0
			for index, line in enumerate(open(file,'r')):
				fsize += 1
		except:
			continue


		RDT = dynDic[file]["RDT"]
  		# print(RDT)
		# RDTlist.append(RDT)
		if "VDT" in dynDic[file].keys():
			VDT = dynDic[file]["VDT"]
			VDTlist.append(VDT)	
		if RDT ==0:
			pass
					# DTlist.append(1)
		else:	
			RDTlist.append(RDT)
			sizelist.append(fsize)

	# print(len(sizelist),sizelist)

	# print(RDTlist)
	# print(VDTlist)
	# print(len(DTlist),DTlist)
	# # smooth
	# smooth(OR_raw_data)
	# print("Dynamic typing,file_size")
	i = 0 
	while i < len(DTlist) -1 :

		# print(DTlist[i],sizelist[i])
		i = i + 1
		# print(sizelist)
	spear,spvalue = stats.spearmanr(RDTlist,sizelist)
	pccs,pvalue = stats.pearsonr(RDTlist,sizelist)
	return pccs,pvalue,spear,spvalue


def runVDT(dynamicfile):
	dynDic	= json.load(open(dynamicfile,'r'))  

	sizelist = []
	RDTlist =[]
	VDTlist =[]
	DTlist = []

	for file in dynDic.keys():
		RDT = 0
		VDT = 0
		try:
			fsize = 0
			for index, line in enumerate(open(file,'r')):
				fsize += 1
		except:
			continue


		RDT = dynDic[file]["RDT"]
  		# print(RDT)
		RDTlist.append(RDT)
		if "VDT" in dynDic[file].keys():
			VDT = dynDic[file]["VDT"]
			# VDTlist.append(VDT)	

		if VDT ==0:
			pass
					# DTlist.append(1)
		else:	
			VDTlist.append(VDT)
			sizelist.append(fsize)

	# print(len(sizelist),sizelist)

	# print(RDTlist)
	# print(VDTlist)
	# print(len(DTlist),DTlist)
	# # smooth
	# smooth(OR_raw_data)
	# print("Dynamic typing,file_size")
	i = 0 
	while i < len(DTlist) -1 :

		# print(DTlist[i],sizelist[i])
		i = i + 1
		# print(sizelist)



	try:

		pccs,pvalue = stats.pearsonr(VDTlist,sizelist)
	except:
		pccs,pvalue = "nan","nan"
	try:
		spear,spvalue = stats.spearmanr(VDTlist,sizelist)
	except:
		spear,spvalue = "nan","nan"

	return pccs,pvalue,spear,spvalue





def runRQ9():
	RQ9list = [("project","Pearsonr","pvalue","spearmanr","pvalue")]

	filelist = []
	for file in os.listdir('/home/xxm/Desktop/EMSE/crawlerResult'):
		filelist.append(file)

	DTDir = '/home/xxm/Desktop/EMSE/DTResult'

	for root, dirs, files in os.walk(DTDir):
		for file in files:
			if not file.startswith("."):
				if file in filelist:
					dynamicfile = root+"/"+file 

					pccs,pvalue,spear,spvalue = runDT(dynamicfile)
					print(file.replace(".json",""),"file_size","Pearsonr",pccs,pvalue)
					print(file.replace(".json",""),"file_size","spearmanr",spear,spvalue)
					RQ9list.append((file.replace(".json",""),pccs,pvalue,spear,spvalue))
	return RQ9list

# RQ9list = runRQ9()
# print(RQ9list)