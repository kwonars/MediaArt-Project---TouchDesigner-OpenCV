# me - this DAT
# 
# dat - the DAT that received the data
# rowIndex - the row number the data was placed into
# message - an ascii representation of the data
#			Unprintable characters and unicode characters will
#			not be preserved. Use the 'bytes' parameter to get
#			the raw bytes that were sent.
# bytes - a byte array of the data received
# peer - a Peer object describing the originating data
#   peer.close() 	#close the connection
#	peer.owner	#the operator to whom the peer belongs
#	peer.address	#network address associated with the peer
#	peer.port		#network port associated with the peer

# For TCP/IP Touch Designer Module

def messageToCoords(message):
	coordsOut = []
	element =''
	for i in message:
		if i != '/':
			element = element + i
		else:
			coordsOut.append(float(element))
			element = ''
	return coordsOut


def onConnect(dat, peer):
	print("TouchDesigner is connected!")
	return

def onReceive(dat, rowIndex, message, bytes, peer):
	# print("Data is received!")
	coordsOut = messageToCoords(message)
	op('table1').clear()
	for i in coordsOut:
		op('table1').appendCol(i)

	return

def onClose(dat, peer):
	print("onClose is called!")
	return

	