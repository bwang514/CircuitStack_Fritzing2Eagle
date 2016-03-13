import xml.etree.ElementTree as ET
import sys
tree = ET.parse(sys.argv[1])
root = tree.getroot()
leftHalfBoardLong = 0
rightHalfBoardLong = 1
lineX = 2
lineY = 3
lineW = 4
lineZ = 5
spaceBetweenTwoLongLine = 17.78
spaceBetweenTwoShortLine = 3.81
leftLongLineStartPoint = [7,4]
rightLongLineStartPoint = [7 + spaceBetweenTwoLongLine , 4]
leftShortLineStartPoint = [13.99 , 8.66]
rightShortLineStartPoint = [13.99 + spaceBetweenTwoShortLine , 8.66]
spaceBetweenTwoPairsOfPadForXZWY = 13.33 
spaceBetweenTwoPad = 2.54
startYCoordinateForXZ = 8.66
startYCoordinateForWY = startYCoordinateForXZ + spaceBetweenTwoPad
wireIndex = 0
signalIndex = 0
def main():	
	signals = readWireFile()
	for signal in signals:
		points = splitWireIntoPoints(signals)
		addsignal(points,signalIndex,wireindex)
	tree.write('output.brd')

def readInputFile():
	signalFile = open('input.txt','r')
	signals  = []
	for line in signalFile.readlines():
		signals.append(line)
	return signals		
def splitWireIntoPoints(wire):
	points = wire.split(',')
	points[0] = splitAlphaAndDigit(points[0])
	points[1] = splitAlphaAndDigit(points[1])	
	return points
def getCoordinate(point):
	if point[0] == leftHalfBoardLong:
		xCoordinate = leftLongLineStartPoint[0]
		yCoordinate = (int(point[1]) - 1) * spaceBetweenTwoPad + leftLongLineStartPoint[1]
	elif point[0] == rightHalfBoardLong:
		xCoordinate = rightLongLineStartPoint[0]
		yCoordinate = (int(point[1]) - 1) * spaceBetweenTwoPad + rightLongLineStartPoint[1]
	elif point[0] == lineX:
		xCoordinate = leftShortLineStartPoint[0]
		yCoordinate = PadOrdertoCoordinate(findClosestPointForXZ(point[1]))
	elif point[0] == lineY:
		xCoordinate = rightShortLineStartPoint[0]
		yCoordinate = PadOrdertoCoordinate(findClosestPointForWY(point[1]))
	elif point[0] == lineW:
		xCoordinate = leftShortLineStartPoint[0]
		yCoordinate = PadOrdertoCoordinate(findClosestPointforWY(point[1]))	
	elif point[0] == lineZ:
		xCoordinate = rightShortLineStartPoint[0]
		yCoordinate = PadOrdertoCoordinate(findClosestPointForXZ(point[1]))	
	Coordinate = [xCoordinate,yCoordinate]
	return Coordinate		
def splitAlphaAndDigit(point):
	Alpha = ord(filter(str.isalpha, point))
	Digit = filter(str.isdigit,point)
	if Alpha <= ord('E'):
		x1 = leftHalfBoardLong
	elif Alpha <= ord('J'):
		x1 = rightHalfBoardLong
	elif Alpha == ord('X'):
		x1 = lineX
	elif  Alpha == ord('Y'):
		x1 = lineY
	elif Alpha == ord('W'): 
		x1 = lineW
	elif Alpha == ord('Z'):
		x1 = lineZ
	Point = [x1,Digit]
	return Point
def findClosestPointForXZ(yAxisOrder):
	yCoordinate = (yAxisOrder - 1) * spaceBetweenTwoPad + leftLongLineStartPoint[1]
	OrderofPadToConnect = yCoordinate / spaceBetweenTwoPairsOfPadForXZWY
	return OrderofPadToConnect
def findClosestPointForWY(yAxisOrder):
	yCoordinate = (yAxisOrder - 1) * spaceBetweenTwoPad + rightLongLineStartPoint[1]
	OrderofPadToConnect = yCoordinate / spaceBetweenTwoPairsOfPadForXZWY
	return OrderofPadToConnect
def PadOrdertoCoordinate(orderofPadToConnect):
	CoordinateToConnect = startYCoordinateForWY + OrderofPadToConnect * spaceBetweenTwoPairsOfPadForXZWY

def addsignal(points,signal_index,wire_index):
	signalLength = len(points)
	for signals in root.iter('signals'):
		newsignal = ET.Element('signal')
		newsignal.set('name','signal' + str(signal_index))
		padNameList = getContactref(points)
		for pad in padNameList:
			newContactref = ET.Element('contactref')
			newContactref.set('name',str(pad)) 
			newContactref.set('pad',"P$1")
			newsignal.append(newContactref)	
		## time to add wire using signal_index and wireindex
		
		signals.append(newsignal)
def getContactref(points):
	padNameList = []
	for point in points:
		Pad = splitAlphaAndDigit(point)
		if Pad[0] == leftHalfBoardLong:
			padName = "LL" + str(point[1])
		elif Pad[0] == rightHalfBoardLong:
			padName = "RL" + str(point[1])
		elif Pad[0] == lineX:
			padName = "LS" + str(findClosestPointForXZ * 2) 
		elif Pad[0] == lineY:
			padName = "RS" + str((findClosestPointForWY * 2 + 1))
		elif Pad[0] == lineW:
			padName = "LS" + str((findClosestPointForWY * 2 + 1))
		elif Pad[0] == lineZ:
			padName = "RS" + str(findClosestPointForXZ * 2)
		padNameList.append(padName)
	return padNameList		 
def addWire(first_point,second_point,signal_index,wire_index):	
	print wire_index
	for wire in root.iter('signals'):
		child = ET.Element('signal')
		child.set('name','wire' + str(wire_index))
		cchild = ET.Element('wire')
		firstPointCoordinate = getCoordinate(first_point)
		secondPointCoordinate = getCoordinate(second_point)
		cchild.set('x1',str(firstPointCoordinate[0]))
		cchild.set('x2',str(secondPointCoordinate[0]))
		cchild.set('y1',str(firstPointCoordinate[1]))
		cchild.set('y2',str(secondPointCoordinate[1]))
		cchild.set('layer','19')
		cchild.set('width','0')
		cchild.set('extent',"1-1")
		child.append(cchild)
		wire.append(child)
	wireIndex = wireIndex + 1		
	
if __name__ == '__main__':
	main()
