# Parts of this code were adapted from:
# https://www.electricmonk.nl/docs/dependency_resolving_algorithm/dependency_resolving_algorithm.html

import json


class Node:
  def __init__(self, name):
    self.name = name
    self.edges = []

  def addEdge(self, node):
    self.edges.append(node)


knowns = []
targets = []
topology = {}

output = []

# import nessecary things
with open("topology.json") as json_file:
  topology = json.load(json_file)

with open("known.txt") as known_file:
  known = known_file.read().splitlines()

with open("target.txt") as target_file:
  target = target_file.read().splitlines()

# create nodes
rootnode = Node("root")
allnodes = []
for key in topology:
  current = Node(key)
  for connection in topology[key]:
    # find node if already exists
    filterres = list(filter(lambda x: x.name == connection, allnodes))
    if len(filterres) == 0:
      node = Node(connection)
    else:
      node = filterres[0]
    current.addEdge(node)

  allnodes.append(current)

for node in allnodes:
  rootnode.addEdge(node)


def dep_resolve(node, resolved):
  print(node.name)
  for edge in node.edges:
    dep_resolve(edge, resolved)
  resolved.append(node)


# main
resolved = []
dep_resolve(rootnode, resolved)
for node in resolved:
  print(node.name, " ")
