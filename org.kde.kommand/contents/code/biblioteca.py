import sys
import os

try:
	from urllib.request import Request, urlopen  # Python 3
except ImportError:
	from urllib2 import Request, urlopen  # Python 2

class Biblioteca(object):
	h = {
	"Accept-Language": "en-US,en;q=0.5",
	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	"DNT": "1",
	"Connection": "keep-alive",
	"Upgrade-Insecure-Requests": "1",
	"Cache-Control": "max-age=0"
	}
	timeout = 1

	def __init__(self):
		pass

	def ajax(self, url):
		spt = url.split("/")
		req = Request(url)
		req.add_header("Host", spt[2])
		for key in self.h:
			req.add_header(key, self.h[key])
		#res = urlopen(req)
		res = urlopen(req, timeout=self.timeout)
		data = res.read()
		return res, data