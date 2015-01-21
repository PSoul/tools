import os
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sf = s.fileno()
s_fd = os.dup(s.fileno())
df = os.dup2(sf,0)
