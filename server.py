import socket
from _thread import *
import sys
from player import MOplayer
import pickle

port = 5555
host = socket.gethostname()
ip = socket.gethostbyname(host)
server = ip

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

game_data = [MOplayer('Player1'),MOplayer('Player2')]


def threaded_client(conn, player):
    conn.send(pickle.dumps(game_data[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2000))
            game_data[player] = data
            
            if not data:
                print("Client Disconnected")
                break
            else:
                if player == 1:
                    reply = game_data[0]
                else:
                    reply = game_data[1]
                    
            conn.sendall(pickle.dumps(reply))
        except:
            break
            
    print("Lost Connection")
    conn.close()

totalPlayers = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    start_new_thread(threaded_client, (conn, totalPlayers))
    totalPlayers += 1
print("Total players connected", totalPlayers)
