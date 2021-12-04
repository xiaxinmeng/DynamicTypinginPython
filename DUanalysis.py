# -*- coding: utf-8 -*-
import beniget, gast
import ast


#decide define or use for every name of identifiers
def analysisDURel(duc):
	dName = []
	for key in duc.chains:
		chain = duc.chains[key]
		# print ast.dump(key),dir(key)
		# print dir(chain.node)
		# print ast.dump(chain.node)
		if hasattr(chain.node,'ctx'):
			if gast.dump(chain.node.ctx) == "Load()":
				dName.append(("U" , chain.name(),chain.node.lineno))
			elif gast.dump(chain.node.ctx) == "Store()":
				dName.append(("D" , chain.name(),chain.node.lineno))
	return dName



#return all name(define or use) in a file
def recoName(duc):
	DUTupleList = analysisDURel(duc)
	name = set()
	for item in DUTupleList:
		name.add(item[1])

	return list(name)

# IDname = recoName(duc)
# print IDname

def returnDUtuple(name, usenode, definenode):
	dTuple = ()
	uTuple = ()
	# print name, ast.dump(usenode),ast.dump(definenode)
	for node in gast.walk(usenode):
		# print type(node)
		if isinstance(node, gast.Name) and node.id == name:
			# print gast.dump(node),dir(node)
			uTuple = (node.id,node.lineno)
	
	for node in gast.walk(definenode):
		# print gast.dump(node),dir(node)
		if isinstance(node,gast.Name) and node.id == name:
			if hasattr(node,"lineno"):
				dTuple = (node.id,node.lineno)

	# print dTuple,uTuple
	return dTuple,uTuple


def defUsePair(duc,ancestors):
	DUDict = {}
	IDname = recoName(duc)
	for key in duc.chains:
		chain = duc.chains[key]
		for use in chain.users():
			if use.name() in IDname: 
			   # we're interested in the parent of the decorator
				parents = ancestors.parents(use.node)
			   # direct parent of the decorator is the function

				fdef = parents[-1]
				# print dir(fdef),gast.dump(fdef),gast.dump(key)
				dTuple,uTuple = returnDUtuple(use.name(),fdef, key)
				DUDict[uTuple] =dTuple
				# DUDict[(use.name(),fdef.lineno, fdef.col_offset)]= [(use.name(),key.lineno,key.col_offset)]

	return DUDict
# defUsePair(duc)


# def printDefineName(duc):
# 	DUTupleList = analysisDURel(duc)	
# 	for item in DUTupleList:
# 		if item[0] == "D":
# 			print (item[1],item[2],item[3])









# module = gast.parse(code)

# # compute the def-use chains at module level
# duc = beniget.DefUseChains()
# duc.visit(module)

# # analysis to find parent of a node
# ancestors = beniget.Ancestors()
# ancestors.visit(module)




# #find Define-use relations
# DUDict = defUsePair(duc, ancestors)

# # print '\n',"Define-use relations:"
# for item in DUDict:
# 	if DUDict[item]:
# 		print DUDict[item], item


