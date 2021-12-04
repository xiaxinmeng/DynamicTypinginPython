#coding=utf-8
import csv
import sys
import re
import os
import matplotlib.pyplot as plt

csv.field_size_limit(sys.maxsize)



def patternClassify(mystr):
	# x ='' 
	p1 = r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}\'.{0,}\'\s{0,}$'
	pattern1 = re.compile(p1)
	
	# x=" "
	p2 =  r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}\'.{0,}\'\s{0,}$'
	pattern2 = re.compile(p2)

	# x = 1234 or x= 1.1
	p3 =  r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}[0-9\.]{1,}\s{0,}$'
	pattern3 = re.compile(p3)
	
	# x= True or False
	p4 =  r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}(True|False)\s{0,}$'
	pattern4 = re.compile(p4)
	# x = 1 + 2j

	p5 = r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=(\s{0,}[0-9\.]{1,}\s{0,}\+\s{0,}|\s{0,})[0-9\.]{1,}j\s{0,}$'
	pattern5 = re.compile(p5)

	# x = {,,}
	p6 =  r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}\{.{0,}\}\s{0,}$'
	pattern6 = re.compile(p6)

	# x = [,,]
	p7 = r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}\[.{0,}\]\s{0,}$'
	pattern7 = re.compile(p7)

	# x = (,,)
	p8 = r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}\(.{0,}\)\s{0,}$'
	pattern8 = re.compile(p8)

	# x = a.j
	p9 = r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\.[A-Za-z_][A-Za-z0-9_\.]{0,}\s{0,}$'
	pattern9 = re.compile(p9)
	
	# x = xx()
	p10 = r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}[A-Za-z][A-Za-z0-9_\.]{0,}\(\s{0,}[^$]{0,}\s{0,}\)\s{0,}$'
	pattern10 = re.compile(p10)

	# x = asdd
	p11 = r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}$'
	pattern11 = re.compile(p11)
	
	# x = app[]
	p12 = r'\s{0,}[A-Za-z_][A-Za-z0-9_]{0,}\s{0,}=\s{0,}[A-Za-z_][A-Za-z0-9_\.]{0,}\[[A-Za-z0-9_\.\'\"\(\)]{0,}\]\s{0,}$'
	pattern12 = re.compile(p12)

#test code
	# str1 = "x ='1.23(12.3)'"
	# print "p1 succ", pattern1.match(str1)
	# str2 = 'x ="1.23(12.3)"'
	# print "p1 succ",pattern2.match(str2)

	# str3 = "x = 3"
	# print "p2 succ",pattern3.match(str3)


	# str4 = "_x = False"
	# print "p3 succ",pattern4.match(str4)

	# str5 = "x = 2j"
	# print "p4 succ",pattern5.match(str5)

	# str6 = "x = {asdf,sad}"
	# print "p5 succ",pattern6.match(str6)

	# str7 = "x = [asdf,sad]"
	# print "p6 succ",pattern7.match(str7)
	
	# str8 = "x = (asdf,sad)"
	# print "p7 succ",pattern8.match(str8)
	
	# str9 = "x = a.j.i"
	# print "p8 succ",pattern9.match(str9)

	# str10 = "x = ss.xx()"
	# print "p9 succ",pattern10.match(str10)
	
	#10 complex
	
	if pattern1.match(mystr) != None:
		return 1
	elif pattern2.match(mystr.replace("\"","\'")) != None:
		return 1
	elif pattern3.match(mystr) != None:
		return 2
	elif pattern4.match(mystr) != None:
		return 3
	elif pattern5.match(mystr) != None:
		return 4
	elif pattern6.match(mystr) != None:
		return 5
	elif pattern7.match(mystr) != None:
		return 6
	elif pattern8.match(mystr) != None:
		return 7
	elif pattern9.match(mystr) != None:
		return 8
	elif pattern10.match(mystr) != None:
		return 9
	elif pattern11.match(mystr) != None:
		return 10
	elif pattern12.match(mystr) != None:
		return 11
	else:
		return 12





def getPattern(dyfile):
	patterndic= {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
	# print(sss)

	for item in dyfile:
		# print(item)
		if item[2] == 'var':
			patterndic[patternClassify(item[6])] = patterndic[patternClassify(item[6])] + 1
			# print(patternClassify(item[6]),item[2],item[6])
	return patterndic


def getChangePattern(dlist):
	changepattern = []
	i = 0 
	while i<12:
		changepattern.append([0,0,0,0,0,0,0,0,0,0,0,0])
		i=i+1

	# print(changepattern)

	j = 1
	for item1 in dlist:
		for item2 in dlist:
			# print(item1[0],item1[2],item1[3])
			if item1[0] == item2[0] and item1[3] == item2[3] and item1[2] == 'var' and item2[2] == 'var' and item1[4]!= item2[4] and  int(item1[5]) < int(item2[5]):
				pattern1 =  patternClassify(item1[6])
				pattern2 =  patternClassify(item2[6])
				# if pattern1 ==pattern2:
					# print(item1[3:7],item2[3:7])
				changepattern[pattern1-1][pattern2-1]=changepattern[pattern1-1][pattern2-1] + 1

		j = j + 1

	return changepattern


def getinfolistfromcsv(dypath):

	dyfile = csv.reader(open(dypath,'r'))


	dlist = []
	for item in dyfile:
		dlist.append((item[0],item[1],item[2],item[3],item[4],item[5],item[6]))
	return dlist



# dypath = '/home/xxm/Desktop/EMSE/DTlist/dash.csv' 
# dypath = '/home/xxm/Desktop/EMSE/DTlist/ansible.csv' 



def getTypeKinds(dlist):
	typedic = {}
	for item in dlist:
		infertype = item[4]
		idkind = item[2]
		if idkind == 'var':
			if infertype in typedic.keys():
				typedic[infertype] = typedic[infertype] + 1
			else:
				typedic[infertype] = 0
	return typedic


def mergeBuildin(typedic):

	newdic = {'list':0 ,'dict':0,'tuple':0 , 'set': 0 }
	for key in typedic.keys():
		if key.startswith('[') or key == 'list':
			newdic["list"] = newdic['list'] + typedic[key]
		elif key.startswith('{') :
			newdic["set"] =  newdic['dict'] + typedic[key]
		elif key.startswith('(') or key == 'tuple':
			newdic["tuple"] =  newdic['tuple'] + typedic[key]
		else:
			newdic[key] = typedic[key]
	return newdic


def mergeClass(typedic):

	listelment = ['None','list' ,'str','int','tuple', 'set', 'dict','bool' ,'float' , 'object' ,'callable']
	newdic = {}
	for item in listelment:
		newdic[item] = 0

	for key in typedic.keys():
		if '->' in key:
			newdic["callable"] = newdic['callable'] + typedic[key]
		elif key not in listelment:
			newdic["object"] =  newdic['object'] + typedic[key]
		else: 
			newdic[key] = newdic[key] + typedic[key]

	return newdic



def getTopNType(typedic,n):
	topNdic = {}
	mlist = []
	for key in typedic:
		mlist.append((key,typedic[key]))
	mlist.sort(key=lambda x:x[1],reverse = True)
	return mlist[:n]


def drawpie(typelist):
	labels = []
	fracs = []
	for item in typelist:
		labels.append(item[0])
		fracs.append(item[1])

	plt.pie(fracs,labels = labels,autopct = '%.0f%%')
	plt.show()

mydir = '/home/xxm/Desktop/EMSE/DTlist/'


alltypedic ={}

for root,dirs,files in os.walk(mydir):
	for file in files:

		dypath = mydir + file
		print(dypath)

		dlist = getinfolistfromcsv(dypath)

		typedic = getTypeKinds(dlist)
		for key in typedic.keys():
			if key in alltypedic.keys():
				alltypedic[key] = alltypedic[key] + typedic[key]
			else:
				alltypedic[key] =  typedic[key]



		listTopN = getTopNType(typedic,5)
		print(listTopN)


alltypedic = mergeBuildin(alltypedic)
alltypedic = mergeClass(alltypedic)
listAllTopN =getTopNType(alltypedic,20)






print(listAllTopN)
# print(alltypedic)
drawpie(listAllTopN)
