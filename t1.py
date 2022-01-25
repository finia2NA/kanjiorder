import json
from functools import reduce


class Node:
  def __init__(self, name):
    self.name = name
    self.edges = []

  def addEdge(self, node):
    self.edges.append(node)


targets = []
topology = {}

# import nessecary things
with open("topology.json") as json_file:
  topology = json.load(json_file)

with open("known.txt") as known_file:
  known = known_file.read().splitlines()

with open("target.txt") as target_file:
  targets = target_file.read().splitlines()


def findOrCreateNode(name, thelist):
  node = None
  filterres = list(filter(lambda x: x.name == name, thelist))
  if len(filterres) == 0:
    node = Node(name)
  else:
    node = filterres[0]
  return node


def buildGraph():
  # create nodes
  allnodes = [Node("0")]
  for key in topology:
    # find out of i already exists
    current = findOrCreateNode(key, allnodes)
    for connection in topology[key]:
      # find node if already exists
      node = findOrCreateNode(connection, allnodes)
      current.addEdge(node)

    allnodes.append(current)
  return allnodes


graph = buildGraph()


def dep_resolve(node, resolved):
  # source: https://www.electricmonk.nl/docs/dependency_resolving_algorithm/dependency_resolving_algorithm.html
  for edge in node.edges:
    if edge not in resolved:
      dep_resolve(edge, resolved)
  resolved.append(node)


def d1(name):
  resolved = []
  node = list(filter(lambda x: x.name == name, graph))[0]
  dep_resolve(node, resolved)
  return resolved


def d2(targets):
  resolved = []
  for name in targets:
    try:
      node = list(filter(lambda x: x.name == name, graph))[0]
      dep_resolve(node, resolved)
    except:
      print("something went wrong for " + name)
  return resolved


# node = list(filter(lambda x: x.name == "会", graph))[0]
res = d2(targets)

print("Whole order:")
print(list(map(lambda x: x.name, res)))

print("New ones:")
print(list(filter(lambda x: x not in known, map(lambda x: x.name, res))))
