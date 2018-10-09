from common import Common


class Udp:

    def send_request(self, query):
        """Send request to secure DNS server from the UDP Socket"""
        common = Common()
        sock = common.tls_socket()
        tcp_query = common.get_tcp_from_udp(query).encode('cp1252')
        sock.send(tcp_query)
        data = sock.recv(1024)
        return data

    def handler(self, data, addr, sock, conn, protocol):
        common = Common()
        common.response(self.send_request(data), addr, sock, conn, protocol)
