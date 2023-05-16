import threading
from u_commands import * 
from upsCommands import *

def handle_world_responses(world_sock, amazon_sock, engine):
    #listen while amazon sock is open 
    print(' ')
    print('***** You got a Message from WORLD *****')
   
    whole_message = getMessage(world_sock)
    parsed_message = UResponses()
    parsed_message.ParseFromString(whole_message)
    #print(parsed_message)

    # Handle the parsed_message as needed
    if len(parsed_message.completions):
        #print('In thread 1: Completions message received from World')
        t1 = threading.Thread(target=handle_completions(engine, parsed_message.completions, world_sock, amazon_sock))
        t1.start()
        
    if len(parsed_message.delivered):
        #print('In thread 1: Delivered message received from Wrold')
        t2 = threading.Thread(target=handle_delivered(engine, parsed_message.delivered, world_sock, amazon_sock))
        t2.start()

    if len(parsed_message.truckstatus):
        #print('In thread 3: Truckstatus message received from Wrold')
        t3 = threading.Thread(target=handle_truckstatus(engine, parsed_message.truckstatus, world_sock))
        t3.start()
    
    if len(parsed_message.acks):
        #print('In thread 4: Ack message received from Wrold')
        t4 = threading.Thread(target=handle_acks(engine, parsed_message.acks))
        t4.start()
        

    if len(parsed_message.error):
        #print('In thread 5: Error message received from Wrold')
        t5 = threading.Thread(target=handle_error(engine,parsed_message.error))
        t5.start()
        
    if parsed_message.finished == 'true':
        world_sock.close()
        amazon_sock.close()


def handle_completions(engine, completions, world_sock, amazon_sock):
    print('-------------------------------')
    print("Received : UFinish from World. Message received : ")
    print(completions)
    local_world_acks =[]
    for completion in completions:
        #print ('Handling UFinished from World')
        #print(completion)
        processed =  check_if_acked_world(completion.seqnum,engine)
        if processed == True:
            continue
        ufinish_update_db(engine, completion.truckid, completion)
        #print('Updated Truck status to world given state: Arrive Warehouse - Does not upadte package')
        local_world_acks.append(completion.seqnum)

        if completion.status == "ARRIVE WAREHOUSE":
           
            packages_ready_pickle = get_ready_packages(engine, completion.truckid)
            #print('Searched for all packages with state - Ready for pickup')

            #print ('222222222222222')

            packages_ready = pickle.loads(packages_ready_pickle)
            for package_ready in packages_ready: 
                #print ('3333333333')
                seq_num = get_seq_num()
                start_load = UPSAmazonStartShip()
                start_load.packageid = package_ready.trucking_num
                start_load.id = seq_num
                message = UPSCommands(startship = [start_load])
                print('-------------------------------')
                print("Sent : UPSAmazonStartShip to Amazon. Message sent : ")
                print(message)
                send_message(amazon_sock, message)
                #and save each message to global seqnum(saved message needs to be UPSCommand)
                add_to_amazon_seqnums(seq_num, message.SerializeToString(),engine)
        
        if completion.status == "IDLE":
            update_truck_idle(engine, completion.truckid)

    send_world_acks(local_world_acks, world_sock)
    add_to_acked_world(local_world_acks,engine)


def handle_delivered(engine, delivereds, world_sock, amazon_sock):
    print('-------------------------------')
    print("Received : UDeliveryMade from World. Message received : ")
    print(delivereds)
    local_world_acks =[]
    for delivered in delivereds: 
        #print ('Handling UDeliveryMade from World')
        processed =  check_if_acked_world(delivered.seqnum,engine)
        if processed == True:
            continue
        udeliverymade_update_db(engine, delivered.packageid)
        #print('Updated truck and package status to Delivering')
        local_world_acks.append(delivered.seqnum)
        
        #tell amazon package is delivered
        seq_num = get_seq_num()
        message = tell_amazon_delivered(seq_num, delivered.packageid, amazon_sock)
        print('-------------------------------')
        print("Sent : UPSAmazonFinishship to Amazon. Message sent : ")
        print(message)

        add_to_amazon_seqnums(seq_num, message.SerializeToString(),engine)

    send_world_acks(local_world_acks, world_sock)
    add_to_acked_world(local_world_acks,engine)

def handle_truckstatus(engine, truckstatuses, world_sock):
    print('-------------------------------')
    print("Received : UTruckStatus from World. Message received: ")
    print(truckstatuses)
    
    local_world_acks =[]
    for truckstatus in truckstatuses:
        processed =  check_if_acked_world(truckstatus.seqnum,engine)
        if processed == True:
            continue
        truckstatus_update_db(engine,truckstatus.truckid,truckstatus)
        local_world_acks.append(truckstatus.seqnum)

    send_world_acks(local_world_acks, world_sock)
    add_to_acked_world(local_world_acks,engine)


def handle_acks(engine, acked):
    print('-------------------------------')
    print(f"Handling ACKS from World :  {acked}")
    for ack in acked:
        mark_ack_world(ack,engine)
    


def handle_error(engine,error,world_sock):
    print('-------------------------------')
    print('Handling Errors from World : ')
    print(error)
    local_acks = []
    for err in error:
        local_acks.append (err.id)
        processed = check_if_acked_world(err.id,engine)
        if processed == True:
                continue
        seq_num = get_seq_num()
        send_world_message(engine,err.originseqnum,world_sock,seq_num)
    send_world_acks(local_acks, world_sock)
    add_to_acked_world(local_acks,engine)


def send_world_message(engine,originseqnum,world_sock,seq):
        parsed_message = find_world_error_message(engine,originseqnum)
        if len(parsed_message.initship):
            for initship in parsed_message.initship:
                initship.id = seq
                message = UPSCommands(initship = [initship])
                send_message(world_sock, message)
                add_to_world_seqnums(seq, message,engine)
        
        if len(parsed_message.startship):
            for startship in parsed_message.startship:
                startship.id = seq
                message = UPSCommands(startship = [startship])
                send_message(world_sock, message)
                add_to_world_seqnums(seq, message.SerializeToString(),engine)
                
        if len(parsed_message.finishship):
            for finishship in parsed_message.finishship:
                finishship.id = seq
                message = UPSCommands(finishship = [finishship])
                send_message(world_sock, message)
                add_to_world_seqnums(seq, message.SerializeToString(),engine)



        
    