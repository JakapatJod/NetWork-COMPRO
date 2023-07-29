import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

root = ET.Element('root')
ET.dump(root)

book = ET.Element('book')
root.append(book)
ET.dump(root)

name = ET.SubElement(book,'name')
name.text = 'Book1'
ET.dump(root)

temp = ET.SubElement(root , 'temp') 
ET.dump(root)

root.remove(temp) # <root><book><name>Book1</name></book></root>
ET.dump(root)
print(minidom.parseString(ET.tostring(root)).toprettyxml())
