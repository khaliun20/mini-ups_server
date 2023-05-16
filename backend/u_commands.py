
from dbAmazon import*
from dbWorld import*


def send_ugopickup(truck_assigned, wid, seq_num, world_sock):
    #print ('Sending UGoPickUp command to world')
    gopickup = UGoPickup()
    gopickup.truckid = truck_assigned
    gopickup.whid = wid
    gopickup.seqnum = seq_num
    #print(gopickup)
    #message = UCommands(pickups = [gopickup])
    message = UCommands(pickups = [gopickup])
    #print(message)
    send_message(world_sock, message)
    return message

def send_ugodeliver (assigned_truck, package_to_deliver, seq_num, world_sock):
    godeliver  = UGoDeliver()
    godeliver.seqnum = seq_num
    godeliver.truckid = assigned_truck
    init_package = UDeliveryLocation()
    init_package.packageid = package_to_deliver.trucking_num
    init_package.x = package_to_deliver.x
    init_package.y = package_to_deliver.y
    godeliver.packages.append(init_package)
    message  = UCommands(deliveries = [godeliver])
    #print (message)
    send_message(world_sock, message)  
    #print ('Sending UGoDeliver command to world')
    return message

def send_world_acks(seqnums, world_sock):
    message = UCommands()
    message.acks.extend(seqnums)
    send_message(world_sock, message)

def uquery_truck(engine, world_sock):
    for x in range (1,6):
        seq_num = get_seq_num()
        query = UQuery()
        query.truckid = x
        query.seqnum = seq_num
        message  = UCommands(queries = [query])
        send_message(world_sock, message)
        add_to_world_seqnums(seq_num, message.SerializeToString(), engine)





    

