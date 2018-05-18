#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind(("0.0.0.0", 1234))
    while True:
        print(s.recvfrom(65535))
