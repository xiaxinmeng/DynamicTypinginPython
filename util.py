import json
# [(path,scope,category,name,itype,lineno,content)]
def tupleToJson(tlist):
	outDic = {}
	for info in tlist: 
		path = info[0]
		scope = info[1]
		category = info[2]
		name = info[3]
		itype = info[4]
		linenum = info[5]
		content = info[6]
		if path in outDic.keys():
			if scope in outDic[path].keys():
				if category in outDic[path][scope].keys():
					if name in outDic[path][scope][category].keys():
						if itype in outDic[path][scope][category][name].keys():
							outDic[path][scope][category][name][itype].append((linenum,content))
						else:
							outDic[path][scope][category][name][itype] = [(linenum,content)]
					else: 
						outDic[path][scope][category][name] = {itype: [(linenum,content)]}
				else:
					outDic[path][scope][category] = {name:{itype:[(linenum,content)]}}
			else:
				outDic[path][scope] = {category: {name:{itype:[(linenum,content)]}}}
		else:
			outDic[path]={scope : {category: {name:{itype:[(linenum,content)]}}}}
	return outDic



def jsonToTuple(jsonfile):
	dynamiclist = []
	for path in jsonfile.keys():
		for scope in jsonfile[path].keys():
			for category in jsonfile[path][scope].keys():
				for name in jsonfile[path][scope][category].keys():
					for itype in jsonfile[path][scope][category][name].keys():
							for item in jsonfile[path][scope][category][name][itype]:
								lineno = item[0]
								content = item[1]
								dynamiclist.append((path,scope,category,name,itype,lineno,content))
	# for item in dynamiclist:
	# 	print item
	return dynamiclist
	



def totalList(inpath, jsonfile):
	dynamiclist = []
	path = inpath
	for scope in jsonfile.keys():
		for category in jsonfile[scope].keys():
			for name in jsonfile[scope][category].keys():
				for itype in jsonfile[scope][category][name].keys():
						for item in jsonfile[scope][category][name][itype]:
							lineno = item[0]
							content = item[1]
							dynamiclist.append((path,scope,category,name,itype,lineno,content))
	# for item in dynamiclist:
	# 	print item
	return dynamiclist	

# jsonfile  = json.load(open('/home/xxm/Desktop/EMSE/PysonarResult/auto-sklearn.json','r' ))

# jslist = jsonToTuple(jsonfile)
# tupleToJson(jslist)