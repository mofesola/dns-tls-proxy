from common import Common


class Tcp:

    def send_request(self, query):
        """Send request to secure DNS server from the TCP Socket"""
        common = Common()
        sock = common.tls_socket()
        sock.sendall(query)
        data = sock.recv(1024)
        return data

    def handler(self, data, addr, sock, conn, protocol):
        common = Common()
        common.response(self.send_request(data), addr, sock, conn, protocol)
