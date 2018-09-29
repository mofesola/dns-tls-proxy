import ssl
import thread
import os
import socket
import logging
from multiprocessing import Process

tls_host, tls_port = os.environ["TLS_DNS_HOST"], int(os.environ["TLS_DNS_PORT"])
proxy_host, proxy_port = os.environ["PROXY_HOST"], int(os.environ["PROXY_PORT"])


def tls_socket():
    """Create a socket object wrapped in an SSL context"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(100)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    tls_socket = ssl_context.wrap_socket(sock, server_hostname=tls_host)
    tls_socket.connect((tls_host, tls_port))
    return tls_socket


def get_tcp_from_udp(query):
    """Create TCP string from UDP query"""
    message = "\x00" + chr(len(query)) + query
    return message


def send_tcp_request(query):
    """Send request to secure DNS server from the TCP Socket"""
    sock = tls_socket()
    sock.sendall(query)
    data = sock.recv(1024)
    return data


def send_udp_request(query):
    """Send request to secure DNS server from the UDP Socket"""
    sock = tls_socket()
    tcp_query = get_tcp_from_udp(query)
    sock.send(tcp_query)
    data = sock.recv(1024)
    return data


def router(data, addr, sock, conn, protocol):
    """Route requests to handler based on protocol"""
    if protocol == "tcp":
        tcp_handler(data, addr, sock, conn, protocol)
    elif protocol == "udp":
        udp_handler(data, addr, sock, conn, protocol)
    else:
        logging.error("Unknown Protocol")


def tcp_handler(data, addr, sock, conn, protocol):
    response(send_tcp_request(data), addr, sock, conn, protocol)


def udp_handler(data, addr, sock, conn, protocol):
    response(send_udp_request(data), addr, sock, conn, protocol)


def response(response, addr, sock, conn, protocol):
    """Format response string returned from Secure DNS Server"""
    if response:
        rcode = response[:6].encode("hex")
        rcode = str(rcode)[11:]
        if (int(rcode, 16) == 1):
            logging.error("Wrong DNS Format")
        else:
            logging.info("Request successful")
            if protocol == "udp":
                response = response[2:]
                sock.sendto(response, addr)
            elif protocol == "tcp":
                conn.send(response)
    else:
        logging.error("Wrong DNS Format")


def listen_tcp():
    """Listen on requested port for TCP DNS requests"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((proxy_host, proxy_port))
        sock.listen(2)
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((proxy_host, proxy_port))
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
