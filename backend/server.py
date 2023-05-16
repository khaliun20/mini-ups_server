from db import *
import socket, threading, select, time
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
from amazonCommands import handle_amazon_commands
from dbAmazon import resend_amazon
from dbWorld import resend_world
from u_response import handle_world_responses
from u_commands import uquery_truck
from share import get_seq_num, send_message
import google.protobuf

def initDatabase():
    print(f"Using protobuf version: {google.protobuf.__version__}")
    #create_database()
    delete_tables()
    print("Delete tables")
    engine = create_tables()
    print("Build tables")
    #create 5 trucks 
    initialize_trucks(engine)
    initialize_branches(engine)
    return engine
    

def startListen() -> socket.socket:
    s = socket.socket()
    hostname = socket.gethostname()
    port = 9708
    s.bind((hostname, port))
    s.listen(100)
    return s

def connectWorld():
    print("Connecting to world")
    host = 'vcm-30715.vm.duke.edu'  # replace with the server address
    port = 12345  # replace with the correct port number
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connected to world")
    return sock


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
    msg = message.SerializeToString()
    _EncodeVarint(sock.send, len(msg), None)
    sock.send(msg)


def get_world_id(world_sock):
    whole_messsage = getMessage(world_sock)
    parsed_message = UConnected()
    parsed_message.ParseFromString(whole_messsage)
    #print(parsed_message)
    return parsed_message

def get_amazon_connected(amazon_sock):
    whole_messsage = getMessage(amazon_sock)
    parsed_message = Connected()
    parsed_message.ParseFromString(whole_messsage)
    #print(parsed_message)
    return parsed_message

def process_warehouse(amazon_connected_message, engine):
    for init_warehouse in amazon_connected_message.initwh:
        #print (init_warehouse)
        w_id = init_warehouse.id
        #print (w_id)
        w_x= init_warehouse.x
        w_y = init_warehouse.y
        store_in_database( w_id, w_x, w_y, engine)
        #print("stored in database")
    return



def buildWorld(world_sock, engine, s):
    #send to the World connection request
    print ('Sending UConnect to World')
    message = UConnect()
    trucks_str = get_truck_info(engine)
    trucks = pickle.loads(trucks_str)
    for truck in trucks:
        init_truck = UInitTruck()
        init_truck.id = truck.truck_id
        init_truck.x = int(truck.x)
        init_truck.y = int(truck.y)
        message.trucks.append(init_truck)
    message.isAmazon = 0
    #print(message)
    send_message (world_sock,message)


    #receive from World a worldid
    parsed_message = get_world_id(world_sock)
    while parsed_message.result != 'connected!':
        ####################################
        parsed_message = get_world_id(world_sock)
    print('Received world_id from world')
    #print(parsed_message)


 #******************** disconnection ******************
    #disconnection(world_sock)
    
    amazon_sock, addr = s.accept()

    #send to Amazon the worldid 
    world_id = Connect()
    world_id.worldid = parsed_message.worldid
    send_message(amazon_sock, world_id)
    print('Sent world_id to Amazon')
    
    #receive from Amazon warehouse and connection confirmation
    amazon_connected_message = None
    while not amazon_connected_message or amazon_connected_message.result != 1:
        amazon_connected_message = get_amazon_connected(amazon_sock)
        if amazon_connected_message.result == 1:
            process_warehouse(amazon_connected_message, engine)
    print ('Received Warehouse from Amazon')
    #print (amazon_connected_message)

     #******************** Set SIM Speed ******************

    set_sim_speed(world_sock)
    print('Changed the simspeed level of world')

    #*****************************************************
    print (' ')
    print (' ***** Ready to Receive Delivery Requests from Amazon *****')
    print (' ')


    redo_thread = threading.Thread(target = redo_worker, args =(world_sock, amazon_sock, engine))
    redo_thread.start()
    
    worker_thread = threading.Thread(target=worker, args=(world_sock, amazon_sock, engine))
    worker_thread.start()
   
    worker_thread.join()
    redo_thread.join()

    world_sock.close()
    amazon_sock.close()

    return 

def worker(world_sock, amazon_sock, engine):


   
    while amazon_sock.fileno() != -1 and world_sock.fileno() != -1:
        ready, _, _ = select.select([amazon_sock, world_sock], [], [], None)
        for sock in ready:
            if sock is amazon_sock:
                #print('Handling Messages Received from AMAZON')
                handle_amazon_commands(world_sock, amazon_sock, engine)
                
         
            elif sock is world_sock:
                #print('Handling Messages Received from WORLD')
                handle_world_responses(world_sock, amazon_sock, engine)
             
            else:
                pass  
           
def redo_worker(world_sock, amazon_sock, engine):
     while amazon_sock.fileno() != -1 and world_sock.fileno() != -1:
           resend_world(world_sock, engine) 
           #uquery_truck(engine, world_sock)

           time.sleep(5)
           

def set_sim_speed(world_sock): 
    message = UCommands()
    message.simspeed = 100
    send_message(world_sock, message)

 
            
def disconnection(world_sock):
    message = UCommands()
    message.disconnect = True
    send_message(world_sock, message)

