import threading
from sqlalchemy import create_engine, Column, Integer, String, Enum, Boolean, Double
from sqlalchemy import not_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import pickle
from google.protobuf.internal.encoder import _EncodeVarint
from proto.amazon_ups_pb2 import *
from proto.world_ups_pb2 import *
from share import *
from sqlalchemy.dialects.postgresql import BYTEA
from math import sqrt

# use below to create database for the first time 
"""
def create_database():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="passw0rd"
        )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("CREATE DATABASE ups;")
    cur.close()
    conn.close()
"""

engine = create_engine('postgresql://postgres:passw0rd@localhost:5432/ups')
Base = declarative_base()
print(f"Opened: {engine}")
sock_lock = threading.Lock()

class Branches(Base):
    __tablename__ = 'branches'

    branch_id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    distance = Column(Integer, nullable=False)

class ShipLabel(Base):
    __tablename__ = 'shiplabel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tox = Column(Integer, nullable=False)
    toy = Column(Integer, nullable=False)
    fromx = Column(Integer, nullable=False)
    fromy = Column(Integer, nullable=False)
    weight = Column(Double, nullable=False)
    username = Column(String, nullable=False)

class Warehouse(Base):
    __tablename__ = 'warehouse'

    warehouse_id = Column(Integer, primary_key=True, autoincrement=True)
    wid = Column(Integer, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)


class Truck(Base):
    __tablename__ = 'truck'

    truck_id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    wid = Column(Integer, nullable = True)
    state = Column(Enum('idle', 'traveling', 'delivering', 'arrive_warehouse', 'loading', 
                    name='truck_state'), default='idle')
    world_given_state = Column(Enum('idle', 'traveling', 'delivering', 'arrive_warehouse', 'loading', 
                    name='truck_state'), default='idle')

class Packages(Base):
    __tablename__ = 'packages'

    packages_id = Column(Integer, primary_key=True, autoincrement=True)
    truck_id = Column(Integer, nullable = True)
    trucking_num = Column(Integer, nullable = False) #packageid
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    username = Column (String, nullable = False)
    warehouse_id = Column(Integer, nullable = False)
    #state = Column(Enum('delivering', 'preparing_for_pickup','delivered','arrive_warehouse', 'loading', 'loaded','ready_for_pickup',
                    #name='package_state'))
    state = Column(String, nullable = False)


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trucking_num = Column(Integer,nullable = False)
    description = Column(String, nullable = True)
    quantity = Column(Integer, nullable=True)

    #status = Column(Enum('open', 'canceled', 'executed',
                    #name='order_status'), default='open')
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable = False)
    password = Column(String, nullable = False)
    state = Column(String, nullable = False)


class WorldSeq(Base):
    __tablename__ = 'worldSeq'
    
    seq= Column(Integer, primary_key=True, nullable = False)
    message = Column(BYTEA, nullable = False)
    ack = Column(Boolean, default=False, nullable=False)

class WorldAck(Base):
    __tablename__ = 'worldAck'

    ack = Column(Integer, primary_key=True, nullable=False)

class AmazonSeq(Base):
    __tablename__ = 'amazonSeq'

    seq= Column(Integer, primary_key=True, nullable = False)
    message = Column(BYTEA, nullable = False)
    ack = Column(Boolean, default=False, nullable=False)

class AmazonAck(Base):
    __tablename__ = 'amazonAck'

    ack = Column(Integer, primary_key=True, nullable=False)


def create_tables():
    Base.metadata.create_all(bind=engine)
    return engine


def delete_tables():
    Base.metadata.reflect(bind=engine)
    Base.metadata.drop_all(bind=engine)


@contextmanager
def session_scope(engine):
    Session = sessionmaker(bind = engine)
    session = Session()
    try:
        yield session
        session.commit()
        #print('Commited')
    except:
        session.rollback()
        raise
    finally:
        session.close() 
        #print ("Closed")

def initialize_trucks(engine):
    with session_scope(engine) as session:
        for i in range(5):
            truck = Truck(x = 0, y = 0)
            session.add(truck)

def initialize_branches(engine):
    with session_scope(engine) as session:
        for i in range(5):
            branch = Branches(branch_id = i+1,  x = (i+1) * 10 , y = (i+1) * 10, distance=sqrt(((i+1)*10)*((i+1)*10) + ((i+1)*10)*((i+1)*10)))
            session.add(branch)
            #distance = Column(Integer, nullable=False)


def get_truck_info(engine):
    with session_scope(engine) as session:
        trucks = session.query(Truck).all()
        trucks_str = pickle.dumps(trucks)
    return trucks_str

def store_in_database( w_id, w_x, w_y, engine):
    with session_scope(engine) as session:
        new_wh = Warehouse(wid = w_id, x = w_x, y = w_y)
        session.add(new_wh)
     


def closeDatabase():
    engine.dispose()
    print(f"Closed: {engine}")