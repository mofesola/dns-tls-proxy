import ssl
import os
import socket
import logging


class Common:

    def tls_socket(self):
        """Create a socket object wrapped in an SSL context"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(100)
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        tls_socket = ssl_context.wrap_socket(sock, server_hostname=self.tls_host())
        tls_socket.connect((self.tls_host(), int(self.tls_port())))
        return tls_socket

    def get_tcp_from_udp(self, query):
        """Create TCP string from UDP query"""
        message = '\x00' + chr(len(query)) + query.decode('cp1252')
        return message

    def response(self, response, addr, sock, conn, protocol):
        """Format response string returned from Secure DNS Server"""
        if response:
            rcode = response[:6].hex()
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

    def tls_host(self):
        return os.environ["TLS_DNS_HOST"]

    def tls_port(self):
        return int(os.environ["TLS_DNS_PORT"])

    def proxy_host(self):
        return os.environ["PROXY_HOST"]

    def proxy_port(self):
        return os.environ["PROXY_PORT"]
