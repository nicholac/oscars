'''
Created on 18 Oct 2015

@author: dusted-ipro
'''

from bs4 import BeautifulSoup
import os
import urllib2
from urllib import urlretrieve
import time
from random import randint
import json


def getPoster(filmName, filmURL, outDir):
    '''Pull the poster - film is wikipedia url to film page
    '''
    try:
        response = urllib2.urlopen(filmURL)
        pHtml = response.read()
        pSoup = BeautifulSoup(pHtml, "lxml")
        #Find the poster url
        for s in pSoup.find('table'):
            img = s.find('img')
            if img and img!=-1:
                #Done
                imgURL = 'https:' + img['src']
                filename = outDir+filmName+"_poster.jpg"
                urlretrieve(imgURL, filename)
        return ['OK', filmName+"_poster.jpg"]
    except:
        return ['fail',filmName]


def firstPara(filmURL):
    '''Get the first paragraph from the page
    '''
    response = urllib2.urlopen(filmURL)
    pHtml = response.read()
    pSoup = BeautifulSoup(pHtml, "lxml")
    para = pSoup.find_all('p')[0]
    return para.get_text()

def resetWatched():
    '''Reset the Watched films
    '''
    projPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fp = open(projPath+'/static/data/oscarsData.json', 'r')
    data = json.load(fp)
    fp.close()
    cnt = 0
    for pic in data:
        pic['watched']='no'
        pic['carmenRate']=0
        pic['chrisRate']=0
        pic['uid']=cnt
        cnt+=1
    fp = open(projPath+'/static/data/oscarsData.json', 'w')
    json.dump(data, fp)
    fp.close()
    return

def getWinners():
    '''Get all the winners from the wiki doc and stash relevent info in a pkl
    wikidoc = path
    '''
    outFilm = {}
    outArr = []
    baseURL = 'https://en.wikipedia.org'
    baseMediaURL = 'https://upload.wikimedia.org'
    projPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    postersPath = projPath+"/static/data/posters/"
    wikiData = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/static/data/winnerswiki.html"
    soup = BeautifulSoup(open(wikiData), "lxml")
    winners = soup.find_all(style="background:#FAEB86")
    #Could give year here aswelll maybe
    fails = []
    for win in winners:
        #This is the name
        filmName = win.find('a').get_text()
        print filmName
        #Get the poster - works
        pURL = baseURL+win.find('a').get('href')
        poster = getPoster(filmName, pURL, postersPath)
        if poster[0] != 'OK':
            fails.append(poster[1])
            continue
        #Get the first para
        paraTxt = firstPara(pURL)
        #Build output
        outFilm['name']=filmName
        outFilm['synopsis']=paraTxt
        outFilm['postName']=poster[1]
        outFilm['wikiURL']=pURL
        outArr.append(outFilm.copy())
        print 'Sleeping...'
        time.sleep(randint(1,15))

    #Save to PKL
    fp = open(projPath+"/static/data/oscarsData.json",'w')
    json.dump(outArr, fp)
    fp.close()
    print fails
    print 'Done'


if __name__ == '__main__':
    resetWatched()