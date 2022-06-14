import argparse
import networkx as nx
import math

def cnf_to_primal(numVar,numClause,clauses):
    # code to convert cnf to primal graph in adjacency list form

    edges={}
    for var in range(numVar):
        edges[var]=[]

    for c in range(numClause):
        clique = []

        for var in clauses[c]:
            clique.append(var)

        for j in clique:
            for k in clique:
                if j!=k:
                    edges[j].append(k)
    return edges


def cnf_to_clauseGraph(numVar,numClause,clauses):
    G = nx.Graph()
    
    G.add_nodes_from(range(numClause))
    
    node_dict = {k:[] for k in range(1,numVar+1)}

    for c in range(numClause):
        for var in clauses[c]:
            node_dict[var].extend([c])

    for key, value in node_dict.items():
        for v1 in value:
            for v2 in value:
                if v1!=v2:
                    G.add_edge(v1,v2)  
    return G

def mis_coverage(clauses,mis):
    coverage = set([])

    for clause in mis:
        coverage = coverage.union(set(clauses[clause]))
    
    return coverage    

def multiplier(clauses,mis,num_uncovered):
    m = int(2**num_uncovered)
    for clause in mis:
        m*=2**len(clauses[clause]) - 1
    return math.log(m,2)    


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

primal_graph = cnf_to_primal(numVar,numClause,clauses)
clause_graph = cnf_to_clauseGraph(numVar,numClause,clauses)
mis =  nx.maximal_independent_set(clause_graph)
print("length of max ind set and #clause", len(mis), numClause)

#print("mis", mis)

all_vars = range(1,numVar+1)
covered_vars = mis_coverage(clauses,mis)
uncovered_vars = set(all_vars) - set(covered_vars)

print("size of union of vars of mis", len(covered_vars))

print("multiplier, #var", multiplier(clauses,mis,len(uncovered_vars)), numVar)

print(primal_graph)

exit(0)