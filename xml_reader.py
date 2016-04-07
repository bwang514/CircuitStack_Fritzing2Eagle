import xml.etree.ElementTree as ET
import sys
from zipfile import ZipFile
import os
import re

def main():
	if len(sys.argv) == 2:
		long_board = 0
		# Extract Fzz File for fz only or rename fz file as 'output.fz'.
		extractFile(sys.argv[1])
		
		# Parse from XML files
		tree = ET.parse(os.path.dirname(os.path.abspath(sys.argv[1])) + '/output.fz')
		root = tree.getroot()

		# Directly get instance using iteration.
		instances = getInstances(root)

		# Filter redundant or extra XML instance.
		filteredInstances = filterInstanceWithoutConnetionAndBreadboardOnly(instances)

		# Warning:
		# The object shild contain the names of
		# - 2nd parameter for ID which currently is "moduleIdRef"
		# - 3rd parameter for Breadboard moduleIdRef for wireName type 1 (ex: A32, B4)
		# - 4rd parameter for Breadboard moduleIdRef for wireName type 2 (ex: pin32A, pin4B), and 
		# - 5th parameter for Wire moduleIdRef
		# And Sould only contain "one" Breadboard in the file.
		# This will return the connections on Breadboard "Only".
		
		# Removed:
		# uCirKit-boardModuleID
		
		# WireName type [A,B,C][1,2,3,4]
		boardType1 = ["BreadboardModuleID", "HalfBreadboardModuleID", "TinyBreadboardModuleID", "MiniBreadboardModuleID","HalfMinusBreadboardModuleID"]
		# WireName type pin[1,2,3,4][A,B,C]
		boardType2 = ["Breadboard-RSR03MB102-ModuleID", "13f88e58b86d08d73d112f0fb05e6968"]

		paths, wireType = findConnectionsOnBoard(filteredInstances, "moduleIdRef", boardType1, boardType2, 'WireModuleID', [])
		combinedPaths = combinePaths(paths)

		formatedPaths = formatPaths(combinedPaths, wireType)

		combineBreadboradPointsPaths = combineBreadboardPoints(formatedPaths)
		##print combineBreadboradPointsPaths
		with open('input.txt', 'w') as f:
			for path in combineBreadboradPointsPaths:
				f.write(str(path))
				f.write('\n')
		for path in combineBreadboradPointsPaths:
			for point in path:
				digit = filter(str.isdigit,point)
				if int(digit) > 30:
					long_board = 1
		if long_board == 1:
			print long_board
		else:
			print 0				
				

	else:
		print "ERROR: Please input file name."

def extractFile(filepath):


	filename, file_extension = os.path.splitext(filepath)
	if file_extension == '.fz':
		os.rename(filepath,"output.fz")
	else:
		with open(filepath, 'rb') as file:
			z = ZipFile(file)

			for name in z.namelist():
				if '.fzp' not in name and '.fz' in name:
					z.extract(name)
					os.rename(name,"output.fz")
					break

def getInstances(root):
	
	instances = []

	for child in root.iter('instance'):
		instances.append(child)
	return instances 

def filterInstanceWithoutConnetionAndBreadboardOnly(instances):

	indexToRemove = []
	for x in xrange(0,len(instances)):
		if len(instances[x].findall('*//breadboardView/connectors')) == 0:
			indexToRemove.append(x)
		if instances[x].find('.//views/schematicView') is not None:
			instances[x].find('.//views').remove(instances[x].find('.//views/schematicView'))
		if instances[x].find('.//views/pcbView') is not None:
			instances[x].find('.//views').remove(instances[x].find('.//views/pcbView'))


	indexToRemove = reversed(indexToRemove)
	for index in indexToRemove:
		instances.remove(instances[index])		
	return instances

def findConnectionsOnBoard(instances, moduleId_identifier, bread1Names, bread2Names, wireName, ignoreElementName):

	breadBoardInstance = None
	wireInstances = []
	wireType = None
	for instance in instances:
		if instance.get(moduleId_identifier) in bread1Names:
			if breadBoardInstance == None:
				breadBoardInstance = instance
				wireType = 0
		if instance.get(moduleId_identifier) in bread2Names:
			if breadBoardInstance == None:
				breadBoardInstance = instance
				wireType = 1
		if instance.get(moduleId_identifier) == wireName:
			wireInstances.append(instance)

	if breadBoardInstance == None:
		print "ERROR: Cannot find any breadborad"
		exit()
	# index in BreadBoard to find paths
	indexesToFind = []

	# Paths Description
	pathsOnBoard = []

	# Find connectID on Board and modelIndex for wires
	for connector in breadBoardInstance.iter('connector'):
		for connect in connector.findall('*//connect'):
			if connect.get('modelIndex') not in indexesToFind:
				indexesToFind.append(connect.get('modelIndex'))
			
	for index in indexesToFind:
		wireIDsFoundRelated = findConnectionByModuleIndex(index, wireInstances, [breadBoardInstance.get('modelIndex')])
		# Get related wireInstances
		wireInstancesRelated = []
		for wire in wireInstances:
			if wire.get('modelIndex') in wireIDsFoundRelated:
				wireInstancesRelated.append(wire)

		path = []
		for wire in wireInstancesRelated:
			for connect in wire.findall('*//connect'):

				XYvalue = None
				if wireType == 0:
					XYvalue = re.match(r"([A-Z])(\d{1,2})", connect.get('connectorId'))
				elif wireType == 1:
					XYvalue = re.match(r"pin(\d{1,2})([A-Z])", connect.get('connectorId'))
				if XYvalue:
					if connect.get('connectorId') not in path:
						path.append(connect.get('connectorId'))
		
		if path not in pathsOnBoard and len(path) >= 2:
			pathsOnBoard.append(path)
		
	return pathsOnBoard, wireType

# Return <connect> instances.
def findConnectionByModuleIndex(indexToFind, wireInstances, excludeIDs):
	returnInstances = [indexToFind]
	for wire in wireInstances:
		if wire.get('modelIndex') == indexToFind:
			wiresInThisWire = wire.findall('*//connect')
			for wireInWire in wiresInThisWire:
				if wireInWire.get('modelIndex') not in excludeIDs:
					excludeIDs.append(wire.get('modelIndex'))
					returnInstances.extend(findConnectionByModuleIndex(wireInWire.get('modelIndex'), wireInstances, excludeIDs))
	return returnInstances

def combinePaths(paths):
	sets = []
	removeCount = 0;
	combineIndexes = [];
	noConnection = [];
	# Using set
	for path in paths:
		sets.append(set(path))
	# Test having interset
	for x in xrange(0,len(sets)):
		connection = False
		for y in xrange(0,len(sets)):
			if x == y:
				continue
			elif sets[x].isdisjoint(sets[y]):
				continue
			else:
				connection = True
				existIndex = None
				for z in xrange(0,len(combineIndexes)):
					if not combineIndexes[z].isdisjoint(set([x,y])):
						existIndex = z
				if existIndex == None:
					combineIndexes.append(set([x,y]))
				else:
					combineIndexes[existIndex] = combineIndexes[existIndex].union(set([x,y]))
		if connection == False:
			noConnection.append(list(sets[x]))
	returnPaths = []
	for indexes in combineIndexes:
		paths = set()
		for index in indexes:
			paths = paths.union(sets[index])
		returnPaths.append(list(paths))
	return returnPaths + noConnection

def formatPaths(paths, wireType):
	if wireType == 0:
		for x in xrange(0,len(paths)):
			for y in xrange(0,len(paths[x])):
				XYvalue = re.match(r"([A-Z])(\d{1,2})", paths[x][y])
				paths[x][y] = XYvalue.group(1) + XYvalue.group(2)
	elif wireType==1:
		for x in xrange(0,len(paths)):
			for y in xrange(0,len(paths[x])):
				XYvalue = re.match(r"pin(\d{1,2})([A-Z])", paths[x][y])
				paths[x][y] = XYvalue.group(2) + XYvalue.group(1)
	return paths
def combineBreadboardPoints(paths):
	for x in xrange(0,len(paths)):
		for y in xrange(0,len(paths[x])):
			XYvalue = re.match(r"([A-E])(\d{1,2})", paths[x][y])
			XYvalue2 = re.match(r"([F-J])(\d{1,2})", paths[x][y])
			if XYvalue:
				paths[x][y] = 'A' + XYvalue.group(2)
			elif XYvalue2:
				paths[x][y] = 'F' + XYvalue2.group(2)
			else:
				continue
	paths = combinePaths(paths)
	return paths
if __name__ == '__main__':
	main()