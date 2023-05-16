from dbAmazon import*



def send_amazon_acks(seqnums, amazon_sock):
    message = UPSCommands()
    message.acks.extend(seqnums)
    send_message(amazon_sock, message)

#UPSAmazonFinishship
def tell_amazon_delivered(seq_num, packageid, amazon_sock):
    finished = UPSAmazonFinishShip()
    finished.id = seq_num
    finished.packageid = packageid
    message = UPSCommands(finishship = [finished])
    send_message(amazon_sock, message)
    return message

#UPSAmazonInitShip
def tell_amazon_initship(truck_assigned, packageid, amazon_sock, engine):
    seq_num = get_seq_num()
    init = UPSAmazonInitShip()
    init.id = seq_num
    init.packageid = packageid
    init.truckid = truck_assigned
    message = UPSCommands(initship = [init])
    send_message(amazon_sock, message)
    print('-------------------------------')
    print("Sent : UPSAmazonInitShip to Amazon. Message sent : ")
    print(message)
    add_to_amazon_seqnums(seq_num, message.SerializeToString(),engine)
    
def tell_amazon_error(err, amazon_sock, engine):
    seq_num = get_seq_num()
    err.seqnum = seq_num
    message = UPSCommands(Err = [err])
    send_message(amazon_sock, message)
    add_to_amazon_seqnums(seq_num, message.SerializeToString(),engine)



def send_amazon_message(engine,originseqnum,amazon_sock,seq):
        parsed_message = find_amazon_error_message(engine,originseqnum)
        if len(parsed_message.initship):
            for initship in parsed_message.initship:
                initship.id = seq
                message = UPSCommands(initship = [initship])
                send_message(amazon_sock, message)
                add_to_amazon_seqnums(seq, message.SerializeToString(),engine)
        
        if len(parsed_message.startship):
            for startship in parsed_message.startship:
                startship.id = seq
                message = UPSCommands(startship = [startship])
                send_message(amazon_sock, message)
                add_to_amazon_seqnums(seq, message.SerializeToString(),engine)
                
        if len(parsed_message.finishship):
            for finishship in parsed_message.finishship:
                finishship.id = seq
                message = UPSCommands(finishship = [finishship])
                send_message(amazon_sock, message)
                add_to_amazon_seqnums(seq, message.SerializeToString(),engine)
