import xml.etree.ElementTree as ET
import sys
tree = ET.parse(sys.argv[1])
root = tree.getroot()

line1_x = 7
line1_y = 4
line4_x = 24.78
line4_y = 4
line2_x = 13.99
line2_y = 8.66
line3_x = 13.99 + 3.81
line3_y = 8.66
for wire in root.iter('elements'):
	for i in range(0, 64, +1):
		child = ET.Element('element')
		child.set('name','LL' + str(i))
		child.set('library',"SparkFun-Connectors")
		child.set('package',"1X01_SMD_3.0X1.0MM_NO_SILK")
		child.set('value',"")
		child.set('x',str(line1_x))
		child.set('y',str(line1_y + i * 2.54))
		wire.append(child)
	for i in range(0, 64, +1):
		child = ET.Element('element')
		child.set('name','RL' + str(i))
		child.set('library',"SparkFun-Connectors")
		child.set('package',"1X01_SMD_3.0X1.0MM_NO_SILK")
		child.set('value',"")
		child.set('x',str(line4_x))
		child.set('y',str(line4_y + i * 2.54))
		wire.append(child)	
	for i in range(0, 24, +2):
		child = ET.Element('element')
		child.set('name','RS' + str(i))
		child.set('library',"SparkFun-Connectors")
		child.set('package',"1X01_SMD_3.0X1.0MM_NO_SILK")
		child.set('value',"")
		child.set('x',str(line2_x))
		child.set('y',str(line2_y + (i/2) * 13.33))
		wire.append(child)
		child = ET.Element('element')
		child.set('name','RS' + str(i+1))
		child.set('library',"SparkFun-Connectors")
		child.set('package',"1X01_SMD_3.0X1.0MM_NO_SILK")
		child.set('value',"")
		child.set('x',str(line2_x))
		child.set('y',str(line2_y + (i/2) * 13.33 + 2.54))
		wire.append(child)
	for i in range(0, 24, +2):
		child = ET.Element('element')
		child.set('name','LS' + str(i))
		child.set('library',"SparkFun-Connectors")
		child.set('package',"1X01_SMD_3.0X1.0MM_NO_SILK")
		child.set('value',"")
		child.set('x',str(line3_x))
		child.set('y',str(line3_y + (i/2) * 13.33))
		wire.append(child)
		child = ET.Element('element')
		child.set('name','LS' + str(i+1))
		child.set('library',"SparkFun-Connectors")
		child.set('package',"1X01_SMD_3.0X1.0MM_NO_SILK")
		child.set('value',"")
		child.set('x',str(line3_x))
		child.set('y',str(line3_y + (i/2) * 13.33 + 2.54))
		wire.append(child)				
		
tree.write('64_breadboard.brd')
