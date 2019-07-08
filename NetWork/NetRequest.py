import urllib2
import cookielib
import BindHandler

class HttpReq():
    def __init__(self,local_ip="0.0.0.0"):
        self.cookie = cookielib.CookieJar()
        bindHandler=BindHandler.BindHttpHandler()
        bindHandler.setLocalIP(local_ip)
        self.opener = urllib2.build_opener(bindHandler,urllib2.HTTPCookieProcessor(self.cookie))
    
    def Request(self, url, headers="", data=""):
        req  =  urllib2.Request(url)
        for key in headers:
            req.add_header(key,headers[key])

        resp = self.opener.open(req)
        return resp

