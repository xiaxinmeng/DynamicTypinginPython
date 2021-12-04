import os
import sys
import datetime
# from bs4 import BeautifulSoup  
import re
import csv 
import linecache
import json


def getLineNo(scr):
	num = re.findall("(?<=<span class='lineno'>)[^</span>]{1,}",scr)
	return num[len(num)-1]

def getName(scr):
	name = re.findall("(?<=xid =')[^']{1,}",scr)
	return name[0]

def getType(scr):
	myType = re.findall("(?<=title=')[^']{1,}",scr)
	return myType[0]

# match function, parameter, variable, class
def reguAnalysis(inpath,outpath = "temp.csv"):
	writer=csv.writer(open(outpath,'a'))
	with open(inpath, 'r') as f:  
		content=f.read()

		func = re.findall("<span class='lineno'>[^<]{0,}</span>[^<span]{0,}(?<=def )<a name=[^=]{1,}=[^=]{1,}=[^=]{1,}>[^>]{1,}</a>[^(<span)]{0,}",content)
		for f in func:
			writer.writerow([getLineNo(f),"func",getName(f),getType(f)])

		para = re.findall('def[^(]{0,}(?<=\()<a name=[^=]{1,}=[^=]{1,}=[^=]{1,}>[^:]{0,}</a>\):',content)
		para = re.findall("<span class='lineno'>[^<]{0,}</span>[^<]{0,}(?<=def)[^:]{0,}\([^\)]{0,}<a [^:]{0,}</a>[^:]{0,}\)[^(<span)]{0,}",content)
		for p in para:
			# print(p)
			name = re.findall("(?<=name=')[^']{1,}",p)
			myType = re.findall("(?<=title=')[^']{1,}",p)
			k=1
			while k < len(name):
				writer.writerow([getLineNo(p),"param",name[k],myType[k]])
				k=k+1	

		clas = re.findall("<span class='lineno'>[^<]{0,}</span>[^<]{0,}(?<=class )<a name=[^=]{1,}=[^=]{1,}=[^=]{1,}>[^>]{1,}</a>[^(<span)]{0,}",content)
		for c in clas:
			writer.writerow([getLineNo(c),"class",getName(c),getType(c)])


		var = re.findall("<span class='lineno'>[^<]{0,}</span>[^<span]{0,}(?<=[^class|def] )<a name=[^=]{1,}=[^=]{1,}=[^=]{1,}>[^>]{1,}</a>[^(<span)]{0,}",content)
		for v in var:
			writer.writerow([getLineNo(v),"var",getName(v),getType(v)])


def refreshcsv(outpath):
	if os.path.exists(outpath):
		os.remove(outpath)
		os.mknod(outpath) 
	


def extract(inputpath,outpath = "temp.csv"):
	refreshcsv(outpath)
	if os.path.isdir(inputpath):
		for (root, dirs, files) in os.walk(inputpath): 
			for filename in files:
				try:
					reguAnalysis(os.path.join(root,filename),outpath)
				except:
					pass
	else:
		reguAnalysis(inputpath,outpath)


def returnPath(src):
	part = src.split(".")
	p = ''
	k=1
	path = ''
	while k < len(part):
		p1 = p
		p = p + '/'+ part[k] 
		if os.path.exists(p+".py"):
			path = p + ".py"
			break
		elif not os.path.isdir(p):
			path = p1 +'/' + "__init__.py"
			break
		k = k+1

	return path

def returnName(src):
	part = src.split(".")
	name = part[len(part)-1]
	return name 



def getInfoTuple(inpath,outpath = "tupleInfo.csv"): 
	extract(inpath,"temp.csv")
	temp = "temp.csv"
	text = csv.reader(open(temp))
	outDic = {}

	# writer = csv.writer(open(outpath,'a'))
	for line in text:
		category = line[1]
		name = returnName(line[2])
		path = returnPath(line[2])
		# scope = line[2].replace("."+name,"")
		# scope = '.'.join(str(i) for i in line[2].split(".")[0:-1])
		scope = line[2].rstrip("."+name)
		# print path
		linenum = int(line[0])
		itype = line[3]
		# print(path,int(linenum),returnName(line[2]))
		content = linecache.getline(path,linenum).replace("\n","")
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
			# print (line[1],returnName(line[2]), int(linenum), line[2],  content,line[3])
		# writer.writerow([line[1],returnName(line[2]), int(linenum), path, line[2],  content,line[3]])
		else:
			outDic[path]={scope : {category: {name:{itype:[(linenum,content)]}}}}
			# print (line[1],returnName(line[2]), int(linenum), line[2],  content,line[3])
	
	return outDic
	# with open(outpath,"w") as f:
	# 	json.dump(outDic,f) 


def run(dirpath = '/home/xxm/Desktop/EMSE/dataset' ):

	print(dirpath)

	pysonar = '/home/xxm/Desktop/EMSE/pysonar-2.1.1.jar'

	pysonarHTMLpath = dirpath.replace("dataset","pysonarHTML") 

	starttime = datetime.datetime.now()
	err = os.system("java -jar %s %s %s" %(pysonar,dirpath, pysonarHTMLpath))
	endtime = datetime.datetime.now()
	print "Executing time is ",(endtime-starttime)


	infopath = dirpath.replace("dataset","PysonarResult")+".json"
	outjson = {}
	for (root, dirs, files) in os.walk(pysonarHTMLpath): 
		for filename in files:
			# try:
			# 	getInfoTuple(os.path.join(root,filename),infopath)
			# except:
			# 	pass

			outDic = getInfoTuple(os.path.join(root,filename),infopath)
			for key in outDic:
				if key != '':
					outjson[key] = outDic[key]
	
	with open(infopath,"w") as f:
		json.dump(outjson,f) 


# path = sys.argv[1]
# run(path)