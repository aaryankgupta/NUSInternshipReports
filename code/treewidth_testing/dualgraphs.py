import argparse
import networkx as nx
import math

def cnf_to_dual(numVar,numClause,clauses):
    # code to convert cnf to dual graph in adjacency list form

    edges={}
    for clause in range(numClause):
        edges[clause]=[]

    for v in range(numVar):
        clique = []

        for c in range(numClause):
            if v in clauses[c]:
                clique.append(c)     

        for j in clique:
            for k in clique:
                if j!=k:
                    edges[j].append(k)

    
    for c in range(numClause):
        edges[c]=set(edges[c])

    return edges

parser = argparse.ArgumentParser()
parser.add_argument("input", help="input file")
#parser.add_argument("output", help="output file")

args = parser.parse_args()

inputFile = open(args.input,'r')
cnf = inputFile.readlines()
inputFile.close()

numVar,numClause = 0,0

clauses = []
for clause in cnf:
    if len(clause.strip()) == 0 or clause.startswith(('x','w','c')):
        continue
    elif clause.startswith('p'):
        header = clause.strip().split()
        numVar = int(header[2])    
    else:
        clauses.append([abs(int(i)) for i in clause.strip().split()][:-1])

numClause = len(clauses)



dual_graph= cnf_to_dual(numVar,numClause,clauses)

# print(dual_graph)

numedges=0
for c in range(numClause):
    numedges+=len(dual_graph[c])

numedges=numedges//2

with open("dualgraph.gr", "w") as external_file:
    print('p tw '+ str(numClause) + ' '+ str(numedges), file=external_file)
    for c in range(numClause):
        for c2 in dual_graph[c]:
            if(c<c2):
                print(str(c+1)+' '+str(c2+1), file=external_file)

    external_file.close()
