import _thread as thread
import os
import socket
import logging
from tcp import Tcp
from udp import Udp
from common import Common
from multiprocessing import Process


def listen_tcp():
    """Listen on requested port for TCP DNS requests"""
    try:
        common, tcp = Common(), Tcp()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((common.proxy_host(), int(common.proxy_port())))
        sock.listen(2)
        logging.info('Listening for TCP requests')
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            thread.start_new_thread(tcp.handler, (data, addr, sock, conn, "tcp"))
    except Exception as e:
        logging.error(e)
        sock.close()


def listen_udp():
    """Listen on requested port for UDP DNS requests"""
    try:
        common, udp = Common(), Udp()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((common.proxy_host(), int(common.proxy_port())))
        logging.info('Listening for UDP requests')
        while True:
            data, addr = sock.recvfrom(1024)
            thread.start_new_thread(udp.handler, (data, addr, sock, None, "udp"))
    except Exception as e:
        logging.error(e)
        sock.close()


if __name__ == '__main__':
    LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
    logging.basicConfig(level=LOGLEVEL)
    Process(target=listen_tcp).start()
    Process(target=listen_udp).start()
