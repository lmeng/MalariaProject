import matplotlib.pyplot as plt
import os
import math
import sys
import scipy
import scipy.stats

NODES = 'nodes'
EDGES = 'edges'

def read_graph(path):
    node_table = {}
    nodes = set([])
    edges = set([])

    fi = open(path, 'rb')
    next(fi)
    next(fi)
    next(fi)
    cnt = int(next(fi))
    idx = 1
    for i in range(0, cnt):
        node = next(fi).rstrip()
        node = node[2:-2]
        node_table[idx]=node
	nodes.add(node)
	idx = idx + 1

    cnt = int(next(fi))
    for i in range(0, cnt):
	tokens = next(fi).rstrip().split()
	node1 = node_table[int(tokens[0])]
	node2 = node_table[int(tokens[1])]

	if node1 <= node2:
	    edge = node1 + '_' + node2
	else:
	    edge = node2 + '_' + node1
	edges.add(edge)

    G = {NODES: nodes, EDGES: edges}
    return G

#The percentage of edge in the overlap of the two networks 
#divided by the number of nodes in the smaller network
def edge_correctness(edgeSet1, edgeSet2):
	cnt = 0
	for edge in edgeSet1:
		if edge in edgeSet2:
			cnt = cnt + 1
	
	res = cnt * 1.0 / min(len(edgeSet1), len(edgeSet2))
	return res

#Hypergeometric test of the edge overlap
#E1: the number of edges in the first network
#E2: the number of edges in the second network
#V2: the number of nodes in the second network
#P: the number of edges in the overlap of the two networks
def p_value(E1, E2, V2, P):
	p = 1 - scipy.stats.hypergeom.cdf(P-1, V2*(V2-1)/2, E2, E1)
	return p


def compute(G1, G2):
	correctness = edge_correctness(G1[NODES], G2[NODES])

	E1 = len(G1[EDGES])
	E2 = len(G2[EDGES])
	V2 = len(G2[NODES])
	P = len(G1[EDGES] & G2[EDGES])
	pvalue = p_value(E1, E2, V2, P)
	return (correctness, pvalue)

def compute_pairwise_graphs(L):
	for i in range(0, len(L)):
		print L[i]


def main_func(files, labels, outname):
	L = []
	for file in files:
		G = read_graph(file)
		L.append(G)

	R = {}
	for i in range(0, len(L)):
		tmp = {}
		for j in range(0, len(L)):
			tmp[labels[j]] = compute(L[i], L[j])
		R[labels[i]] = tmp

	#print correctness table
	res = ''
	for label in labels:
		res = res + '\t' + label
	res = res + '\n'
	for label1 in labels:
		res = res + label1
		for label2 in labels:
			res = res + '\t' + str(R[label1][label2][0])
		res = res + '\n'

	if not os.path.exists('EdgeOverlap'):
		os.makedirs('EdgeOverlap')
	f = open('EdgeOverlap/'+outname + '_edgeoverlap.txt', 'wb')
	print >>f, res
	f.close()

        #print p-value table
        res = ''
        for label in labels:
                res = res + '\t' + label
        res = res + '\n'
        for label1 in labels:
                res = res + label1
                for label2 in labels:
                        res = res + '\t' + str(R[label1][label2][1])
                res = res + '\n'
	f = open('EdgeOverlap/' + outname + '_edgeoverlap_pvalue.txt', 'wb')
	print >>f, res
	f.close()

def main():
	files = ['gw_malaria141/R_P.gw', 'gw_malaria141/SR_P.gw', 'gw_malaria141/NR_P.gw', 'gw_malaria141/VNR_P.gw']
	labels = ['R', 'SR', 'NR', 'VNR']
	outname = 'malaria141_P'
	main_func(files, labels, outname)

	files = ['gw_malaria141/R_PN.gw', 'gw_malaria141/SR_PN.gw', 'gw_malaria141/NR_PN.gw', 'gw_malaria141/VNR_PN.gw']
        labels = ['R', 'SR', 'NR', 'VNR']
        outname = 'malaria141_PN'
        main_func(files, labels, outname)

	files = ['gw_malaria144/R_P.gw', 'gw_malaria144/SR_P.gw', 'gw_malaria144/NR_P.gw', 'gw_malaria144/VNR_P.gw']
        labels = ['R', 'SR', 'NR', 'VNR']
        outname = 'malaria144_P'
        main_func(files, labels, outname)

	files = ['gw_malaria144/R_PN.gw', 'gw_malaria144/SR_PN.gw', 'gw_malaria144/NR_PN.gw', 'gw_malaria144/VNR_PN.gw']
        labels = ['R', 'SR', 'NR', 'VNR']
        outname = 'malaria144_PN'
        main_func(files, labels, outname)

if __name__ == "__main__":
    main()
