import os 
import re



def getCommitFromLog(logpath):
	commitlist = []
	logfile = open(logpath,'r').read()
	# print logfile
	relist = re.findall("commit \w+\nAuthor",logfile)
	for item in relist:
		commitid = item.split("commit ")[1].split("\n")[0]
		commitlist.append(commitid)
	return commitlist


gitdir = '/home/xxm/Desktop/git'

root = '/home/xxm/Desktop/EMSE/gitinfo'

gproj = []
for mydir in os.listdir(root):
	if "." not in mydir:
		gproj.append(mydir)


for d in os.listdir(gitdir):
	if not d.startswith(".") and d not in gproj:
		outdir = root+"/"+d
		print outdir
		if not os.path.exists(outdir):
			os.mkdir(outdir)

		gitrepo = gitdir+"/"+ d
		log = outdir + "/" +  "log.txt"
		os.system("cd %s; git log > %s "%(gitrepo,log))

		commitrepo = outdir + "/" + "commit"
		print commitrepo
		if not os.path.exists(commitrepo):
			os.mkdir(commitrepo)

		commitlist = getCommitFromLog(log)
		
		for commitid in commitlist:

			commitinfofile = commitrepo + "/"+ commitid  + ".txt"
			os.system("cd %s; git show %s > %s "%(gitrepo,commitid,commitinfofile))
