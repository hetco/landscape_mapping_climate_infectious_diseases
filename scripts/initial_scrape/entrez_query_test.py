import urllib.request
from bs4 import BeautifulSoup

searchURL = "https://pubmed.ncbi.nlm.nih.gov/?term=Climate+change+Zika+statistical"
advancedURL = "https://pubmed.ncbi.nlm.nih.gov/historyCacheExists/"

headers = { 'User-Agent' : 'Mozilla/5.0' }

req = urllib.request.Request(
    searchURL, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)

contents = urllib.request.urlopen(req).read()
print('contents')

req = urllib.request.Request(
    advancedURL, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
)
advancedContent = urllib.request.urlopen(req).read()
print(advancedContent)