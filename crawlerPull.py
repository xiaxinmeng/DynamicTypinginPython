from github import Github
import random
import re
import time
import json
import datetime




# reponame = "automl/auto-sklearn"
# outfile = '/home/xxm/Desktop/EMSE/crawlerResult/auto-sklearn.json'

reponame = "pandas-dev/pandas"
outfile = '/home/xxm/Desktop/EMSE/tempresult/pandas_41.json'



use_agent=[              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                         "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
                         "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
                         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
						 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
						 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
						 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
						 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
						 "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
						 "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
						 "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
						 "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
						 "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
						 "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
						 "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
						 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
						 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
						 "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
						 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
						 "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
						 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
						 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
						 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
						 "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"
      
                     ]


usename  = ["michael0923","michael199309","michael1902"]   
# g = Github(login_or_token = usename[random.randint(0,2)],password ="xxm930923",user_agent = use_agent[random.randint(0,25)])


g = Github("michael0923","xxm930923",user_agent = use_agent[random.randint(0,5)])
# g = Github("michael199309","xxm930923",user_agent = use_agent[random.randint(0,25)])
# g = Github("michael1902","xxm930923",user_agent = use_agent[random.randint(0,25)])


repo = g.get_repo(reponame)
# print(repo.get_issues(state='open'))

pulls = repo.get_pulls(state='closed')


# for pull in pulls[:1]:
# 	print(pull.raw_data)


def decideBugPull(title):
	keyword = ["fix","Fix","defect","Defect","error","Error","bug","Bug","issue","Issue","mistake","Mistake","incorrect","Incorrect","fault","Fault","flaw","Flaw"]
	flag = False
	titlelist = title.split(" ")
	for key in keyword:
		for t in titlelist:
			# print(t)
			if key in t:
				flag = True
	return flag

# title = "Allow 1-D threshold binary predictions Fixes"
# print (decideBugPull(title))

jsonlist = []

print("crawler pull...")
lpulls = pulls[16401:] 
print("start")
for pull in lpulls:
	# print(pull.title)
	# print(pull.number,pull.as_issue())
	title = pull.title
	isbug = decideBugPull(title)
	# print(isbug)
	content = pull.body
	# print(content)
	pullid = pull.number
	is_merged = pull.is_merged()
	mergeable = pull.mergeable
	mergeable_state = pull.mergeable_state
	print(pullid)
	# print(pull.is_merged(),pull.mergeable,pull.mergeable_state,pull.merged,pull.state)
	try:
		issueid = re.findall(r"\#\s*\d+",content)
	except:
		issueid = []
	jsoncontent = {}
	issuelist = []
	issuecontent = {}
	commitfile = []
	filechange = {}
	issueLastTime = 0
	issueBegin = 0
	issueEnd = 0
	if issueid:
		for isid in issueid:
			isid = int(isid.replace("#","")) 
			try:
				iss = repo.get_issue(isid)
			except:
				continue
			# print(iss.raw_data)
			# print(iss.get_timeline())
			# for item in iss.get_timeline():
			# 	print(item)
			closetime = iss.closed_at
			createtime = iss.created_at
			if closetime:
				# print(issueBegin,createtime )
				if issueBegin == 0:
					issueBegin = createtime
				elif issueBegin > createtime:
					issueBegin = createtime
				if issueEnd == 0:
					issueEnd = closetime
				elif issueEnd < closetime:
					issueEnd = closetime					

				# if closetime < createtime:
				# 	print("sdfa")
				# else:
				# 	print("ssssss")
				issuecontent["issue_id"] = isid
				issuecontent["issue_created_time"] = iss.created_at.strftime('%Y-%m-%d %H:%M:%S') 
				issuecontent["issue_closed_time"] = iss.closed_at.strftime('%Y-%m-%d %H:%M:%S') 
				# issuecontent["issue_last_time_seconds"] = (iss.closed_at - iss.created_at).total_seconds()/86400
				# print((iss.created_at -iss.closed_at).total_seconds()/86400)
				issuecontent["issue_status"] ="closed"
				# print((iss.closed_at - iss.created_at).total_seconds()/86400)
			else:
				issueBegin = createtime
				issueEnd = datetime.datetime.now()
				issuecontent["issue_id"] = isid
				issuecontent["issue_created time"] = iss.created_at.strftime('%Y-%m-%d %H:%M:%S') 
				issuecontent["issue_status"] ="open"	
			issuelist.append(issuecontent)


	issueLastTime = issueEnd - issueBegin	
	if isinstance(issueLastTime, int):
		pass
	else:
		issueLastTime = issueLastTime.total_seconds()/86400	
	print(issueLastTime)

	for file in pull.get_files():
		# print(file.filename)
		# print(file.patch,file.changes)
		# print(dir(file))
		commitfile.append(file.filename)
		filechange[file.filename]= file.changes


	jsoncontent["pull_id"] = pullid
	jsoncontent["title"] = title
	jsoncontent["is_merged"] = is_merged
	jsoncontent["mergeable_state"] = mergeable_state
	jsoncontent["mergeable"] = mergeable
	jsoncontent["fixBug"] = isbug
	jsoncontent["issue_last_time"] = issueLastTime
	jsoncontent["issues"] = issuelist
	# jsoncontent["commit_files"] = commitfile
	jsoncontent["commitfile"] = filechange
	jsonlist.append(jsoncontent)

# print(jsonlist)

with open(outfile, 'w') as f:
	json.dump(jsonlist,f)



