###
# This script will convert a list of IP addresses into Palo Alto
# set commands for bulk import into a firewall. The IP addresses
# are expected to be separated by new lines, not commas or spaces.
# The IP addresses should be individual hosts only, as the script
# is not aware of netmasks at this time. Future updates may
# address that functionality.
###

import ntpath

# Input the file in full directory format, IE: C:\temp\file.txt
print('Input the file location in full directory format, IE: C:\\temp\\file.txt')
fileLocation = input('Location of ASA Object Configuration: ')
fileDir = ntpath.dirname(fileLocation)
name = input('Provide a prefix/tag for the created objects: ')

# Read the document into a List
try:
    docIPList = open(fileLocation, 'r')
except:
    print('Error opening file at directory '+fileLocation+'. Please check the ntpath and run again.')
    exit()

try:
    row = [line.split(' ') for line in docIPList.readlines()]
    docIPList.close()
except:
    print('Error performing readlines operation on file.')
    exit()

# Create a list of addresses from the text file
objects = []
for items in row:
    objects.append(items)

# Convert objects list into Palo Alto set command syntax
setAddress = []
for items in objects:
    addr = items[0].strip('\n')
    setAddress.append('set address '+name+'-'+addr+' tag '+name+' ip-netmask '+addr+'\n')

# Save set commands to output file
try:
    with open(fileDir+'\\'+name+'-palo.txt', 'w+') as file_handler:
        file_handler.write('set tag '+name+'\n')
        file_handler.write('set address-group '+name+' dynamic filter '+name+'\n')
        for item in setAddress:
            file_handler.write('{}'.format(item))
except:
    print('Error writing output to file. Check file directory '+fileDir+' for read/write permissions.')
    exit()