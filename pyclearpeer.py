#!/usr/bin/python3.8

import subprocess
import json
import random

getblockchaininfo = subprocess.run( [ "raven-cli", "getblockchaininfo" ], capture_output=True, text=True )
host = json.loads(getblockchaininfo.stdout)

if host["blocks"] != host["headers"]:
    print("Host is not synced, exiting")
    exit(1)

getpeerinfo = subprocess.run( [ "raven-cli", "getpeerinfo" ], capture_output=True, text=True )
peers = json.loads(getpeerinfo.stdout)

num_peers = len(peers)
print ( "Starting with " + str( num_peers ) + " peers")
for peer in peers:
    if host["blocks"] == peer["synced_blocks"]:
        if peer["inbound"] == True:
            if random.getrandbits(1):   # Roll the 50/50 dice
                subprocess.run( [ "raven-cli", "disconnectnode", peer["addr"] ] )
                print ( "Disconnected peer " + peer["addr"] )
                num_peers-=1
            else:
                print ( "Skipping lucky peer " + peer["addr"] )
        else:
            print ( "Skipping non-inbound peer " + peer["addr"] )
    else:
        print ( "Skipping unsynced peer " + peer["addr"] )
print ( "Ended with " + str( num_peers ) + " peers")

