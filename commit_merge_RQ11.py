import json
import scipy.stats as stats
import os


def decidepy(filelist):
	for item in filelist:
		if item.endswith(".py"):
			return True
	return False

def decideDynState(project,filelist,dynfile):
	prefix = '/home/xxm/Desktop/EMSE/dataset'
	for file in filelist:
		if file.endswith(".py"):
			if prefix +"/" + project + "/" + file in dynfile.keys():
				return True
	return False

 

def decideCommitState(statelist):
	if statelist[0] == "success":
		return True
	else:
		return False



def runDT():
	RQ11list = [("project","OR","pvalue")]

	comdir = '/home/xxm/Desktop/EMSE/Commits'

	for root,dirs,files in os.walk(comdir):
		for file in files:
			if file.endswith(".json"):
				ORdic = {"DTS":0,"DTF":0,"NDTS":0,"NDTF":0}
				comfilepath = root + "/"+ file
				dynfilepath = comfilepath.replace("Commits","DTResult")
				comfile = json.load(open(comfilepath,"r"))
				dynfile = json.load(open(dynfilepath,"r"))

				for sha in comfile.keys():
					filelist = comfile[sha][0]
					statelist = comfile[sha][1]
					if decidepy(filelist) and statelist:
						dynState = decideDynState(file.split(".json")[0],filelist,dynfile)
						commitState = decideCommitState(statelist)

						if dynState ==True and commitState ==True:
							ORdic["DTS"] = ORdic["DTS"] + 1
						if dynState ==True and commitState ==False:
							ORdic["DTF"] = ORdic["DTF"] + 1
						if dynState ==False and commitState ==True:
							ORdic["NDTS"] = ORdic["NDTS"] + 1
						if dynState ==False and commitState ==False:
							ORdic["NDTF"] = ORdic["NDTF"] + 1


							# print(pullid,decidepy(filelist),filelist,dynState,statelist,commitState)
				# print(ORdic)
				oddsratio, pvalue = stats.fisher_exact([[ORdic["DTS"],ORdic["DTF"]], [ORdic["NDTS"],  ORdic["NDTF"]]])
				print(file,"fisher_exact",oddsratio, pvalue)
				RQ11list.append((file.replace(".json",""),oddsratio, pvalue))
	return RQ11list



def runRDT():
	RQ11list = [("project","OR","pvalue")]

	comdir = '/home/xxm/Desktop/EMSE/Commits'

	for root,dirs,files in os.walk(comdir):
		for file in files:
			if file.endswith(".json"):
				ORdic = {"DTS":0,"DTF":0,"NDTS":0,"NDTF":0}
				comfilepath = root + "/"+ file
				dynfilepath = comfilepath.replace("Commits","DTResult")
				comfile = json.load(open(comfilepath,"r"))
				dynfile = json.load(open(dynfilepath,"r"))

				for sha in comfile.keys():
					filelist = comfile[sha][0]
					statelist = comfile[sha][1]
					if decidepy(filelist) and statelist:
						dynState = decideDynState(file.split(".json")[0],filelist,dynfile)
						commitState = decideCommitState(statelist)

						if dynState ==True and commitState ==True:
							ORdic["DTS"] = ORdic["DTS"] + 1
						if dynState ==True and commitState ==False:
							ORdic["DTF"] = ORdic["DTF"] + 1
						if dynState ==False and commitState ==True:
							ORdic["NDTS"] = ORdic["NDTS"] + 1
						if dynState ==False and commitState ==False:
							ORdic["NDTF"] = ORdic["NDTF"] + 1


							# print(pullid,decidepy(filelist),filelist,dynState,statelist,commitState)
				# print(ORdic)
				oddsratio, pvalue = stats.fisher_exact([[ORdic["DTS"],ORdic["DTF"]], [ORdic["NDTS"],  ORdic["NDTF"]]])
				print(file,"fisher_exact",oddsratio, pvalue)
				RQ11list.append((file.replace(".json",""),oddsratio, pvalue))
	return RQ11list




def decideVDynState(project,filelist,dynfile):
	prefix = '/home/xxm/Desktop/EMSE/dataset'
	for file in filelist:
		if file.endswith(".py"):
			if prefix +"/" + project + "/" + file in dynfile.keys():
				if "VDT" in dynfile[prefix +"/" + project + "/" + file].keys():
					return True
	return False

def runVDT():
	RQ11list = [("project","OR","pvalue")]

	comdir = '/home/xxm/Desktop/EMSE/Commits'

	for root,dirs,files in os.walk(comdir):
		for file in files:
			if file.endswith(".json"):
				ORdic = {"DTS":0,"DTF":0,"NDTS":0,"NDTF":0}
				comfilepath = root + "/"+ file
				dynfilepath = comfilepath.replace("Commits","DTResult")
				comfile = json.load(open(comfilepath,"r"))
				dynfile = json.load(open(dynfilepath,"r"))

				for sha in comfile:
					filelist = comfile[sha][0]
					statelist = comfile[sha][1]
					if decidepy(filelist) and statelist:
						dynState = decideVDynState(file.split(".json")[0],filelist,dynfile)
						commitState = decideCommitState(statelist)

						if dynState ==True and commitState ==True:
							ORdic["DTS"] = ORdic["DTS"] + 1
						if dynState ==True and commitState ==False:
							ORdic["DTF"] = ORdic["DTF"] + 1
						if dynState ==False and commitState ==True:
							ORdic["NDTS"] = ORdic["NDTS"] + 1
						if dynState ==False and commitState ==False:
							ORdic["NDTF"] = ORdic["NDTF"] + 1


							# print(pullid,decidepy(filelist),filelist,dynState,statelist,commitState)
				# print(ORdic)
				oddsratio, pvalue = stats.fisher_exact([[ORdic["DTS"],ORdic["DTF"]], [ORdic["NDTS"],  ORdic["NDTF"]]])
				print(file,"fisher_exact",oddsratio, pvalue)
				RQ11list.append((file.replace(".json",""),oddsratio, pvalue))
	return RQ11list



def runRQ11():
	RQ11list = runDT()
	return RQ11list

# RQ11list = runRQ11()
# print(RQ11list)


# gitpath = '/home/xxm/Desktop/EMSE/gitinfo'

# datasetlist = ['ansible','cookiecutter','dash','faceswap','flask','mitmproxy','models','pandas','sentry']

# fdic = {}
# for  d in os.listdir(gitpath):
# 	droot = gitpath + "/" + d
# 	c = len(os.listdir(droot+"/commit"))
# 	fdic[d] = c
# # print(fdic)


# for item in RQ11list[1:]:
# 	# print (item)
# 	print(item[0],"...",fdic[item[0].replace(".json","")],"...",item[1],"...",item[2])