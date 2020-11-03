import math
import sys

def takeSecond(elem):
    return float(elem.split("\t")[1])

def sort_y(elem):
    return float(elem[3])

def endiamesoi_komvoi(epipedo):
	global k
	area1=0
	george=vectors[:]
	x_low=[]
	x_high=[]
	y_low=[]
	y_high=[]
	lst3=[]
	lst4=[]
	for j in range(0,epipedo):
		for i in range(0,min(int(leaves),len(george[j-epipedo][1]))):
			x_low.append(float(george[j-epipedo][1][i][1]))
			x_high.append(float(george[j-epipedo][1][i][2]))
			y_low.append(float(george[j-epipedo][1][i][3]))
			y_high.append(float(george[j-epipedo][1][i][4]))
		lst3.append((george[j-epipedo][0]))
		lst3.append(min(x_low))
		lst3.append(max(x_high))
		lst3.append(min(y_low))
		lst3.append(max(y_high))
		lst4.append(lst3)
		area1=area1+((float(lst3[2])-float(lst3[1]))*(float(lst3[4])-float(lst3[3])))
		lst3=[]
		x_low=[]
		x_high=[]
		y_low=[]
		y_high=[]
		if(j%leaves==(leaves-1) or j==epipedo-1):
			vectors.append([k,lst4])
			k=k+1
			lst4=[]
	area_levels.append(area1/epipedo)

def intersection(RCT_q,RCT):
	if RCT_q[1]>RCT[2] or RCT[1]>RCT_q[2]:
		return False
	if RCT_q[4]<RCT[3] or RCT[4]<RCT_q[3]:
		return False
	return True

def intersection_query(rectangle,node):
	global number_retangle, node_accesses

	if node not in leaves_node:
		node_accesses=node_accesses+1
		for i in range(0,len(vectors[node][1])):
			if intersection(rectangle,vectors[node][1][i])==True:
				node1=vectors[node][1][i][0]
				intersection_query(rectangle,node1)
	if node in leaves_node:
		node_accesses=node_accesses+1
		for j in range(0,len(vectors[node][1])):
			if intersection(rectangle,vectors[node][1][j])==True:
				number_retangle=number_retangle+1
	
def inside(RCT_q,RCT):
	if RCT_q[4]>=RCT[4] and RCT_q[3]<=RCT[3] and RCT_q[1]<=RCT[1] and RCT_q[2]>=RCT[2]:
		return True
	return False

def inside_query(rectangle,node):
	global number_retangle, node_accesses

	if node not in leaves_node:
		node_accesses=node_accesses+1
		for i in range(0,len(vectors[node][1])):
			if intersection(rectangle,vectors[node][1][i])==True:
				node1=vectors[node][1][i][0]
				inside_query(rectangle,node1)
	if node in leaves_node:
		node_accesses=node_accesses+1
		for j in range(0,len(vectors[node][1])):
			if inside(rectangle,vectors[node][1][j])==True:
				number_retangle=number_retangle+1

def containment_query(rectangle,node):
	global number_retangle, node_accesses

	if node not in leaves_node:
		node_accesses=node_accesses+1
		for i in range(0,len(vectors[node][1])):
			if intersection(rectangle,vectors[node][1][i])==True:
				node1=vectors[node][1][i][0]
				containment_query(rectangle,node1)
	if node in leaves_node:
		node_accesses=node_accesses+1
		for j in range(0,len(vectors[node][1])):
			if inside(vectors[node][1][j],rectangle)==True:
				number_retangle=number_retangle+1

arxeio=sys.argv[1] #arxeio eisodou
block_size=int(sys.argv[2]) #block size
vectors=[] #oloi oi komboi mou
levels=[] #ta epipeda mou
area_levels=[] #ta embada
leaves_node=[] #ta fylla
lst=list(open(arxeio)) 
N=len(lst)
f=math.floor(block_size/36)
leaves=f
L=math.ceil(N/f)
lst.sort(key=takeSecond)
levels.append(int(L))
rectangles=f*(math.ceil(math.sqrt(L)))
k=0
for i in range (0,int(leaves)):
	result=int(math.ceil(levels[i]/leaves))
	if result==1:
		levels.append(result)
		break
	levels.append(result)
lst1=[]
lst2=[]
area=0
#EPIPEDO 0 FYLLA
for i in range(0,N):
	field=lst[i].split("\t")
	field = [f.strip() for f in field]
	field[0]=int(field[0])
	for b in range(1,len(field)):
		field[b]=float(field[b])
	area=area+((float(field[2])-float(field[1]))*(float(field[4])-float(field[3])))
	lst1.append(field)
	if(i%rectangles==(rectangles-1) or i==N-1):
		lst1.sort(key=sort_y)
		for j in range(0,len(lst1)):
			lst2.append(lst1[j])
			if(j%leaves==(leaves-1) or j==(len(lst1)-1)):
				vectors.append([k,lst2])
				leaves_node.append(k)
				k=k+1
				lst2=[]
		lst1=[]
area_levels.append(area/N)
#TELOS EPIPEDOU 0

#DHMIOURGIA OLWN TWN EPIPEDWN
for i in range (0,len(levels)-1):
	endiamesoi_komvoi(levels[i])
#TELOS EPIPEDWN

#Grafo sto arxeio
with open('rtree.txt', 'w') as f:
	f.write(str(vectors[-1][0])+"\n")
	f.write(str(len(levels))+"\n\n")
	for item in vectors:
		f.write(str(item[0])+", ")
		f.write(str(len(item[1]))+", ")
		f.write("%s\n" % item[1])
		f.write("\n")
f.close()

#Typono ta apotelesmata
word=""
word1=""
print "The heigt of r-tree is: ",len(levels)
for i in range (0,len(levels)):
	word=word+str(levels[i])+" "
	word1=word1+str(area_levels[i])+" "
print "The numbers of nodes at each level is: ",word
print "Average MBRs area at each level is: ",word1

#---------------------2o MEROS-----------------------------
number_retangle=0
node_accesses=0
lst_query=list(open("query_rectangles.txt"))
for i in range(0,len(lst_query)):
	field1=lst_query[i].split("\t")
	field1 = [f.strip() for f in field1]
	for j in range(0,len(field1)):
		field1[j]=float(field1[j])
	lst_query[i]=field1
#typodi olwn twn apotelesmatvn twn ervtisewn
print "-------------INTERSECTION QUERY-------------"
print "query-id  Number of retangle   Node accesses"
for i in range(0,len(lst_query)):
	intersection_query(lst_query[i],int(vectors[-1][0]))
	print repr(i).rjust(2),"            ", repr(number_retangle).rjust(4),"             ",repr(node_accesses).rjust(3)
	number_retangle, node_accesses=0,0
print "----------------INSIDE QUERY----------------"
print "query-id  Number of retangle   Node accesses"
number_retangle, node_accesses=0,0
for i in range(0,len(lst_query)):
	inside_query(lst_query[i],int(vectors[-1][0]))
	print repr(i).rjust(3),"            ", repr(number_retangle).rjust(4),"             ",repr(node_accesses).rjust(3)
	number_retangle, node_accesses=0,0
print "--------------CONTAINMENT QUERY-------------"
print "query-id  Number of retangle   Node accesses"
number_retangle, node_accesses=0,0
for i in range(0,len(lst_query)):
	containment_query(lst_query[i],int(vectors[-1][0]))
	print repr(i).rjust(2),"            ", repr(number_retangle).rjust(4),"             ",repr(node_accesses).rjust(3)
	number_retangle, node_accesses=0,0