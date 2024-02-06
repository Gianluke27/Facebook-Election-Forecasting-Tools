#from func_timeout import func_timeout
from time import time
from facebook2 import facebook_friend, facebook_enmy

def read_graph1(filename):
    infile = open(filename, 'r')
    V=set()
    E=dict()
        
    for line in infile:
        nodes=line.split()
        if nodes[0] not in V:
            V.add(nodes[0])
        if nodes[1] not in V:
            V.add(nodes[1])
        E[(nodes[0],nodes[1])]=int(nodes[2])
    infile.close()
    return V, E

def read_graph2(filename):
    infile = open(filename, 'r')
    V=dict()
    E=dict()
    edge_mode=False
        
    for line in infile:
        if line == "Edges\n":
            edge_mode=True
            continue
        if not edge_mode:
            nodes=line.split()
            V[nodes[0]] = (int(nodes[1]),int(nodes[2]))
        else:
            nodes=line.split()
            E[(nodes[0],nodes[1])] = int(nodes[2])
    infile.close()
    return V, E

def mytest1():
    outfile=open("results1_old.txt", 'w')
    V, E=read_graph1("test-graph1.txt")
    try:
        start = time()
#        dem, rep = func_timeout(10800,facebook_enmy,(V, E))
        dem, rep = facebook_enmy(V,E)
        end = time()-start
        print("dem: ", dem)
        print("rep: ", rep)
        result = 0
        for i in dem:
            for j in rep:
                if (i, j) in E.keys():
                    result += E[(i,j)]
                elif (j, i) in E.keys():
                    result += E[(j,i)]
        outfile.write(str(result)+"\n")
        outfile.write(str(end))
    except Exception as e:
        outfile.write("Error\n")
        outfile.write(str(e))
    outfile.close()

def mytest2():
    outfile=open("results2.txt",'w')
    V, E=read_graph2("test-graph2.txt")
    try:
        start = time()
    #        dem, rep = func_timeout(10800,facebook_friend,(V, E))
        dem, rep = facebook_friend(V, E)
        end = time()-start
        result = 0
        for i in dem:
            result += V[i][1]
        for i in rep:
            result += V[i][0]
        for i in dem:
            for j in rep:
                if (i, j) in E.keys():
                    result += E[(i,j)]
                elif (j, i) in E.keys():
                    result += E[(j,i)]
        outfile.write(str(result)+"\n")
        outfile.write(str(end))
    except Exception as e:
        outfile.write("Error\n")
        outfile.write(str(e))
    outfile.close()
    
mytest1()
#mytest2()
