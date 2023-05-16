import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(parent_dir)

from proto.world_ups_pb2 import *
from proto.amazon_ups_pb2 import *

def getMessage (c):
    var_int_buff = []
    while True:
        buf = c.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    whole_message = c.recv(msg_len)
    return whole_message

def send_message (sock, message):
    print(message)
    msg = message.SerializeToString()
    _EncodeVarint(sock.send, len(msg), None)
    sock.send(msg)
    
def create_wh(id,x,y):
    wh = InitWarehouse()
    wh.id = id
    wh.x =x
    wh.y =y
    return wh

def create_item(description,quantity):
    item = Item()
    item.description = description
    item.quantity = quantity
    return item

def create_initship(id,wid,items,packageid,x,y,username):
    initShip = AmazonUPSInitShip()
    initShip.id = id
    initShip.wid = wid
    initShip.items.extend(items)
    initShip.packageid = packageid
    initShip.x = x
    initShip.y = y
    initShip.username = username
    return initShip
    

def create_startship(id,packageid):
    startShip = AmazonUPSStartShip()
    startShip.id = id
    startShip.packageid = packageid
    return startShip

def create_finishShip(id,packageid):
    finishShip = AmazonUPSFinishShip()
    finishShip.id = id
    finishShip.packageid = packageid



if __name__ == '__main__':
    print('Connecting to amazon...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (socket.gethostname(), 9708)
    sock.connect(server_address)
    print('Connected to amazon')
   
    whole_message = getMessage(sock)
    parsed_message = Connect()
    parsed_message.ParseFromString(whole_message)
    print('Recieved world_id from UPS')
    print(parsed_message)


    command = Connected()
    command.result = 1

  
    command.initwh.append(create_wh(1,1,1))
    command.initwh.append(create_wh(2,2,2))
    command.initwh.append(create_wh(3,3,3))
    command.initwh.append(create_wh(4,4,4))
    command.initwh.append(create_wh(5,5,5))
    command.initwh.append(create_wh(6,6,6))
    msg = command.SerializeToString()
    #_EncodeVarint(sock.send, len(msg), None)
    _EncodeVarint(sock.send, len(msg), None)
    sock.send(msg)
    
    #test initship

    commands = AmazonCommands()

    #sending 2 items (2 books and 5 pens) to delivery address ix (10 ,20)
    commands.initship.append (create_initship(1,1,[create_item("book",2),create_item("pen",5)],1,10,10,"haliunaa"))
    commands.initship.append (create_initship(2,2,[create_item("book",2),create_item("pen",5)],2,10,10,"haliunaa"))
    commands.initship.append (create_initship(3,3,[create_item("book",2),create_item("pen",5)],3,10,10,"haliunaa"))
    commands.initship.append (create_initship(4,4,[create_item("book",2),create_item("pen",5)],4,10,10,"haliunaa"))
    commands.initship.append (create_initship(5,5,[create_item("book",2),create_item("pen",5)],5,10,10,"haliunaa"))
    commands.initship.append (create_initship(6,6,[create_item("book",2),create_item("pen",5)],6,10,10,"haliunaa"))

    #sending 2 items (3 laptops and 3 keyboards) to delivery address ix (30 ,40)

    commands.initship.append (create_initship(10,1,[create_item("laptop",3),create_item("keyboard",3)],10,10,20,"Xinwen"))
    commands.initship.append (create_initship(11,1,[create_item("laptop",3),create_item("keyboard",3)],11,10,20,"Xinwen"))


    command_startship = AmazonCommands()

    command_startship.startship.append(create_startship(50,1))
    command_startship.startship.append(create_startship(51,2))
    command_startship.startship.append(create_startship(52,3))
    command_startship.startship.append(create_startship(53,1))


    """
    finishShip1 = AmazonUPSFinishShip()
    finishShip1.id = 5
    finishShip1.packageid = 17
    
    commands.finishship.append(finishShip1)
    """

    send_message(sock, commands)

    #receive ack

    whole_message = getMessage(sock)
    parsed_message = UPSCommands()
    parsed_message.ParseFromString(whole_message)
    print(parsed_message)

    send_message(sock, commands)
    whole_message = getMessage(sock)
    parsed_message = UPSCommands()
    parsed_message.ParseFromString(whole_message)
    print(parsed_message)

    send_message(sock, command_startship)
    whole_message = getMessage(sock)
    parsed_message = UPSCommands()
    parsed_message.ParseFromString(whole_message)
    print(parsed_message)

   




 

    print("Send warehouse and connected confirmation")
    sock.close()


  