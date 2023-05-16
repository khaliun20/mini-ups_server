from dbAmazon import*
from dbWorld import*
import threading
from u_commands import send_ugopickup,send_ugodeliver
from upsCommands import * 


def handle_amazon_commands(world_sock, amazon_sock, engine):
    print(' ')
    print('***** You got a Message from AMAZON *****')
    
    #listen while amazon sock is open 

    whole_message = getMessage(amazon_sock)
    parsed_message = AmazonCommands()
    parsed_message.ParseFromString(whole_message)
    #print(parsed_message)
    # Handle the parsed_message as needed
    if len(parsed_message.initship):
        #print('In thread 1: Initship received from Amazon')
        t1 = threading.Thread(target=handle_initship(engine, parsed_message.initship, world_sock, amazon_sock))
        t1.start()
    
    
    if len(parsed_message.startship):
        #print('In thread 2: Startship received from Amazon')
        t2 = threading.Thread(target=handle_startship(engine, parsed_message.startship, world_sock, amazon_sock))
        t2.start()
        
    if len(parsed_message.finishship):
        #print('In thread 3: Finishship received from Amazon')
        t3 = threading.Thread(target=handle_finishship(engine, parsed_message.finishship, world_sock, amazon_sock))
        t3.start()
        
    if len(parsed_message.acks):
        #print('In thread 4: Acks received from Amazon')
        t4 = threading.Thread(target=handle_acks(engine, parsed_message.acks))
        t4.start()
        

    if len(parsed_message.error):
        #print('In thread 5: Errors received from Amazon')
        t5 = threading.Thread(target=handle_error(engine,parsed_message.error))
        t5.start()
    




def handle_initship(engine, initships, world_sock, amazon_sock):
    print('-------------------------------')
    print("Received : AmazonUPSInitship from Amazon. Message received : ")
    print (initships)
   
    local_acks= []


    for initship in initships: 
        
        try:
            #print (initship)
            # there is no truck can be assigned at this time. Amazon will have to resend this request
            processed = check_if_acked_amazon(initship.id,engine)
            if processed == True:
                    continue
            #chekcing if have any available trucks
            truck_assigned = get_available_truck(engine, initship.wid)
            if truck_assigned is None:
                continue

            #if reached here, it means that truck has been assigned to the package
            # and that initship has not been processed before (aka not a resend)

            #save into database
            store_initship_db(engine, initship, truck_assigned)
    
            #print('Saved initship to database. Truck State changed to Traveling. Package state changed to Preparing for Pickup  ')

            #Todo: DONE our UPS end need to handle this instead of world
            #print(truck_assigned,initship.wid,initship.packageid)
            ugopickup_sent = check_ugopickup_sent(engine, truck_assigned, initship.wid, initship.packageid)
            #print(f"Have we assigned truck? False if we need to send UGoPickup: {ugopickup_sent}")
        

            message = None
            if ugopickup_sent == False: 
                seq_num = get_seq_num()
                message = send_ugopickup(truck_assigned, initship.wid, seq_num, world_sock)
                print('-------------------------------')
                print("Sent : UGoPickup to World. Message sent : ")
                print (message)
                add_to_world_seqnums(seq_num, message.SerializeToString(),engine)
                #add_to_world_seqnums(seq_num, message,engine)
            else:
                pass
            #print (message)
            #save seqnums (seqnum, (message, boolean))
            
            #PRINT STATEMENT IS DONE IN METHOD
            tell_amazon_initship(truck_assigned, initship.packageid, amazon_sock, engine)
            #save all the seqnums of amazon requests
            local_acks.append (initship.id)
        except Exception as e:
            
            tell_amazon_error(create_error(str(e),initship.id),amazon_sock, engine)
            
    send_amazon_acks(local_acks, amazon_sock)
    add_to_acked_amazon(local_acks,engine)
    #print(global_acks)
    #print(global_seqnums)

#amazon saying package is ready for pickup
def handle_startship(engine, startships, world_sock, amazon_sock): 
    print('-------------------------------')
    print("Received : AmazonUPSStartship from Amazon. Message received : ")
    print (startships)
    # ready for pick up 
    # we recieve this from Amazon 
    local_acks = []
    for startship in startships:
        try:
            #print("in handle_startship")
            #check if it has been already takesn caren of
            processed = check_if_acked_amazon(startship.id,engine)
            if processed == True:
                    continue
            startship_update_db(engine, startship.packageid)
            #print ("Change Package Status from preparing for pickup to ready for pickup")
            #print('1. At the end of try block')
            local_acks.append (startship.id)
            check_ready_forStartship(engine,startship.packageid,amazon_sock)
        except Exception as e:
            #print ('2. Exception thrown in startship')
            tell_amazon_error(create_error(str(e),startship.id),amazon_sock, engine)
    send_amazon_acks(local_acks, amazon_sock)

    add_to_acked_amazon(local_acks,engine)

 


#finished loading
def handle_finishship(engine, finishships, world_sock, amazon_sock):
    print('-------------------------------')
    print("Received : AmazonUPSFinishship from Amazon. Message received : ")
    print (finishships)
    local_acks = []
    #handle each package individually
    for finishship in finishships:
        #check if hanfled
        try:

            processed = check_if_acked_amazon(finishship.id,engine)
            if processed == True:
                    continue
    
            #update the db
            assigned_truck = update_db(engine, finishship.packageid)
            #print('Searched for trucks in loading state and uptade Truck to Arrive Wareouse and Package to Arrive Warehouse')
            package_to_deliver_pickle = get_package_to_deliver(engine,finishship.packageid)
            package_to_deliver = pickle.loads(package_to_deliver_pickle)
            local_acks.append (finishship.id)



        #todo:uquey the way (need to make sure truck get all package loaded)
        #(maybe the world will handle this)


            seq_num = get_seq_num()
            #send UGoDeliver in UCommand to World
            message = send_ugodeliver(assigned_truck, package_to_deliver, seq_num, world_sock)
            print('-------------------------------')
            print("Sent : UGoDeliver to World. Message sent : ")
            print (message)
            #save seqnums (seqnum, (message, boolean))
            
            
            add_to_world_seqnums(seq_num, message.SerializeToString(),engine)
            #add_to_world_seqnums(seq_num, message,engine)

            #Is this when we send back UPSAmazonFinishShip?
        except Exception as e:
            tell_amazon_error(create_error(str(e),finishship.id),amazon_sock, engine)
    send_amazon_acks(local_acks, amazon_sock)
    add_to_acked_amazon(local_acks,engine)

#go back to the dictionary and mark them all acked
def handle_acks(engine, acked):
     print('-------------------------------')
     print(f"Handling ACKS from Amazon : {acked}")
     for ack in acked:
        mark_ack_amazon(ack,engine)
     #print("finish handle_acks")


def handle_error(engine,error,amazon_sock):
    print('-------------------------------')
    print('Handling Errors from Amazon')
    local_acks = []
    for err in error:
        try:
            local_acks.append (err.id)
            processed = check_if_acked_amazon(err.id,engine)
            if processed == True:
                    continue
            seq_num = get_seq_num()
            #Todo:write code for this
            #send_error_message(engine,err.originseqnum,amazon_sock,seq_num)
        except Exception as e:
            tell_amazon_error(create_error(str(e),err.id),amazon_sock, engine)  
    send_amazon_acks(local_acks, amazon_sock)
    add_to_acked_amazon(local_acks,engine)
    
    
def create_error(err,originseqnum):
    err = Err()
    err.err = err
    err.originseqnum=originseqnum
    return err

