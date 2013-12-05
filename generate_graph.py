import os
import sys
import argparse

import networkx as nx
import numpy as np
import scipy.sparse
import itertools


def gen_graph(vertex_num, edge_prob):
  '''
  Genereate Erdos-Renyi binomial graphs with given nodes number and
  edge probablity, and return as scipy sparse matrix

  Parameters
  ----------
  vertex_num : int
      number of vertex
  edge_prob : float
      probality to craete a edge

  Return
  ---------
  m : SciPy sparse matrix
      Graph adjacency matrix.
  '''
  graph = nx.erdos_renyi_graph(vertex_num, edge_prob, False)
  graph_sparse_m = nx.to_scipy_sparse_matrix(graph)
  return graph_sparse_m


def loadgraph(fn):
  """
  Load a numpy-saved graph from disk

  @param fn: the file path and name of the saved graph
  @return: the loaded sparse csc scipy matrix
  """
  assert os.path.exists(fn), "The specified file path: %s does not exist" % str(fn)
  return np.load(fn).item()

def output_giraph_json(filename, m):
  '''
  out put sparse matrix into
  giraph JsonLongDoubleFloatDoubleVertexInputFormat

  Here is an example with vertex id 1, vertex value 4.3, and two edges.
  First edge has a destination vertex 2, edge value 2.1.
  Second edge has a destination vertex 3, edge value 0.7.
  [1,4.3,[[2,2.1],[3,0.7]]]

  Parameters
  ----------
  filename : string
    output file name
  m : SciPy sparse matrix
    Graph adjacency matrix
  '''
  coo_m = scipy.sparse.coo_matrix(m)
  with open(filename, 'w') as file:
    prev_i = -1
    for i,j,v in zip(coo_m.row, coo_m.col, coo_m.data):
      if i != prev_i:
        if prev_i != -1:
          file.write("]]\n")
        file.write("[%d,0,[[%d,1]" % (i,j))
        prev_i = i
      else:
        file.write(",[%d,1]" % j)


def output_giraph_intIntNullText(filename, m):
  '''
  out put sparse matrix into
  giraph  IntIntNullTextInputFormat

  Each line consists of: vertex neighbor1 neighbor2 ...

  Parameters
  ----------
  filename : string
    output file name
  m : SciPy sparse matrix
    Graph adjacency matrix
  '''
  coo_m = scipy.sparse.coo_matrix(m)
  with open(filename, 'w') as outf:
    prev_i = -1
    for i,j,v in itertools.izip(coo_m.col, coo_m.row, coo_m.data):
      if i != prev_i:
        if prev_i != -1:
          outf.write("\n")
        outf.write("%d %d" % (i,j))
        prev_i = i
      else:
        outf.write(" %d" % j)

