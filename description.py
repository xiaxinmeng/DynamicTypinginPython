# -*- coding: utf-8 -*-
import json
import os

# 每个项目中pull的总数目
jsonfile = []
for root,dirs,files in os.walk('/home/xxm/Desktop/EMSE/crawlerResult'):
	for file in files:
		filename = root+'/'+file
		if filename.endswith(".json"):
			jf = json.load(open(filename,"r"))
			length = len(jf)
			jsonfile.append((file,length))
# jsonfile.sort(key=lambda x:x[1])
print ("number of pulls: filename , pulls number")
print(jsonfile)





# 每个项目的统计信息,包括py文件总数和平均代码行
def getloc(filepath):
    count = 0
    #判断给定的路径是否是.py文件
    if filepath.endswith('.py'):
        #打开文件
        f = open(filepath,'r')
        #先读取一行
        content = f.readline()
        #当读取的代码行不是空的时候进入while循环
        while content != '':
            #判断代码行不是换行符\n时进入,代码行数加1
            if content != '\n' and '#' not in content :
                count += 1
                #接着读取下一行
            content = f.readline()
        f.close()
    return count



def descrption(dirpath):
	pyfile = 0
	totalloc = 0


	for root,dirs,files in os.walk(dirpath):
		for file in files:
			if file.endswith(".py"):
				pyfile = pyfile + 1
				totalloc = totalloc + getloc(root+"/"+file)
	# print(dirpath,pyfile,totalloc)
	avgloc = totalloc/pyfile
	return pyfile,avgloc


filesize = []
for root,dirs,files in os.walk('/home/xxm/Desktop/EMSE/crawlerResult'):
	for file in files:
		filename = root+'/'+file
		dirname = filename.split(".json")[0].replace("crawlerResult","dataset")
		pyfile,avgloc = descrption(dirname)
		filesize.append((file.split(".json")[0],pyfile,avgloc))
# filesize.sort(key=lambda x:x[1])

print("\n")
print("pull file description: filename , num of pyfile, avgloc")
print(filesize)






# 动态类型信息汇总,包括每个项目中多少RDT,VDT等

dydir = '/home/xxm/Desktop/EMSE/crawlerResult'


dylist = []
for root,dirs, files in os.walk(dydir):
	for file in files:
		dyDic = {}
		filenum =0
		RDTPair = 0
		VDT = 0
		VDTfile = 0
		RDT = 0
		totalDT = 0

		dyfile = dydir.replace("crawlerResult","DTResult")+"/"+file
		dyjsfile = json.load(open(dyfile,"r"))
		for path in dyjsfile.keys():
			if dyjsfile[path].has_key("RDT"):
				RDT = RDT + dyjsfile[path]["RDT"]

			if dyjsfile[path].has_key("RDTPair"):
				RDTPair = RDTPair + dyjsfile[path]["RDTPair"]

			if dyjsfile[path].has_key("VDT"):
				VDT = VDT + dyjsfile[path]["VDT"]
				VDTfile = VDTfile + 1

		filenum = len(dyjsfile.keys())
		dyDic["filename"] =  file.split(".json")[0]
		dyDic["RDT"] = RDT
		dyDic["VDT"] = VDT
		dyDic["RDTPair"] = RDTPair
		dyDic["VDTfile"] = VDTfile
		dyDic["RDTfile"] = filenum
		dylist.append(dyDic)


print("\n")
print("file contains dynamic typing: filename , RDT,VDT,RDTPair,filenum")
# for item in dylist:
# 	print(item["VDTfile"])
print(dylist)



print("\n")
print("commit number: project commitNum")
datasetlist = []
for file in os.listdir('/home/xxm/Desktop/EMSE/dataset'):
	datasetlist.append(file)

for item in datasetlist:
	countcommit = 0
	for root,dirs,files in os.walk('/home/xxm/Desktop/EMSE/gitinfo/'+item+'/commit'):
		for file in files:
			countcommit = countcommit + 1
	print(item, countcommit)
