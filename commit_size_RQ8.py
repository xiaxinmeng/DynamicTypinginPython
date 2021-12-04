import json
import scipy.stats as stats
import os


def runDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  
	# print(dynamicfile,crawlerfile)
	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"
	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull

	sizelist = []
	RDTlist =[]
	VDTlist =[]
	DTlist = []

	for pull in pulls:
		commitfile = pull["commitfile"]

		for file in commitfile.keys():
			if file.endswith(".py"):
				VDT = 0
				RDT = 0
				size = commitfile[file]
				# print prefix + file

				if prefix + file in dynDic.keys():


					RDT = dynDic[prefix + file]["RDT"]
					# print(RDT)
					if "VDT" in dynDic[prefix + file].keys():
						VDT = dynDic[prefix + file]["VDT"]
					# print(prefix + file)

				RDTlist.append(RDT)
				VDTlist.append(VDT)	
				if RDT+VDT ==0 or size ==0:
				# if RDT ==0 or size ==0:
					pass
					# DTlist.append(1)
				else:	
					DTlist.append(RDT+VDT)
					# RDTlist.append(RDT)
					sizelist.append(size)


	# print(len(sizelist),sizelist)

	# print(RDTlist)
	# print(VDTlist)
	# print(len(DTlist),DTlist)
	# i = 0
	# while i<len(RDTlist)-1:
	# 	print(DTlist[i],sizelist[i])
	# 	i = i + 1
	# print(DTlist)
	# print(sizelist)
	# print("Dynamic typing,commit_size")
	i = 0 
	while i < len(DTlist) -1 :

		# print(DTlist[i],sizelist[i])
		i = i + 1
		# print(sizelist)
	pccs,pvalue = stats.pearsonr(DTlist,sizelist)
	spear,spvalue = stats.spearmanr(DTlist,sizelist)
	return pccs,pvalue,spear,spvalue

def runRDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  
	# print(dynamicfile,crawlerfile)
	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"
	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull

	sizelist = []
	RDTlist =[]
	VDTlist =[]
	DTlist = []

	for pull in pulls:
		commitfile = pull["commitfile"]

		for file in commitfile.keys():
			if file.endswith(".py"):
				VDT = 0
				RDT = 0
				size = commitfile[file]
				# print prefix + file

				if prefix + file in dynDic.keys():


					RDT = dynDic[prefix + file]["RDT"]
					# print(RDT)
					if "VDT" in dynDic[prefix + file].keys():
						VDT = dynDic[prefix + file]["VDT"]
					# print(prefix + file)

				# RDTlist.append(RDT)
				# VDTlist.append(VDT)	
				# if RDT+VDT ==0 or size ==0:
				if RDT ==0 or size ==0:
					pass
					# DTlist.append(1)
				else:	
					# DTlist.append(RDT+VDT)
					RDTlist.append(RDT)
					sizelist.append(size)


	# print(len(sizelist),sizelist)

	# print(RDTlist)
	# print(VDTlist)
	# print(len(DTlist),DTlist)
	# i = 0
	# while i<len(RDTlist)-1:
	# 	print(DTlist[i],sizelist[i])
	# 	i = i + 1
	# print(DTlist)
	# print(sizelist)
	# print("Dynamic typing,commit_size")
	i = 0 
	while i < len(DTlist) -1 :

		# print(DTlist[i],sizelist[i])
		i = i + 1
		# print(sizelist)
	pccs,pvalue = stats.pearsonr(RDTlist,sizelist)
	spear,spvalue = stats.spearmanr(RDTlist,sizelist)
	return pccs,pvalue,spear,spvalue

def runVDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  
	# print(dynamicfile,crawlerfile)
	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"
	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull

	sizelist = []
	RDTlist =[]
	VDTlist =[]
	DTlist = []

	for pull in pulls:
		commitfile = pull["commitfile"]

		for file in commitfile.keys():
			if file.endswith(".py"):
				VDT = 0
				RDT = 0
				size = commitfile[file]
				# print prefix + file

				if prefix + file in dynDic.keys():


					RDT = dynDic[prefix + file]["RDT"]
					# print(RDT)
					if "VDT" in dynDic[prefix + file].keys():
						VDT = dynDic[prefix + file]["VDT"]
					# print(prefix + file)

				# RDTlist.append(RDT)
				# VDTlist.append(VDT)	
				# if RDT+VDT ==0 or size ==0:
				if VDT ==0 or size ==0:
					pass
					# DTlist.append(1)
				else:	
					# DTlist.append(RDT+VDT)
					VDTlist.append(VDT)
					sizelist.append(size)


	# print(len(sizelist),sizelist)

	# print(RDTlist)
	# print(VDTlist)
	# print(len(DTlist),DTlist)
	# i = 0
	# while i<len(RDTlist)-1:
	# 	print(DTlist[i],sizelist[i])
	# 	i = i + 1
	# print(DTlist)
	# print(sizelist)
	# print("Dynamic typing,commit_size")
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



def runRQ8():
	RQ8list = [("project","Pearsonr","pvalue","spearmanr","pvalue")]

	crawlerDir = '/home/xxm/Desktop/EMSE/crawlerResult'

	for root, dirs, files in os.walk(crawlerDir):
		for file in files:
			if not file.startswith("."):
				crawlerfile =root+"/"+file 
				dynamicfile = crawlerfile.replace("crawlerResult","DTResult")
				pccs,pvalue,spear,spvalue = runDT(crawlerfile,dynamicfile)

				print(file.replace(".json",""),"commit_size","Pearsonr",pccs,pvalue)
				print(file.replace(".json",""),"commit_size","spearmanr",spear,spvalue)
				RQ8list.append((file.replace(".json",""),pccs,pvalue,spear,spvalue))

	return RQ8list

# RQ8list = runRQ8()
# print(RQ8list)