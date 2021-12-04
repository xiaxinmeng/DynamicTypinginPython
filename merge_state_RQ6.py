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


def calORraw(ismerge,isdyn,dic):
	if ismerge == True and isdyn ==True:
		dic["mergeDT"] = dic["mergeDT"] + 1
	if ismerge == False and isdyn == False:
		dic["NmergeNDT"] = dic["NmergeNDT"] + 1
	if ismerge == True and isdyn ==False:
		dic["mergeNDT"] = dic["mergeNDT"] + 1
	if ismerge == False and isdyn == True:
		dic["NmergeDT"] = dic["NmergeDT"] + 1
	return dic


def smooth(OR_raw_data):
	for key in OR_raw_data.keys():
		if OR_raw_data[key] == 0:
			OR_raw_data[key] = OR_raw_data[key] + 1


def runDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  


	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"
	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull

	OR_raw_data = {"mergeDT":0,"NmergeDT":0,"mergeNDT":0,"NmergeNDT":0}

	for pull in pulls:

		commitfile = pull["commitfile"]
		if decidePy(commitfile):
			ismerge= pull["is_merged"]
			isdyn = False
			# print(type(fixbug))
			for file in commitfile.keys():
				# print pre + file
				if prefix + file in dynDic.keys():
					isdyn = True
					# print(prefix + file)

			OR_raw_data = calORraw(ismerge,isdyn,OR_raw_data)

	# print(OR_raw_data)

	# smooth
	# smooth(OR_raw_data)


	oddsratio, pvalue = stats.fisher_exact([[OR_raw_data["mergeDT"], OR_raw_data["NmergeDT"]], [OR_raw_data["mergeNDT"], OR_raw_data["NmergeNDT"]]])
	return oddsratio,pvalue 


def runRDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  


	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"
	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull

	OR_raw_data = {"mergeDT":0,"NmergeDT":0,"mergeNDT":0,"NmergeNDT":0}

	for pull in pulls:

		commitfile = pull["commitfile"]
		if decidePy(commitfile):
			ismerge= pull["is_merged"]
			isdyn = False
			# print(type(fixbug))
			for file in commitfile.keys():
				# print pre + file
				if prefix + file in dynDic.keys():
					isdyn = True
					# print(prefix + file)

			OR_raw_data = calORraw(ismerge,isdyn,OR_raw_data)

	# print(OR_raw_data)

	# smooth
	# smooth(OR_raw_data)


	oddsratio, pvalue = stats.fisher_exact([[OR_raw_data["mergeDT"], OR_raw_data["NmergeDT"]], [OR_raw_data["mergeNDT"], OR_raw_data["NmergeNDT"]]])
	return oddsratio,pvalue 


def runVDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  


	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"
	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull

	OR_raw_data = {"mergeDT":0,"NmergeDT":0,"mergeNDT":0,"NmergeNDT":0}

	for pull in pulls:

		commitfile = pull["commitfile"]
		if decidePy(commitfile):
			ismerge= pull["is_merged"]
			isdyn = False
			# print(type(fixbug))
			for file in commitfile.keys():
				# print pre + file
				if prefix + file in dynDic.keys():
					if "VDT" in dynDic[prefix + file].keys():
						isdyn = True
					# print(prefix + file)

			OR_raw_data = calORraw(ismerge,isdyn,OR_raw_data)

	# print(OR_raw_data)

	# smooth
	# smooth(OR_raw_data)


	oddsratio, pvalue = stats.fisher_exact([[OR_raw_data["mergeDT"], OR_raw_data["NmergeDT"]], [OR_raw_data["mergeNDT"], OR_raw_data["NmergeNDT"]]])
	return oddsratio,pvalue 


def runRQ6():
	RQ6list = [("project","OR","pvalue")]
	crawlerDir = '/home/xxm/Desktop/EMSE/crawlerResult'

	for root, dirs, files in os.walk(crawlerDir):
		for file in files:
			if not file.startswith("."):
				crawlerfile =root+"/"+file 
				dynamicfile = crawlerfile.replace("crawlerResult","DTResult")
				oddsratio,pvalue = runDT(crawlerfile,dynamicfile)
				print(file.replace(".json",""),"ismerge","Fisher_exact",oddsratio,pvalue)
				RQ6list.append((file.replace(".json",""),oddsratio,pvalue))
	return RQ6list

# RQ6list = runRQ6()
# print(RQ6list)