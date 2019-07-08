import httplib
import socket
import urllib2

class BindHttpConnection(httplib.HTTPConnection):
    def connect(self):
        self.sock = socket.socket()
        self.sock.bind((self.source_ip,0))
        if isinstance(self.timeout,float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        
def BindHttpConnectionFactory(source_ip):
    def _get(host, port=None, strict=None, timeout= 0):
        bhc=BindHttpConnection(host,port=port,strict=strict,timeout=timeout)
        bhc.source_ip=source_ip
        return bhc
    return _get

class BindHttpHandler(urllib2.HTTPHandler):
    def setLocalIP(self, local_ip):
        self.local_ip=local_ip
    def http_open(self,req):
        return self.do_open(BindHttpConnectionFactory(self.local_ip),req)
