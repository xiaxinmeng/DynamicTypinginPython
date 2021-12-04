import json
import scipy.stats as stats
import os



# decide whether there are Python files in commit files
def decidePy(commitfile):
	flag = False
	for file in commitfile:
		if file.endswith(".py"):
			# print(file)
			flag = True
	return flag

def runDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  
	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"
	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull
	issueid = []
	timelist = []
	RDTlist =[]
	VDTlist =[]
	DTlist = []

	for pull in pulls:
		commitfile = pull["commitfile"]

		if decidePy(commitfile):
			if pull["issues"]:

				VDT = 0
				RDT = 0


				for file in commitfile.keys():
					# print pre + file
					if prefix + file in dynDic.keys():
						# print(prefix + file)

						RDT = RDT + dynDic[prefix + file]["RDT"]
						if "VDT" in dynDic[prefix + file].keys():
							VDT = VDT + dynDic[prefix + file]["VDT"]
						# print(prefix + file)
				# RDTlist.append(RDT)
				# VDTlist.append(VDT)


				if RDT+VDT ==0 and pull["issue_last_time"] < 365 :
				# if RDT ==0 and pull["issue_last_time"] < 365 :
					pass
					# DTlist.append(1)
				else:
					issueid.append(pull["pull_id"])

					DTlist.append(RDT+VDT)
					# RDTlist.append(RDT)
					timelist.append(pull["issue_last_time"])

	# print(len(timelist),timelist)

	# print(RDTlist)
	# print(VDTlist)
	# print(len(DTlist),DTlist)
	# # smooth
	# smooth(OR_raw_data)
	# print(DTlist)
	# print(timelist)

	# print(dynamicfile,"Dynamic typing,maintain_time")
	i = 0 
	while i < len(DTlist) -1 :

		# print(issueid[i],DTlist[i],timelist[i])
		i = i + 1
		# print(sizelist)


	spearmanr, spvalue= stats.spearmanr(DTlist,timelist)
	pccs,pvalue = stats.pearsonr(DTlist,timelist)
	return pccs,pvalue,spearmanr,spvalue


def runRDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  
	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"
	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull
	issueid = []
	timelist = []
	RDTlist =[]
	VDTlist =[]
	DTlist = []

	for pull in pulls:
		commitfile = pull["commitfile"]

		if decidePy(commitfile):
			if pull["issues"]:

				VDT = 0
				RDT = 0


				for file in commitfile.keys():
					# print pre + file
					if prefix + file in dynDic.keys():
						# print(prefix + file)

						RDT = RDT + dynDic[prefix + file]["RDT"]
						if "VDT" in dynDic[prefix + file].keys():
							VDT = VDT + dynDic[prefix + file]["VDT"]
						# print(prefix + file)
				# RDTlist.append(RDT)
				# VDTlist.append(VDT)


				# if RDT+VDT ==0 and pull["issue_last_time"] < 365 :
				if RDT ==0 and pull["issue_last_time"] < 365 :
					pass
					# DTlist.append(1)
				else:
					issueid.append(pull["pull_id"])

					# DTlist.append(RDT+VDT)
					RDTlist.append(RDT)
					timelist.append(pull["issue_last_time"])

	# print(len(timelist),timelist)

	# print(RDTlist)
	# print(VDTlist)
	# print(len(DTlist),DTlist)
	# # smooth
	# smooth(OR_raw_data)
	# print(DTlist)
	# print(timelist)

	# print(dynamicfile,"Dynamic typing,maintain_time")
	i = 0 
	while i < len(DTlist) -1 :

		# print(issueid[i],DTlist[i],timelist[i])
		i = i + 1
		# print(sizelist)


	spearmanr, spvalue= stats.spearmanr(RDTlist,timelist)
	pccs,pvalue = stats.pearsonr(RDTlist,timelist)
	return pccs,pvalue,spearmanr,spvalue



def runVDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  
	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"
	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull
	issueid = []
	timelist = []
	RDTlist =[]
	VDTlist =[]
	DTlist = []

	for pull in pulls:
		commitfile = pull["commitfile"]

		if decidePy(commitfile):
			if pull["issues"]:

				VDT = 0
				RDT = 0


				for file in commitfile.keys():
					# print pre + file
					if prefix + file in dynDic.keys():
						# print(prefix + file)

						RDT = RDT + dynDic[prefix + file]["RDT"]
						if "VDT" in dynDic[prefix + file].keys():
							VDT = VDT + dynDic[prefix + file]["VDT"]
						# print(prefix + file)
				# RDTlist.append(RDT)
				# VDTlist.append(VDT)


				# if RDT+VDT ==0 and pull["issue_last_time"] < 365 :
				if VDT ==0 and pull["issue_last_time"] < 365 :
					pass
					# DTlist.append(1)
				else:
					issueid.append(pull["pull_id"])

					# DTlist.append(RDT+VDT)
					VDTlist.append(VDT)
					timelist.append(pull["issue_last_time"])

	# print(len(timelist),timelist)

	# print(RDTlist)
	# print(VDTlist)
	# print(len(DTlist),DTlist)
	# # smooth
	# smooth(OR_raw_data)
	# print(DTlist)
	# print(timelist)

	# print(dynamicfile,"Dynamic typing,maintain_time")
	i = 0 
	while i < len(DTlist) -1 :

		# print(issueid[i],DTlist[i],timelist[i])
		i = i + 1
		# print(sizelist)


	spearmanr, spvalue= stats.spearmanr(VDTlist,timelist)
	pccs,pvalue = stats.pearsonr(VDTlist,timelist)
	return pccs,pvalue,spearmanr,spvalue

def runRQ7():

	RQ7list = [("project","Pearsonr","pvalue","spearmanr","pvalue")]

	crawlerDir = '/home/xxm/Desktop/EMSE/crawlerResult'

	for root, dirs, files in os.walk(crawlerDir):
		for file in files:
			if not file.startswith("."):
				crawlerfile =root+"/"+file 
				dynamicfile = crawlerfile.replace("crawlerResult","DTResult")
				pccs,pvalue,spearmanr,spvalue = runDT(crawlerfile,dynamicfile)
				print(file.replace(".json",""),"maintain_time","Pearsonr",pccs,pvalue)
				print(file.replace(".json",""),"maintain_time","spearmanr",spearmanr,spvalue)
				RQ7list.append((file.replace(".json",""),pccs,pvalue,spearmanr,spvalue))
	
	return RQ7list


# RQ7list = runRQ7()
# print(RQ7list)