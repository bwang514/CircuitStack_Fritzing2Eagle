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
	signals = readInputFile()
	for signal in signals:
		print 'signal index = ' + str(signalIndex)
		points = splitWireIntoPoints(signal)
		addsignal(points)
	tree.write('output.brd')

def readInputFile():
	signalFile = open('input.txt','r')
	signals  = []
	for line in signalFile.readlines():
		signals.append(line)
	return signals		
def splitWireIntoPoints(wire):
	points = wire.split(',')
	allPoints = []
	for point in points:
		alphaAndDigit = splitAlphaAndDigit(point)
		allPoints.append(alphaAndDigit)
	return allPoints
def getCoordinate(point):
	if point[0] == leftHalfBoardLong:
		xCoordinate = leftLongLineStartPoint[0]
		yCoordinate = (int(point[1]) - 1) * spaceBetweenTwoPad + leftLongLineStartPoint[1]
	elif point[0] == rightHalfBoardLong:
		xCoordinate = rightLongLineStartPoint[0]
		yCoordinate = (int(point[1]) - 1) * spaceBetweenTwoPad + rightLongLineStartPoint[1]
	elif point[0] == lineX:
		xCoordinate = leftShortLineStartPoint[0]
		yCoordinate = PadOrdertoCoordinateXZ(findClosestPointForXZ(int(point[1])))
		print 'x'
	elif point[0] == lineY:
		xCoordinate = rightShortLineStartPoint[0]
		yCoordinate = PadOrdertoCoordinateWY(findClosestPointForWY(int(point[1])))
		print 'y'
	elif point[0] == lineW:
		xCoordinate = leftShortLineStartPoint[0]
		yCoordinate = PadOrdertoCoordinateWY(findClosestPointforWY(int(point[1])))
		print 'w'
	elif point[0] == lineZ:
		xCoordinate = rightShortLineStartPoint[0]
		yCoordinate = PadOrdertoCoordinateXZ(findClosestPointForXZ(int(point[1])))
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
	OrderofPadToConnect = yCoordinate // spaceBetweenTwoPairsOfPadForXZWY
	print OrderofPadToConnect
	print 'hi'
	return OrderofPadToConnect
def findClosestPointForWY(yAxisOrder):
	yCoordinate = (yAxisOrder - 1) * spaceBetweenTwoPad + rightLongLineStartPoint[1]
	OrderofPadToConnect = yCoordinate // spaceBetweenTwoPairsOfPadForXZWY
	return OrderofPadToConnect
def PadOrdertoCoordinateXZ(OrderofPadToConnect):
	CoordinateToConnect = startYCoordinateForXZ + OrderofPadToConnect * spaceBetweenTwoPairsOfPadForXZWY
	return CoordinateToConnect
def PadOrdertoCoordinateWY(OrderofPadToConnect):
	CoordinateToConnect = startYCoordinateForWY + OrderofPadToConnect * spaceBetweenTwoPairsOfPadForXZWY
	return CoordinateToConnect
def addsignal(points):	
	global signalIndex
	global wireIndex
	signalLength = len(points)
	for signals in root.iter('signals'):
		newsignal = ET.Element('signal')
		newsignal.set('name','signal' + str(signalIndex))
		padNameList = getContactref(points)
		for pad in padNameList:
			newContactref = ET.Element('contactref')
			newContactref.set('element',str(pad)) 
			newContactref.set('pad',"P$1")
			newsignal.append(newContactref)	
		## time to add wire using signal_index and wireindex
		for i in range(0,signalLength - 1):
			wire = ET.Element('wire')
			firstPointCoordinate = getCoordinate(points[i])
			secondPointCoordinate = getCoordinate(points[i+1])
			wire.set('x1',str(firstPointCoordinate[0]))
			wire.set('x2',str(secondPointCoordinate[0]))
			wire.set('y1',str(firstPointCoordinate[1]))
			wire.set('y2',str(secondPointCoordinate[1]))
			wire.set('layer','19')
			wire.set('width','0')
			wire.set('extent',"1-1")
			newsignal.append(wire)
			wireIndex = wireIndex + 1		
		signals.append(newsignal)
		signalIndex = signalIndex + 1
def getContactref(points):
	padNameList = []
	for point in points:
		Pad = point
		if Pad[0] == leftHalfBoardLong:
			padName = "LL" + str(point[1])
		elif Pad[0] == rightHalfBoardLong:
			padName = "RL" + str(point[1])
		elif Pad[0] == lineX:
			padName = "LS" + str(int(findClosestPointForXZ(int(point[1]))) * 2) 
		elif Pad[0] == lineY:
			padName = "RS" + str(int((findClosestPointForWY(int(point[1]))) * 2 + 1))
		elif Pad[0] == lineW:
			padName = "LS" + str(int((findClosestPointForWY(int(point[1])))) * 2 + 1)
		elif Pad[0] == lineZ:
			padName = "RS" + str(int(findClosestPointForXZ(int(point[1]))) * 2)
		padNameList.append(padName)
	return padNameList		 
if __name__ == '__main__':
	main()
