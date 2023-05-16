from db import *


def get_available_truck(engine, package_whid):
    with session_scope(engine) as session:
        # get tuples of all the trucks where the status is not delivering or idle
        all_available_trucks = session.query(Truck).filter((Truck.state == 'idle') | (Truck.state == 'delivering') | (Truck.state == 'traveling')).all()
        #print(all_available_trucks)
        if len(all_available_trucks) > 0:
            truck_id = None
            for available_trucks in all_available_trucks:
                if available_trucks.state== "traveling" and available_trucks.wid == package_whid:
                    truck_id = available_trucks.truck_id
                    return truck_id
            truck_id= all_available_trucks[0].truck_id
            return truck_id
        else:
            return None
        
        
        
def store_initship_db(engine, initship, truck_assigned):
    with session_scope(engine) as session:
        booked_truck = session.query(Truck).filter_by(truck_id = truck_assigned).first()
        booked_truck.state = 'traveling'
        booked_truck.wid = initship.wid
       
        new_package = Packages(
            truck_id = truck_assigned,
            trucking_num = initship.packageid,
            x = initship.x,
            y = initship.y,
            username = str(initship.username),
            warehouse_id = initship.wid,
            state = 'preparing_for_pickup'
        )
        #print(booked_truck, new_package)
        session.add(booked_truck)
        session.add(new_package)
        #print(initship)
        #print(initship.items)
        for item in initship.items:
            new_item = Items(trucking_num= initship.packageid , description= item.description, quantity = item.quantity)
            session.add(new_item)
            
            
def startship_update_db(engine, package_id):
    with session_scope(engine) as session:
        package = session.query(Packages).filter(Packages.trucking_num == package_id and Packages.state == 'preparing_for_pickup').first()
        package.state = 'ready_for_pickup'
        # truckid = package.truck_id
        # truck = session.query(Truck).filter_by(truck_id = truckid).first()
        # truck.state = 'loading'
        # session.add(truck)
        session.add(package)

def check_ready_forStartship(engine, package_id,amazon_sock):
     with session_scope(engine) as session:
         package = session.query(Packages).filter(Packages.trucking_num == package_id).first()
         truckid = package.truck_id
         truck = session.query(Truck).filter_by(truck_id = truckid).first()
         if truck.state == "arrive_warehouse":
             #send shartship
            seq_num = get_seq_num()
            start_load = UPSAmazonStartShip()
            start_load.packageid = package.trucking_num
            start_load.id = seq_num
            message = UPSCommands(startship = [start_load])
            #print("check_ready_forStartship")
            print('-------------------------------')
            print(f"Sent : UPSAmazonStartship to Amazon. Message sent : {message}")
            send_message(amazon_sock, message)
                #and save each message to global seqnum(saved message needs to be UPSCommand)
            add_to_amazon_seqnums(seq_num, message.SerializeToString(),engine)


def get_package_to_deliver(engine, package_id):
    with session_scope(engine) as session:
        package = session.query(Packages).filter_by(trucking_num = package_id).first()
        package_str = pickle.dumps(package)
    return package_str



def check_if_acked_amazon(acked, engine):
    with session_scope(engine) as session:
        query = session.query(AmazonAck).filter_by(ack = acked).first()
        if query is None:
            return False
        else:
            return True  
        


def add_to_acked_amazon(local_acks, engine):
    with session_scope(engine) as session:
        for local_ack in local_acks:
            new_ack = AmazonAck(ack =local_ack)
            session.add(new_ack)



def mark_ack_amazon(acked, engine):
    #go to a table where all the messages we sent to Amazon are saved
    with session_scope(engine) as session:
      
        query = session.query(AmazonSeq).filter_by(seq=acked).first()
        
        if not query:
            #received unexisting seqnum, handle error
            return
        else:
            query.ack = True
            session.add(query)

def add_to_amazon_seqnums(seq_num, command, engine):
    # add to the table where messages sent to Amazon
    with session_scope(engine) as session:
        new_seq = AmazonSeq(seq = seq_num, message = command)
        session.add(new_seq)
        
        
        
        

def resend_amazon(amazon_sock, engine):
    with session_scope(engine) as session:
        queries = session.query(AmazonSeq).filter_by(ack=False).all()
        if queries is None:
            print('All messages have been Ack-ed by Amazon')
            return
        else:
            for query in queries:
                parsed_message = UPSCommands()
                parsed_message.ParseFromString(query.message)
                send_message(amazon_sock, parsed_message)
                
def check_ugopickup_sent(engine, truck_assigned, warehouse, packageid):
    with session_scope(engine) as session:
        queries = session.query(Packages).filter(not_(Packages.trucking_num == packageid), (Packages.state == 'ready_for_pickup') | (Packages.state == 'preparing_for_pickup'), Packages.warehouse_id == warehouse, Packages.truck_id == truck_assigned).all()
        if len(queries) > 0:
            return True
        else:
            return False



def find_amazon_error_message(engine,seq):
    with session_scope(engine) as session:
        query = session.query(AmazonSeq).filter_by(seq=seq).first().message
        parsed_message = UPSCommands()
        parsed_message.ParseFromString(query.message)
    return parsed_message
