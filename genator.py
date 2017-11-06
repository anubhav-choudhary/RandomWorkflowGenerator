class Task:
	def __init__(self,tid):
		self.tid = tid
		self.childs = []
		self.parents = []
		self.load = 0

def printWorkflow(wf,h,w):
	for i in range(h):
		print "--- LVL",(i+1),"-----"
		for j in range(w):
			if wf[i][j] != -1:
				print "[ tid = ", wf[i][j].tid, " load = ", wf[i][j].load,"MIPS childs = {",','.join(map(str,wf[i][j].childs)),"}, parents = {",','.join(map(str,wf[i][j].parents)),"} ]"

def generateWorflowMatrix(wf, h, w, n):
	mapTask = {}
	
	mat2d = [[0 for x in range(n)] for y in range(n)]
	mat1d = [[0, 0] for x in range(n)]
	tid = 0;
	for i in range(h):
		for j in range(w):
			if wf[i][j] != -1:
				mat1d[tid] = wf[i][j].load
				mapTask[wf[i][j].tid] = tid
				tid = tid  +1
	for i in range(h):
		for j in range(w):
			if wf[i][j] != -1:
				pid = wf[i][j].tid
				pind = mapTask[pid]
				for k in range(0,len(wf[i][j].childs)):
					cid = wf[i][j].childs[k][0]
					cind = mapTask[cid]
					mat2d[pind][cind] = wf[i][j].childs[k][1]
	#print mat1d
	#print mapTask
	print tid
	for i in range(n):
		for j in range(n):
			print mat2d[i][j],
		print ""
	for i in range(tid):
		print mat1d[i],
	print ""
		

import math
import random
import sys
# Input Parameter
if len(sys.argv) < 8:
	print "Enter No of tasks (V):"
	v = int(raw_input())
	lower = 1/math.sqrt(v)
	upper = math.sqrt(v)
	alpha = -1
	while alpha <= lower or alpha >= upper:
		print "Enter Shape Parameter (Alpha) [",lower,",",upper,"]:"
		alpha = float(raw_input())

	EdgeProb = -1
	while EdgeProb < 0 or EdgeProb > 1:
		print "Enter Edge Probability [0,1]: "
		EdgeProb  = float(raw_input())

	print "Enter base computational power (MIPS):"
	baseMIPS = float(raw_input())

	print "Enter base Bandwidth (MBPS):"
	baseBandwidth = float(raw_input())

	print "Enter CCR:"
	CCR = float(raw_input())

	print "Max Task Load:"
	Maxload = int(raw_input())
else:
	v = int(sys.argv[1])
	alpha = float(sys.argv[2])
	EdgeProb = float(sys.argv[3])
	baseMIPS = float(sys.argv[4])
	baseBandwidth = float(sys.argv[5])
	CCR = float(sys.argv[6])
	Maxload = int(sys.argv[7])


edgecount = 0

# Height and Width Calculation

height = int(math.ceil(math.sqrt(v)/alpha)) 
width = int(math.ceil(math.sqrt(v)*alpha))
#print "h = ", height, "w = ", width

# define workflow matrix
workflow = [[-1 for x in range(width)] for y in range(height)]
workflowlvlcount = [0 for x in range(height)]

currtaskid = 0
# phase 1 mandetory task assignment to level
for i in range(height):
	workflow[i][0] = Task(currtaskid)
	currtaskid = currtaskid + 1
	workflowlvlcount[i] = workflowlvlcount[i] + 1

# phase 2 random task assignment to all level
while v-currtaskid > 0:
	randlvl = random.randint(0,height-1)
	if workflowlvlcount[randlvl] == width:
		continue
	workflow[randlvl][workflowlvlcount[randlvl]] = Task(currtaskid)
	currtaskid = currtaskid + 1
	workflowlvlcount[randlvl] = workflowlvlcount[randlvl] + 1

# phase 3 mandetory parent connection

for lvl in range(1,height):
		for i in range(workflowlvlcount[lvl]):
			if workflowlvlcount[lvl-1] == 1:
				workflow[lvl][i].parents.append(workflow[lvl-1][0].tid)
				workflow[lvl-1][0].childs.append(workflow[lvl][i].tid)
			else:
				rnd_parent = random.randint(0,workflowlvlcount[lvl-1]-1)
				workflow[lvl][i].parents.append(workflow[lvl-1][rnd_parent].tid)
				workflow[lvl-1][rnd_parent].childs.append(workflow[lvl][i].tid);
			edgecount = edgecount + 1

# phase 4 mandetory child connection
for lvl in range(0,height-1):
		for i in range(workflowlvlcount[lvl]):
			if workflowlvlcount[lvl+1] == 1 and len(workflow[lvl][i].childs) == 0:
				workflow[lvl][i].childs.append(workflow[lvl+1][0].tid)
				workflow[lvl+1][0].parents.append(workflow[lvl][i].tid)
				edgecount = edgecount + 1
			elif len(workflow[lvl][i].childs) == 0:
				rnd_child = random.randint(0,workflowlvlcount[lvl+1]-1)
				workflow[lvl][i].childs.append(workflow[lvl+1][rnd_child].tid)
				workflow[lvl+1][rnd_child].parents.append(workflow[lvl][i].tid)
				edgecount = edgecount + 1

# phase 5 random edge placement
for lvl in range(0,height-1):
		for i in range(workflowlvlcount[lvl]):
			for j in range(workflowlvlcount[lvl+1]):
				putEdge = random.randint(0,100)
				hasEdge = workflow[lvl+1][j].tid in workflow[lvl][i].childs
				if putEdge < EdgeProb*100 and not(hasEdge):
					workflow[lvl][i].childs.append(workflow[lvl+1][j].tid)
					workflow[lvl+1][j].parents.append(workflow[lvl][i].tid)
					edgecount = edgecount + 1

# phase 6 Assigning computational load to all tasks
loadsum = 0
for lvl in range(0,height):
		for i in range(workflowlvlcount[lvl]):
			workflow[lvl][i].load = random.randint(1,Maxload)
			loadsum = loadsum + workflow[lvl][i].load

eff_ccr = CCR * (float(edgecount)/v) * (baseBandwidth/baseMIPS)
filesum = eff_ccr * loadsum;
filesum = int(math.ceil(filesum))

# phase 7 distributing load to edges
# print "file sum = ",filesum, edgecount
edgecountlist = []
for i in range(edgecount):
	edgecountlist.append( random.randint( 1, (filesum-(edgecount-(i+1)))/2  ) )
	filesum = filesum - edgecountlist[-1]

# phase 8 edge cost mapping
for lvl in range(0,height-1):
	for i in range(workflowlvlcount[lvl]):
		for e in range(len(workflow[lvl][i].childs)):
			filesizeInd = random.randint(0,len(edgecountlist)-1)
			filesize = edgecountlist[filesizeInd]
			edgecountlist.pop(filesizeInd)
			workflow[lvl][i].childs[e] = [workflow[lvl][i].childs[e], filesize]
			#find parent in next lvl and update filesize
			for j in range(workflowlvlcount[lvl+1]):
				if workflow[lvl][i].childs[e][0] == workflow[lvl+1][j].tid:
					ind = workflow[lvl+1][j].parents.index(workflow[lvl][i].tid)
					workflow[lvl+1][j].parents[ind] = [workflow[lvl][i].tid, filesize]

printWorkflow(workflow, height, width)
generateWorflowMatrix(workflow, height, width, v)
