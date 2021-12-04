import bug_Fix_RQ5 as rq5
import merge_state_RQ6 as rq6
import maintain_time_RQ7 as rq7
import commit_size_RQ8 as rq8
import file_size_RQ9 as rq9
import change_prone_RQ10 as rq10
import commit_merge_RQ11 as rq11
import csv


bug_fix = rq5.runRQ5()
merge_state = rq6.runRQ6()
maintain_time= rq7.runRQ7()
commit_size= rq8.runRQ8()
file_size =rq9.runRQ9()
change_prone =rq10.runRQ10()
commit_merge =rq11.runRQ11()


writer = csv.writer(open("/home/xxm/Desktop/EMSE/result/test1.csv",'a'))
i = 0
while i < len(bug_fix):
	# print(bug_fix[i][0],bug_fix[i][1],bug_fix[i][2],merge_state[i][1],merge_state[i][2],maintain_time[i][1],maintain_time[i][2],maintain_time[i][3],maintain_time[i][4],commit_size[i][1],commit_size[i][2],commit_size[i][3],commit_size[i][4],file_size[i][1],file_size[i][2],file_size[i][3],file_size[i][4],change_prone[i][1],change_prone[i][2],change_prone[i][3],change_prone[i][4],change_prone[i][5],change_prone[i][6],commit_merge[i][1],commit_merge[i][2])
	writer.writerow([bug_fix[i][0],bug_fix[i][1],bug_fix[i][2],merge_state[i][1],merge_state[i][2],maintain_time[i][1],maintain_time[i][2],maintain_time[i][3],maintain_time[i][4],commit_size[i][1],commit_size[i][2],commit_size[i][3],commit_size[i][4],file_size[i][1],file_size[i][2],file_size[i][3],file_size[i][4],change_prone[i][1],change_prone[i][2],change_prone[i][3],change_prone[i][4],change_prone[i][5],change_prone[i][6],commit_merge[i][1],commit_merge[i][2]])
	# writer.writerows([bug_fix[i][0],bug_fix[i][1],bug_fix[i][2],merge_state[i][1],merge_state[i][2],maintain_time[i][1],maintain_time[i][2],maintain_time[i][3],maintain_time[i][4],commit_size[i][1],commit_size[i][2],commit_size[i][3],commit_size[i][4],file_size[i][1],file_size[i][2],file_size[i][3],file_size[i][4],change_prone[i][1],change_prone[i][2],change_prone[i][3],change_prone[i][4],change_prone[i][5],change_prone[i][6],commit_merge[i][1],commit_merge[i][2]])

	i = i + 1
