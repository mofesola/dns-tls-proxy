import thread
import os
import socket
import logging
from tcp import Tcp
from udp import Udp
from common import Common
from multiprocessing import Process


def router(data, addr, sock, conn, protocol):
    """Route requests to handler based on protocol"""
    tcp, udp = Tcp(), Udp()
    if protocol == "tcp":
        tcp.handler(data, addr, sock, conn, protocol)
    elif protocol == "udp":
        udp.handler(data, addr, sock, conn, protocol)
    else:
        logging.error("Unknown Protocol")


def listen_tcp():
    """Listen on requested port for TCP DNS requests"""
    try:
        common = Common()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((common.proxy_host(), int(common.proxy_port())))
        sock.listen(2)
        logging.info('Listening for TCP requests')
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            protocol = "tcp"
            thread.start_new_thread(router, (data, addr, sock, conn, protocol))
    except Exception as e:
        logging.error(e)
        sock.close()


def listen_udp():
    """Listen on requested port for UDP DNS requests"""
    try:
        common = Common()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((common.proxy_host(), int(common.proxy_port())))
        logging.info('Listening for UDP requests')
        while True:
            data, addr = sock.recvfrom(1024)
            protocol = "udp"
            conn = None
            thread.start_new_thread(router, (data, addr, sock, conn, protocol))
    except Exception as e:
        logging.error(e)
        sock.close()


if __name__ == '__main__':
    LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
    logging.basicConfig(level=LOGLEVEL)
    Process(target=listen_tcp).start()
    Process(target=listen_udp).start()
