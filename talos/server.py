#!/usr/bin/env python
import socket
import subprocess

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8002))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    # Run a viewer with an appropriate command line. Uncomment the mplayer
    # version if you would prefer to use mplayer instead of VLC
    cmdline = ['vlc', '--demux', 'h264', '-']
    print 'x'
    cmdline = ['mplayer', '-fps', '25', '-cache', '32', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    print 'y'
    while True:
#print 'data'
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        data = connection.read(5)
        if not data:
            break
        player.stdin.write(data)
except Exception, e:
    print e
finally:
    connection.close()
    server_socket.close()
    player.terminate()
