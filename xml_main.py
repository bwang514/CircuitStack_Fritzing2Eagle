import xml.etree.ElementTree as ET
import sys
import os
import commands
( status ,  output ) = commands.getstatusoutput("python xml_reader.py " + sys.argv[1]) 
print  output
if int(output) == 0:
	print "short board"
	brd = "tmp_30.brd"
else:
	print "long board"
	brd = "tmp_64.brd"
os.system("python xml_reader.py " + sys.argv[1])
tree = ET.parse(brd)
root = tree.getroot()
print root
leftHalfBoardLong = 0
rightHalfBoardLong = 1
line1_x = 7
line1_y = 4
line4_x = 24.78
line4_y = 4
line2_x = 13.99
line2_y = 8.66
line3_x = 13.99 + 3.81
line3_y = 8.66
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
LL = []
LS = []
RL = []
RS = []
def main():	
	signals = readInputFile()
	if	int(output) == 1:
		buildShortLine()
		print "hihih"	
	else: 
		buildShortLine30()
	for signal in signals:
		#print 'signal index = ' + str(signalIndex)
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
def getCoordinateFromTwoPoints(point1,point2):
	print "point1 = " + str(point1) + " point2 = " + str(point2)
	if point1[0] >= lineX and point2[0] >= lineX:
		if point1[0] == lineX or point1[0] == lineZ:
			index = findClosestPointForXZ(int(point1[1]) - 1)
			Yaxis = PadOrdertoCoordinateXZ(index) 
		elif point1[0] == lineW or point1[0] == lineY:
			index =  findClosestPointForWY(int(point1[1]) - 1)
			Yaxis = PadOrdertoCoordinateWY(index)
		if point1[0] == lineX or point1[0] == lineW:
			Coordinate1 = [leftShortLineStartPoint[0],Yaxis]
			if point2[0] == lineX:
				Coordinate2 = [leftShortLineStartPoint[0],PadOrdertoCoordinateXZ(index)]
			elif point2[0] == lineW:	
				Coordinate2 = [leftShortLineStartPoint[0],PadOrdertoCoordinateWY(index)]
			elif point2[0] == lineY:
				Coordinate2 = [rightShortLineStartPoint[0],PadOrdertoCoordinateWY(index)]
			elif point2[0] == lineZ:
				Coordinate2 = [rightShortLineStartPoint[0],PadOrdertoCoordinateXZ(index)]
		elif point1[0] == lineY or point1[0] == lineZ:
			Coordinate1 = [rightShortLineStartPoint[0],Yaxis]
			if point2[0] == lineX: 
				Coordinate2 = [leftShortLineStartPoint[0],PadOrdertoCoordinateXZ(index)]
			elif point2[0] == lineW:	
				Coordinate2 = [leftShortLineStartPoint[0],PadOrdertoCoordinateWY(index)]
			elif point2[0] == lineY:
				Coordinate2 = [rightShortLineStartPoint[0],PadOrdertoCoordinateWY(index)]
			elif point2[0] == lineZ:
				Coordinate2 = [rightShortLineStartPoint[0],PadOrdertoCoordinateXZ(index)]																	
	elif point1[0] >= lineX and point2[0] < lineX:
		if point1[0] == lineX or point1[0] == lineZ: 
			if point1[0] == lineX:
				Coordinate1 = [leftShortLineStartPoint[0],PadOrdertoCoordinateXZ(findClosestPointForXZ(int(point2[1]) - 1))]
			elif point1[0] == lineZ:
				Coordinate1 = [rightShortLineStartPoint[0],PadOrdertoCoordinateXZ(findClosestPointForXZ(int(point2[1]) - 1))]			
			Coordinate2 = getCoordinate(point2)
		elif point1[0] == lineW or point1[0] == lineY: 
			if point1[0] == lineW: 
				Coordinate1 = [leftShortLineStartPoint[0],PadOrdertoCoordinateWY(findClosestPointForWY(int(point2[1]) - 1))]
			elif point1[0] == lineY:
				Coordinate1 = [rightShortLineStartPoint[0],PadOrdertoCoordinateWY(findClosestPointForWY(int(point2[1]) - 1))]	
			Coordinate2 = getCoordinate(point2)
	elif point1[0] < lineX and point2[0] >=lineX:
		if point2[0] == lineX or point2[0] == lineZ:  
			Coordinate1 = getCoordinate(point1)
			if point2[0] == lineX: 
				Coordinate2 = [leftShortLineStartPoint[0],PadOrdertoCoordinateXZ(findClosestPointForXZ(int(point1[1]) - 1))]
			elif point2[0] == lineZ:
				Coordinate2 = [rightShortLineStartPoint[0],PadOrdertoCoordinateXZ(findClosestPointForXZ(int(point1[1]) - 1))]
		elif point2[0] == lineW or point2[0] == lineY:
			Coordinate1 = getCoordinate(point1)
			if point2[0] == lineW: 
				Coordinate2 = [leftShortLineStartPoint[0],PadOrdertoCoordinateWY(findClosestPointForWY(int(point1[1]) - 1))]
			elif point2[0] == lineY:
				Coordinate2 = [rightShortLineStartPoint[0],PadOrdertoCoordinateWY(findClosestPointForWY(int(point1[1]) - 1))]
	elif point1[0] < lineX and point2[0] < lineX:
		Coordinate1 = getCoordinate(point1)
		Coordinate2 = getCoordinate(point2)
	Coordinate = [Coordinate1,Coordinate2]
	#print Coordinate
	return Coordinate			
def getCoordinate(point):
	if point[0] == leftHalfBoardLong:
		xCoordinate = leftLongLineStartPoint[0]
		yCoordinate = (63 - (int(point[1]) - 1)) * spaceBetweenTwoPad + leftLongLineStartPoint[1]
	elif point[0] == rightHalfBoardLong:
		xCoordinate = rightLongLineStartPoint[0]
		yCoordinate = (63 - (int(point[1]) - 1)) * spaceBetweenTwoPad + rightLongLineStartPoint[1]
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
	print "y input = " + str(yAxisOrder)
	min_distance = 999999999
	for i in range(0,12):	
		distance = abs(((63 - int(yAxisOrder)) * spaceBetweenTwoPad + 4) - (line3_y + i * 13.33))
		if distance < min_distance : 
			min_distance = distance
			OrderofPadToConnect = i
	print "find" + str(OrderofPadToConnect)		
	return OrderofPadToConnect
def findClosestPointForWY(yAxisOrder):
	min_distance = 999999999
	for i in range(0,12):	
		distance = abs(((63 - int(yAxisOrder)) * spaceBetweenTwoPad + 4) - (line3_y + i * 13.33 + 2.54))
		#print distance
		if distance < min_distance: 
			min_distance = distance 
			OrderofPadToConnect = i
	return OrderofPadToConnect
def PadOrdertoCoordinateXZ(OrderofPadToConnect):
	print "order in XZ = " + str(OrderofPadToConnect)
	CoordinateToConnect = startYCoordinateForXZ + (OrderofPadToConnect) * spaceBetweenTwoPairsOfPadForXZWY
	return CoordinateToConnect
def PadOrdertoCoordinateWY(OrderofPadToConnect):
	CoordinateToConnect = startYCoordinateForWY + OrderofPadToConnect * spaceBetweenTwoPairsOfPadForXZWY
	return CoordinateToConnect
def addsignal(points):	
	global signalIndex
	global wireIndex
	Coordinates = []
	signalLength = len(points)
	for signals in root.iter('signals'):
		newsignal = ET.Element('signal')
		newsignal.set('name','signal' + str(signalIndex))
		padNameList = getContactref(points)
		for pad in padNameList:
			newContactref = ET.Element('contactref')
			newContactref.set('element',str(pad)) 
			newContactref.set('pad',"1")
			newsignal.append(newContactref)	
		## time to add wire using signal_index and wireindex
		for i in range(0,signalLength - 1):
			wire = ET.Element('wire')
			Coordinates = getCoordinateFromTwoPoints(points[i],points[i+1])
			firstPointCoordinate = Coordinates[0]
			secondPointCoordinate = Coordinates[1]
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
def addPadOnTheBoard(line,index,Coordinate):
	for wire in root.iter('elements'):
		child = ET.Element('element')
    	child.set('name',str(line) + str(int(index)))
    	child.set('library',"SparkFun-Connectors") 
    	child.set('package',"1X01")
    	child.set('value',"")
    	child.set('x',str(Coordinate[0]))
    	child.set('y',str(Coordinate[1]))
    	wire.append(child)
def buildShortLine():
	for wire in root.iter('elements'):
		for j in range(0, 24, +2):
			child = ET.Element('element')
			child.set('name','RS' + str(24 - j - 2))
			child.set('library',"SparkFun-Connectors")
			child.set('package',"1X01")
			child.set('value',"")
			child.set('x',str(line3_x))
			child.set('y',str(line3_y + (j/2) * 13.33 + 2.54))
			wire.append(child)
			child = ET.Element('element')
			child.set('name','LS' + str(24 - j - 2))
			child.set('library',"SparkFun-Connectors")
			child.set('package',"1X01")
			child.set('value',"")
			child.set('x',str(line2_x))
			child.set('y',str(line2_y + (j/2) * 13.33 + 2.54))
			wire.append(child)								
			child = ET.Element('element')
			child.set('name','RS' + str(24 - j - 1))
			child.set('library',"SparkFun-Connectors")
			child.set('package',"1X01")
			child.set('value',"")
			child.set('x',str(line3_x))
			child.set('y',str(line3_y + (j/2) * 13.33))
			wire.append(child)
			child = ET.Element('element')
			child.set('name','LS' + str(24 - j - 1))
			child.set('library',"SparkFun-Connectors")
			child.set('package',"1X01")
			child.set('value',"")
			child.set('x',str(line2_x))
			child.set('y',str(line2_y + (j/2) * 13.33))
			wire.append(child)
def buildShortLine30():	
   	for wire in root.iter('elements'):
		for j in range(0, 12, +2):
			child = ET.Element('element')
			child.set('name','RS' + str(12 - j - 2))
			child.set('library',"SparkFun-Connectors")
			child.set('package',"1X01")
			child.set('value',"")
			child.set('x',str(line3_x))
			child.set('y',str(line3_y + (j/2) * 13.33 + 2.54 + 87.82))
			wire.append(child)
			child = ET.Element('element')
			child.set('name','LS' + str(12 - j - 2))
			child.set('library',"SparkFun-Connectors")
			child.set('package',"1X01")
			child.set('value',"")
			child.set('x',str(line2_x))
			child.set('y',str(line2_y + (j/2) * 13.33 + 2.54 + 87.82))
			wire.append(child)								
			child = ET.Element('element')
			child.set('name','RS' + str(12 - j - 1))
			child.set('library',"SparkFun-Connectors")
			child.set('package',"1X01")
			child.set('value',"")
			child.set('x',str(line3_x))
			child.set('y',str(line3_y + (j/2) * 13.33 + 87.82))
			wire.append(child)
			child = ET.Element('element')
			child.set('name','LS' + str(12 - j - 1))
			child.set('library',"SparkFun-Connectors")
			child.set('package',"1X01")
			child.set('value',"")
			child.set('x',str(line2_x))
			child.set('y',str(line2_y + (j/2) * 13.33 + 87.82))
			wire.append(child)			
def getContactref(points):
	padNameList = []
	global LL
	global LS
	global RL
	global RS
	length = len(points)
	print points
	for i in range(0,length):
		Pad = points[i]
		print "Pad = " + str(Pad) 
		index = int(points[i][1]) - 1
		print points[i-1]
		yaxis = int(points[i - 1][1]) - 1
		print "yaxis = " + str(yaxis)
		if Pad[0] == leftHalfBoardLong:
			padName = "LL" + str(index)
			if index not in LL:
				Coordinate = getCoordinate(points[i])
				LL.append(index)
				addPadOnTheBoard("LL",str(index),Coordinate)
		elif Pad[0] == rightHalfBoardLong:
			padName = "RL" + str(index)
			if index not in RL:
				Coordinate = getCoordinate(points[i])
				RL.append(index)
				addPadOnTheBoard("RL",str(index),Coordinate)		
		elif Pad[0] == lineX:
			padName = "LS" + str((11 - findClosestPointForXZ(yaxis)) * 2 + 1) 
		elif Pad[0] == lineY:
			padName = "RS" + str((11 - findClosestPointForWY(yaxis)) * 2)
		elif Pad[0] == lineW:
			padName = "LS" + str((11 - findClosestPointForWY(yaxis)) * 2)
		elif Pad[0] == lineZ:
			print "order in contred = " +str(findClosestPointForXZ(yaxis))
			padName = "RS" + str((11 - findClosestPointForXZ(yaxis)) * 2 + 1)
		padNameList.append(padName)
	return padNameList		 
if __name__ == '__main__':
	main()