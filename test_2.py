import json
import os

orcommit = "/home/xxm/Desktop/EMSE/crawlerCommit"
for root,dirs,files in os.walk(orcommit):
	for file in files:
		commitDic = {}
		opath = root + '/' + file
		orjson = json.load(open(opath,'r'))
		for pull in orjson:
			for sha in orjson[pull]:
				commitDic[sha] = orjson[pull][sha]
		newpath = opath.replace("crawlerCommit","Commits")
		json.dump(commitDic,open(newpath,'w'))