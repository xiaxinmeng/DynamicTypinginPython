
import json
import os
import scipy.stats as stats


print("\n")
print("dynamic typing file in pulls commits")

def getpylist(dirpath):
	pylist = []
	for root,dirs,files in os.walk(dirpath):
		for file in files:
			if file.endswith(".py"):
				pylist.append(root+"/"+file)
	return pylist



def smooth(OR_raw_data):
	for key in OR_raw_data.keys():
		if OR_raw_data[key] == 0:
			OR_raw_data[key] = OR_raw_data[key] + 1


def runDT():	
	RQ10list = [("project","OR","pvalue","pearsonr","pvalue","spearmanr","pvalue")]

	crawdir = '/home/xxm/Desktop/EMSE/crawlerResult'

	pulldyndic = {}
	for root, dirs, files in os.walk(crawdir):
		for file in files:



			ORdic={"DTC":set(),"NDTC":set(),"DTNC":set(),"NDTNC":set()}
			dynfileDic = {}
			crawfile = crawdir + "/" + file
			dynfile = crawfile.replace("crawlerResult","DTResult")
			crawjs = json.load(open(crawfile,'r'),encoding="utf-8")
			dynjs = json.load(open(dynfile,"r"),encoding="utf-8")

			
			tfile = []
			datadir = crawfile.replace("crawlerResult","dataset").split(".json")[0]
			pylist = getpylist(datadir)
			# print(len(pylist))



			print(len(pylist))				

			for path in dynjs.keys():
				if dynjs[path].has_key("VDT"):
					dynfileDic[str(path)] = (0,dynjs[path]["VDT"] + dynjs[path]["RDT"])
				else:
					dynfileDic[str(path)] = (0,dynjs[path]["RDT"])				

			for pull in crawjs:
				commitfilelist =  pull["commitfile"]
				# print(root)
				for commitfile in commitfilelist:
					if commitfile.endswith(".py"):

						comfilepath =root.replace("crawlerResult","dataset")+"/"+file.split(".json")[0]+ "/"+ commitfile 
						# print(comfilepath) 
						if dynfileDic.has_key(comfilepath):
							dynfileDic[comfilepath] = (dynfileDic[comfilepath][0] + 1,dynfileDic[comfilepath][1])
							if os.path.exists(comfilepath):					
								ORdic["DTC"].add(comfilepath)
						else:
							# commitfile =str(commitfil)
							if os.path.exists(comfilepath):		
							# if comfilepath in pylist:
								# print comfilepath
								ORdic["NDTC"].add(comfilepath)


			for path in dynjs.keys():
				# print(path)
				# print(ORdic["DTC"])
				if path not in ORdic["DTC"]:
					ORdic["DTNC"].add(str(path))


			for pfile in pylist:
				if pfile not in ORdic["DTC"]:
					if pfile not in ORdic["NDTC"]:
						if pfile not in ORdic["DTNC"]:

							ORdic["NDTNC"].add(pfile)

			# print(len(dynfileDic.keys()),len(ORdic["DTC"]),len(ORdic["NDTC"]),len(ORdic["DTNC"]),len(ORdic["NDTNC"]))


			OR_raw_Dic={}
			OR_raw_Dic["DTC"]=len(ORdic["DTC"])
			OR_raw_Dic["DTNC"]=len(ORdic["DTNC"])
			OR_raw_Dic["NDTC"]=len(ORdic["NDTC"])
			OR_raw_Dic["NDTNC"]=len(ORdic["NDTNC"])
			print(OR_raw_Dic)
			# smooth(OR_raw_Dic)

			oddsratio, pvalue = stats.fisher_exact([[OR_raw_Dic["DTC"], OR_raw_Dic["DTNC"]], [OR_raw_Dic["NDTC"], OR_raw_Dic["NDTNC"]]])

			print(file,oddsratio, pvalue)

			DTlist =[]
			changelist = []
			for key in dynfileDic.keys():
				changelist.append(dynfileDic[key][0])
				DTlist.append(dynfileDic[key][1])


			spearmanr, spvalue= stats.spearmanr(DTlist,changelist)
			pccs,ppvalue = stats.pearsonr(DTlist,changelist)


			print(file,"spearmanr" ,spearmanr,spvalue)
			print(file,"pearsonr",pccs,ppvalue)

			pulldyndic[file] =dynfileDic

			RQ10list.append((file.replace(".json",""),oddsratio, pvalue,pccs,ppvalue,spearmanr,spvalue))


	return RQ10list
	# print(pulldyndic)

def runRDT():	
	RQ10list = [("project","OR","pvalue","pearsonr","pvalue","spearmanr","pvalue")]

	crawdir = '/home/xxm/Desktop/EMSE/crawlerResult'

	pulldyndic = {}
	for root, dirs, files in os.walk(crawdir):
		for file in files:



			ORdic={"DTC":set(),"NDTC":set(),"DTNC":set(),"NDTNC":set()}
			dynfileDic = {}
			crawfile = crawdir + "/" + file
			dynfile = crawfile.replace("crawlerResult","DTResult")
			crawjs = json.load(open(crawfile,'r'),encoding="utf-8")
			dynjs = json.load(open(dynfile,"r"),encoding="utf-8")

			
			tfile = []
			datadir = crawfile.replace("crawlerResult","dataset").split(".json")[0]
			pylist = getpylist(datadir)
			# print(len(pylist))



			print(len(pylist))				

			for path in dynjs.keys():

				dynfileDic[str(path)] = (0,dynjs[path]["RDT"])				

			for pull in crawjs:
				commitfilelist =  pull["commitfile"]
				# print(root)
				for commitfile in commitfilelist:
					if commitfile.endswith(".py"):

						comfilepath =root.replace("crawlerResult","dataset")+"/"+file.split(".json")[0]+ "/"+ commitfile 
						# print(comfilepath) 
						if dynfileDic.has_key(comfilepath):
							dynfileDic[comfilepath] = (dynfileDic[comfilepath][0] + 1,dynfileDic[comfilepath][1])
							if os.path.exists(comfilepath):					
								ORdic["DTC"].add(comfilepath)
						else:
							# commitfile =str(commitfil)
							if os.path.exists(comfilepath):		
							# if comfilepath in pylist:
								# print comfilepath
								ORdic["NDTC"].add(comfilepath)


			for path in dynjs.keys():
				# print(path)
				# print(ORdic["DTC"])
				if path not in ORdic["DTC"]:
					ORdic["DTNC"].add(str(path))


			for pfile in pylist:
				if pfile not in ORdic["DTC"]:
					if pfile not in ORdic["NDTC"]:
						if pfile not in ORdic["DTNC"]:

							ORdic["NDTNC"].add(pfile)

			# print(len(dynfileDic.keys()),len(ORdic["DTC"]),len(ORdic["NDTC"]),len(ORdic["DTNC"]),len(ORdic["NDTNC"]))


			OR_raw_Dic={}
			OR_raw_Dic["DTC"]=len(ORdic["DTC"])
			OR_raw_Dic["DTNC"]=len(ORdic["DTNC"])
			OR_raw_Dic["NDTC"]=len(ORdic["NDTC"])
			OR_raw_Dic["NDTNC"]=len(ORdic["NDTNC"])
			print(OR_raw_Dic)
			# smooth(OR_raw_Dic)

			oddsratio, pvalue = stats.fisher_exact([[OR_raw_Dic["DTC"], OR_raw_Dic["DTNC"]], [OR_raw_Dic["NDTC"], OR_raw_Dic["NDTNC"]]])

			print(file,oddsratio, pvalue)

			DTlist =[]
			changelist = []
			for key in dynfileDic.keys():
				changelist.append(dynfileDic[key][0])
				DTlist.append(dynfileDic[key][1])


			spearmanr, spvalue= stats.spearmanr(DTlist,changelist)
			pccs,ppvalue = stats.pearsonr(DTlist,changelist)


			print(file,"spearmanr" ,spearmanr,spvalue)
			print(file,"pearsonr",pccs,ppvalue)

			pulldyndic[file] =dynfileDic

			RQ10list.append((file.replace(".json",""),oddsratio, pvalue,pccs,ppvalue,spearmanr,spvalue))


	return RQ10list
	# print(pulldyndic)


def runVDT():	
	RQ10list = [("project","OR","pvalue","pearsonr","pvalue","spearmanr","pvalue")]

	crawdir = '/home/xxm/Desktop/EMSE/crawlerResult'

	pulldyndic = {}
	for root, dirs, files in os.walk(crawdir):
		for file in files:



			ORdic={"DTC":set(),"NDTC":set(),"DTNC":set(),"NDTNC":set()}
			dynfileDic = {}
			crawfile = crawdir + "/" + file
			dynfile = crawfile.replace("crawlerResult","DTResult")
			crawjs = json.load(open(crawfile,'r'),encoding="utf-8")
			dynjs = json.load(open(dynfile,"r"),encoding="utf-8")

			
			tfile = []
			datadir = crawfile.replace("crawlerResult","dataset").split(".json")[0]
			pylist = getpylist(datadir)
			# print(len(pylist))



			print(len(pylist))				

			for path in dynjs.keys():
				if dynjs[path].has_key("VDT"):
					dynfileDic[str(path)] = (0,dynjs[path]["VDT"])
			

			for pull in crawjs:
				commitfilelist =  pull["commitfile"]
				# print(root)
				for commitfile in commitfilelist:
					if commitfile.endswith(".py"):

						comfilepath =root.replace("crawlerResult","dataset")+"/"+file.split(".json")[0]+ "/"+ commitfile 
						# print(comfilepath) 
						if dynfileDic.has_key(comfilepath):
							dynfileDic[comfilepath] = (dynfileDic[comfilepath][0] + 1,dynfileDic[comfilepath][1])
							if os.path.exists(comfilepath):					
								ORdic["DTC"].add(comfilepath)
						else:
							# commitfile =str(commitfil)
							if os.path.exists(comfilepath):		
							# if comfilepath in pylist:
								# print comfilepath
								ORdic["NDTC"].add(comfilepath)


			for path in dynjs.keys():
				# print(path)
				# print(ORdic["DTC"])
				if path not in ORdic["DTC"]:
					ORdic["DTNC"].add(str(path))


			for pfile in pylist:
				if pfile not in ORdic["DTC"]:
					if pfile not in ORdic["NDTC"]:
						if pfile not in ORdic["DTNC"]:

							ORdic["NDTNC"].add(pfile)

			# print(len(dynfileDic.keys()),len(ORdic["DTC"]),len(ORdic["NDTC"]),len(ORdic["DTNC"]),len(ORdic["NDTNC"]))


			OR_raw_Dic={}
			OR_raw_Dic["DTC"]=len(ORdic["DTC"])
			OR_raw_Dic["DTNC"]=len(ORdic["DTNC"])
			OR_raw_Dic["NDTC"]=len(ORdic["NDTC"])
			OR_raw_Dic["NDTNC"]=len(ORdic["NDTNC"])
			print(OR_raw_Dic)
			# smooth(OR_raw_Dic)

			oddsratio, pvalue = stats.fisher_exact([[OR_raw_Dic["DTC"], OR_raw_Dic["DTNC"]], [OR_raw_Dic["NDTC"], OR_raw_Dic["NDTNC"]]])

			print(file,oddsratio, pvalue)

			DTlist =[]
			changelist = []
			for key in dynfileDic.keys():
				changelist.append(dynfileDic[key][0])
				DTlist.append(dynfileDic[key][1])


			spearmanr, spvalue= stats.spearmanr(DTlist,changelist)
			pccs,ppvalue = stats.pearsonr(DTlist,changelist)


			print(file,"spearmanr" ,spearmanr,spvalue)
			print(file,"pearsonr",pccs,ppvalue)

			pulldyndic[file] =dynfileDic

			RQ10list.append((file.replace(".json",""),oddsratio, pvalue,pccs,ppvalue,spearmanr,spvalue))


	return RQ10list
	# print(pulldyndic)




def runRQ10():
	RQ10list = runDT()
	return RQ10list

# RQ10list = runRQ10()
# print(RQ10list)

