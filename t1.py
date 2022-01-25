# Parts of this code were adapted from:
# https://www.electricmonk.nl/docs/dependency_resolving_algorithm/dependency_resolving_algorithm.html

import json


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


def findOrCreateNode(name, thelist, rootnode):
  node = None
  filterres = list(filter(lambda x: x.name == name, thelist))
  if len(filterres) == 0:
    node = Node(name)
  else:
    node = filterres[0]
  return node


def buildGraph(rootnode):
  # create nodes
  allnodes = []
  for key in topology:
    # find out of i already exists
    current = findOrCreateNode(key, allnodes, rootnode)
    for connection in topology[key]:
      # find node if already exists
      node = findOrCreateNode(connection, allnodes, rootnode)
      current.addEdge(node)

    allnodes.append(current)
  return allnodes


rootnode = Node("0")
graph = buildGraph(rootnode)

resolved = [rootnode.name]

while len(targets) > 0:
  for t in targets:
    targetNode = list(filter(lambda x: x.name == t, graph))[0]
    allEdgedResolved = True

    for edge in targetNode.edges:
      if edge.name not in resolved:
        allEdgedResolved = False
        break

    if allEdgedResolved:
      resolved.append(t)
      targets.remove(t)

print(":D")
