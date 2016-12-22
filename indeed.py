import os
from BeautifulSoup import BeautifulSoup
import re
import urllib
import urllib2
import ssl
import time
import requests

def createDir():
    if not os.path.isdir('/Users/houxiao/Desktop/DSNYCFTEL'):
        os.makedirs('/Users/houxiao/Desktop/DSNYCFTEL')
    else:
        print "dir already exists."
    return


def getTitle(ad):
    title = 'NA'
    titleChunk = ad.find('a', {'class': re.compile('turnstileLink')})
    if titleChunk:
        title = titleChunk.get('title').encode('ascii', 'ignore')
    return title


def getCompany(ad):
    company = 'NA'
    companyChunk = ad.find('span', {'class': 'company'})
    if companyChunk:
        company = companyChunk.text.encode('ascii', 'ignore')
    return company

def getUrl(ad):
    adUrl = 'NA'
    urlChunk = ad.find('a', {'rel': 'nofollow'})
    if urlChunk:
        adUrl = urlChunk.get('href').encode('ascii', 'ignore')
    return adUrl

def getPageInfo(ad,fileName):
    adUrl='http://www.indeed.com/'+getUrl(ad)
    print adUrl
    context = ssl._create_unverified_context()
    pageInfo = urllib.urlopen(adUrl,context=context).read()
    fw = open('/Users/houxiao/Desktop/DSNYCFTEL/' + fileName + '.html', 'w')
    fw.write(pageInfo)
    fw.close()


def run(url):
    html = None

    try:
        # use the browser to access the url
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
        html = response.content  # get the html\
    except Exception as e:  # browser.open() threw an exception, the attempt to get the response failed
        print 'failed attempt'
        time.sleep(2)

    soup = BeautifulSoup(html)

    ads = soup.findAll('div', {'class': re.compile(' row  result')})

    for ad in ads:
        title = getTitle(ad)
        title = title.replace('/', unichr(ord('/') + 65248)).replace('\\', unichr(ord('\\') + 65248))
        company = getCompany(ad)
        fileName = title + ' ' + company
        getPageInfo(ad,fileName)


if __name__ == '__main__':
    createDir()
    for i in range(0,330,10):
    #for i in range(0, 30, 10):
        print i
        url = 'http://www.indeed.com/jobs?q=data+scientist&l=NYC,+NY&rbl=New+York,+NY&jlid=45f6c4ded55c00bf&jt=fulltime&explvl=entry_level&start='+str(i)+'&pp='
        print url
        run(url )
