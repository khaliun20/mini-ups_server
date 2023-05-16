import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(parent_dir)

from proto.world_ups_pb2 import *
from proto.amazon_ups_pb2 import *

if __name__ == '__main__':
    print('Connecting to server...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (socket.gethostname(), 9708)
    sock.connect(server_address)
    print('Connected to server')

    command = AmazonCommands()

    #sending 2 items (2 books and 5 pens) to delivery address ix (10 ,20)
    initShip1 = AmazonUPSInitShip()
    initShip1.id = 1
    initShip1.wid = 1

    item1 = Item()
    item1.description = "book"
    item1.quantity = 2
    item2 = Item()
    item2.description = "pen"
    item2.quantity = 5
    initShip1.items.extend([item1, item2])
    initShip1.packageid = 12
    initShip1.x = 10
    initShip1.y = 20

    command.initship.append (initShip1)


    #sending 2 items (3 laptops and 3 keyboards) to delivery address ix (30 ,40)

    initShip2 = AmazonUPSInitShip()
    initShip2.id = 2
    initShip2.wid = 1
    item1 = Item()
    item1.description = "laptop"
    item1.quantity = 3
    item2 = Item()
    item2.description = "keyboard"
    item2.quantity = 3
    initShip2.items.extend([item1, item2])
    initShip2.packageid = 13
    initShip2.x = 30
    initShip2.y = 40

    command.initship.append (initShip2)

    startShip1 = AmazonUPSStartShip()

    startShip1.id = 1
    startShip1.packageid = 14

    command.startship.append (startShip1)


    startShip2 = AmazonUPSStartShip()

    startShip2.id = 2
    startShip2.packageid = 15

    command.startship.append (startShip2)

    finishShip1 = AmazonUPSFinishShip()

    finishShip1.id = 1
    finishShip1.packageid = 16

    command.finishship.append (finishShip1)


    finishShip2 = AmazonUPSFinishShip()

    finishShip2.id = 1
    finishShip2.packageid = 17

    command.finishship.append (finishShip2)

    err1  = Err()
    err1.err= 'no error'
    err1. packageid = 18

    command.error.append(err1)

    command.acks.append(123)



    msg = command.SerializeToString()
    #_EncodeVarint(sock.send, len(msg), None)
    _EncodeVarint(sock.send, len(msg), None)
    sock.send(msg)

    sock.close()