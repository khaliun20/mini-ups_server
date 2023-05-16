from db import *
RESET = 0
def update_db(engine, package_id):
    with session_scope(engine) as session:
        package = session.query(Packages).filter(Packages.trucking_num == package_id and Packages.state == "ready_for_pickup").first()
        package.state = 'delivering'
        assigned_truck= package.truck_id
        #temp_x and y are temp variables used to pass data to Truck table

        #temp_x = package.x
        #temp_y = package.y
       
        truck = session.query(Truck).filter(Truck.truck_id == assigned_truck).first()
        truck.state = 'arrive_warehouse'
        # maybe not need to update truck's x and y  after UFinished?
        #truck.x = temp_x
        #truck.y = temp_y
        session.add(package)
        session.add(truck)
        
    return assigned_truck



def ufinish_update_db(engine, truckid, completion): 
    #print("ufinish_update_db")
    with session_scope(engine) as session:
        if completion.status.lower() == 'arrive warehouse':
            truck = session.query(Truck).filter_by(truck_id = truckid).first()
            truck.state = 'arrive_warehouse'
            truck.world_given_state = 'arrive_warehouse'
            truck.x = completion.x
            truck.y = completion.y
            session.add(truck)
        else:
            truck = session.query(Truck).filter_by(truck_id = truckid).first()
            truck.state = 'idle'
            truck.world_given_state = 'idle'
            truck.x = completion.x
            truck.y = completion.y
            session.add(truck)

    

def get_ready_packages(engine, truckid):
    #print("get_ready_packages")
    with session_scope(engine) as session:
        desired_states = ['ready_for_pickup']
        packages_query = session.query(Packages).filter_by(truck_id=truckid).filter(or_(Packages.state.in_(desired_states)))
        packages = packages_query.all()
        packages_str = pickle.dumps(packages)
        # for package in packages:
        #     package.state = 'arrive warehouse'
        #     session.add(package)
    return packages_str



def udeliverymade_update_db(engine, packageid):
    #print("udeliverymade_update_db")

    with session_scope(engine) as session:
        package = session.query(Packages).filter_by(trucking_num = packageid).first()
        package.state = 'delivered'
        tempx = package.x
        tempy = package.y
        truckid = package.truck_id
        truck = session.query(Truck).filter_by(truck_id = truckid).first()
        # reset truck
        if truck.state == 'idle':
            truck.state = 'idle'
            truck.x = RESET
            truck.y = RESET
            truck.wid = None
        else:
            truck.state = 'delivering'
            truck.x = tempx
            truck.y = tempy
        session.add(package)
        session.add(truck)


def truckstatus_update_db(engine,truckid, truckstatus):
    #print("truckstatus_update_db")

    with session_scope(engine) as session:
        truck = session.query(Truck).filter_by(truck_id = truckid).first()
        truck.world_given_state = truckstatus.status.lower()
        #should we also update the truck.state? or leave it as is?
        truck.x = truckstatus.x
        truck.y = truckstatus.y
        session.add(truck)


def check_if_acked_world(acked, engine):
    #print("check_if_acked_world")
    with session_scope(engine) as session:
        query = session.query(WorldAck).filter_by(ack = acked).first()
        if query is None:
            return False
        else:
            return True   
        
        
        
def add_to_acked_world(local_world_acks, engine):
    with session_scope(engine) as session:
        for local_world_ack in local_world_acks:
            new_ack = WorldAck(ack=local_world_ack)
            session.add(new_ack)
            
            
            

def mark_ack_world(acked, engine):
    #go to table where all the messages we sent to the World are saved
    with session_scope(engine) as session:
       
        query = session.query(WorldSeq).filter_by(seq=acked).first()
        
        if not query:
            #received unexisting seqnum, handle error
            return
        else:
            query.ack = True
            session.add(query)
            
            
def add_to_world_seqnums(seq_num, command, engine):
    # add to the table where messages sent to Amazon
    with session_scope(engine) as session:
        new_seq = WorldSeq(seq = seq_num, message = command)
        session.add(new_seq)
        
        
        
        
def resend_world(world_sock, engine):
    with session_scope(engine) as session:
        queries = session.query(WorldSeq).filter_by(ack=False).all()
        if queries is None:
            return
        else:
            for query in queries:
                #print(query.message)
                parsed_message = UCommands()
                parsed_message.ParseFromString(query.message)
                print('-------------------------------')
                print("Resending lost/delayed message to World. Message: ")
                print(parsed_message)
                send_message(world_sock, parsed_message)
"""
def send_message (sock, message):
    with sock_lock:
        msg = message.SerializeToString()

        _EncodeVarint(sock.send, len(msg), None)
        sock.send(msg)
"""
def find_world_error_message(engine,seq):
    with session_scope(engine) as session:
        query = session.query(WorldSeq).filter_by(seq=seq).first().message
        parsed_message = UResponses()
        parsed_message.ParseFromString(query.message)
    return parsed_message

def update_truck_idle(engine, truckid):
    with session_scope(engine) as session:
        truck = session.query(Truck).filter_by(truck_id = truckid).first()
        truck.status = 'idle'
        session.add(truck)
        
