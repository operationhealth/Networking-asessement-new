import datetime
import time

x = datetime.datetime.now()
date = x.strftime("%a, %d %b %Y %H:%M:%S GMT")

"""Date: {}
Server: {}
Last-Modified: {}
Content-Length: {}
Content-Type: {}""".format(date)
