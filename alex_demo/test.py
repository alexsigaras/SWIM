from pyquery import PyQuery as pq
import urllib
mUrl = "http://www.nytimes.com/"
d = pq(url=mUrl, opener=lambda url: urllib.urlopen(url).read())
print d(".story").text()
    	