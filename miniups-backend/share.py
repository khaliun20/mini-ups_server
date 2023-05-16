
import threading
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
from proto.amazon_ups_pb2 import UPSCommands
from proto.world_ups_pb2 import UCommands, UConnected



seq_lock = threading.Lock()
sock_lock = threading.Lock()

world_seq_num = 0

def get_seq_num():
    global world_seq_num
    with seq_lock:
        world_seq_num += 1
        seq_num = world_seq_num
    return seq_num

def getMessage (c):
    with sock_lock:
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
    with sock_lock:
        msg = message.SerializeToString()

        _EncodeVarint(sock.send, len(msg), None)
        sock.send(msg)
