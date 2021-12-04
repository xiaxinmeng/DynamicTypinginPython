import ast
import traceback
import os
import csv



def judgeStruct(iname, ilineno, node):
	for n in ast.walk(node):
		# if isinstance(n, ast.Assign):
		# 	# print(dir(n.targets[0]))
		if hasattr(n,'targets'):
			if hasattr(n.targets[0],'id') and hasattr(n.targets[0],'lineno'):
				# print(n.targets[0].lineno)
				if iname == n.targets[0].id and ilineno ==n.targets[0].lineno:
					return True
	return False


def analyStruct(dfpath,dtype,structID, structDic, root_node, handler_name,lineno):

	# print(ast.dump(root_node))
	for node in ast.walk(root_node):

		if isinstance(node, ast.If):
			if judgeStruct(handler_name,lineno, node):
				structDic["If"] = structDic["If"] + 1
				structID["If"].add((handler_name,lineno))
				print(handler_name, dtype,lineno,dfpath)

		if isinstance(node, ast.FunctionDef):
			if judgeStruct(handler_name,lineno, node):
				structDic["FunctionDef"] = structDic["FunctionDef"] + 1
				structID["FunctionDef"].add((handler_name,lineno))

		if isinstance(node, ast.ClassDef):
			if judgeStruct(handler_name,lineno, node):
				structDic["ClassDef"] = structDic["ClassDef"] + 1
				structID["ClassDef"].add((handler_name,lineno))

		if isinstance(node, ast.For):
			if judgeStruct(handler_name,lineno, node):
				structDic["For"] = structDic["For"] + 1
				structID["For"].add((handler_name,lineno))


		if isinstance(node, ast.While):
			if judgeStruct(handler_name,lineno, node):
				structDic["While"] = structDic["While"] + 1
				structID["While"].add((handler_name,lineno))


		if isinstance(node, ast.Try):
			if judgeStruct(handler_name,lineno,node):
				structDic["Try"] = structDic["Try"] + 1
				structID["Try"].add((handler_name,lineno))


		# if isinstance(node, ast.TryExcept):
		# 		# print ("TryExcept")
		# 	if judgeStruct(handler_name,lineno, node):
		# 		structDic["TryExcept"].append((handler_name,lineno))


		# if isinstance(node, ast.TryFinally):
		# 	# print ("TryFinally")
		# 	if judgeStruct(handler_name,lineno, node):
		# 		structDic["TryFinally"].append((handler_name,lineno))
	return structDic,structID


error = 0

dydir = '/home/xxm/Desktop/EMSE/DTlist'

for root,dirs,files in os.walk(dydir):
	for file in files:
		if file == 'pipenv.csv':
			print(file)
			csvpath = dydir + '/' + file
			csvfile = csv.reader(open(csvpath,'r'))
			structDic = {"If":0,"FunctionDef":0,"ClassDef":0,"For":0,"While":0,"Try":0}
			structID = {"If":set(),"FunctionDef":set(),"ClassDef":set(),"For":set(),"While":set(),"Try":set(),"Other":set()}

			other = 0
			for item in csvfile:

				try:
					# print(item)
					dfpath = item[0]
					handler_name =item[3]
					lineno = int(item[5])
					dtype = item[4]
					code =open(dfpath,'r').read()
					root_node = ast.parse(code)
					orginstructID = structID
					# print((structDic,ast.dump(root_node),handler_name,lineno))
					structDic,structID = analyStruct(dfpath,dtype, structID ,structDic,root_node,handler_name,lineno)
					# if orginstructID ==structID:
					# 	structID["Other"].add((handler_name,lineno))


				except:
					error = error + 1
					pass

			print(structDic)
			for key in structID.keys():
				print(key,len(structID[key]))

print(error)