from server import initDatabase, startListen, connectWorld, buildWorld
from db import closeDatabase

def main():
    # build database connection, create tables and initialize trucks
    engine = initDatabase()

    # connect to the world
    world_sock = connectWorld()

    # start listening for Amazon connection 
    s = startListen()

    # connect with Amazon on amazon_sock
    

    #create world, send truck info, send Amazon word id
    buildWorld(world_sock, engine, s)
    #worker(world_sock, amazon_sock, engine)


    # close the database connection
    closeDatabase()

    return

if __name__ == "__main__":
    main()