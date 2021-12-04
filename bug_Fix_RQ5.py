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


def calORraw(isbug,isdyn,dic):
	if isbug == True and isdyn ==True:
		dic["bugDT"] = dic["bugDT"] + 1
	if isbug == False and isdyn == False:
		dic["NbugNDT"] = dic["NbugNDT"] + 1
	if isbug == True and isdyn ==False:
		dic["bugNDT"] = dic["bugNDT"] + 1
	if isbug == False and isdyn == True:
		dic["NbugDT"] = dic["NbugDT"] + 1
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

	OR_raw_data = {"bugDT":0,"NbugDT":0,"bugNDT":0,"NbugNDT":0}

	for pull in pulls:

		commitfile = pull["commitfile"]
		if decidePy(commitfile):
			isbug = pull["fixBug"]
			isdyn = False
			# print(type(fixbug))
			for file in commitfile.keys():
				# print pre + file
				if prefix + file in dynDic.keys():
					isdyn = True
					# print(prefix + file)

			OR_raw_data = calORraw(isbug,isdyn,OR_raw_data)

	# print(OR_raw_data)

	# smooth
	# smooth(OR_raw_data)


	oddsratio, pvalue = stats.fisher_exact([[OR_raw_data["bugDT"], OR_raw_data["NbugDT"]], [OR_raw_data["bugNDT"], OR_raw_data["NbugNDT"]]])
	return oddsratio,pvalue 


def runRDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  

	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"

	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull

	OR_raw_data = {"bugDT":0,"NbugDT":0,"bugNDT":0,"NbugNDT":0}

	for pull in pulls:

		commitfile = pull["commitfile"]
		if decidePy(commitfile):
			isbug = pull["fixBug"]
			isdyn = False
			# print(type(fixbug))
			for file in commitfile.keys():
				# print pre + file
				if prefix + file in dynDic.keys():
					isdyn = True
					# print(prefix + file)

			OR_raw_data = calORraw(isbug,isdyn,OR_raw_data)

	# print(OR_raw_data)

	# smooth
	# smooth(OR_raw_data)


	oddsratio, pvalue = stats.fisher_exact([[OR_raw_data["bugDT"], OR_raw_data["NbugDT"]], [OR_raw_data["bugNDT"], OR_raw_data["NbugNDT"]]])
	return oddsratio,pvalue 



def runVDT(crawlerfile,dynamicfile):
	pulls = json.load(open(crawlerfile,'r'))
	dynDic	= json.load(open(dynamicfile,'r'))  

	prefix = crawlerfile.split(".")[0].replace("crawlerResult","dataset")+"/"

	# prefix = '/home/xxm/Desktop/EMSE/dataset/auto-sklearn/'
	# print pull

	OR_raw_data = {"bugDT":0,"NbugDT":0,"bugNDT":0,"NbugNDT":0}

	for pull in pulls:

		commitfile = pull["commitfile"]
		if decidePy(commitfile):
			isbug = pull["fixBug"]
			isdyn = False
			# print(type(fixbug))
			for file in commitfile.keys():
				# print pre + file
				if prefix + file in dynDic.keys():
					if "VDT" in dynDic[prefix + file].keys():
						isdyn = True
					# print(prefix + file)

			OR_raw_data = calORraw(isbug,isdyn,OR_raw_data)

	# print(OR_raw_data)

	# smooth
	# smooth(OR_raw_data)


	oddsratio, pvalue = stats.fisher_exact([[OR_raw_data["bugDT"], OR_raw_data["NbugDT"]], [OR_raw_data["bugNDT"], OR_raw_data["NbugNDT"]]])
	return oddsratio,pvalue 



def runRQ5():
	RQ5list = [("project","OR","pvalue")]

	crawlerDir = '/home/xxm/Desktop/EMSE/crawlerResult'

	for root, dirs, files in os.walk(crawlerDir):
		for file in files:
			if not file.startswith("."):
				crawlerfile =root+"/"+file 
				dynamicfile = crawlerfile.replace("crawlerResult","DTResult")
				oddsratio,pvalue = runDT(crawlerfile,dynamicfile)
				print(file.replace(".json",""),"bug_fix","Fisher_exact",oddsratio,pvalue)
				RQ5list.append((file.replace(".json",""),oddsratio,pvalue))
	return RQ5list

# RQ5list = runRQ5()
# print(RQ5list)