
import os
import sys
import logging
import json
from random import randint, choice
import ast


from flask import Flask, render_template, jsonify, g, request, Response

# Ensure paths then use . package notation and __init__ files.
this_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if this_dir not in sys.path:
    sys.path.append(this_dir)

# Basic lagging configuration
logging.basicConfig(format='%(levelname)s:\t%(message)s', level=logging.INFO, filename=os.path.dirname(os.path.abspath(__file__))+'/timestreams.log')
logger = logging.getLogger(__name__)


# Flask App configuration
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = ''
app.name = 'oscars'
print app.name


@app.route('/oscarsData')
def oscarsData():
    watched = request.args.get('watched', None)
    fp = open(this_dir+"/oscars/static/data/oscarsData.json", 'r')
    out = json.load(fp)
    fp.close()
    if watched == 'all':
        return Response(json.dumps(out),  mimetype='application/json')
    elif watched == 'no':
        filt = []
        for pic in out:
            if pic['watched']=='no':
                filt.append(pic)
        return Response(json.dumps(filt),  mimetype='application/json')
    elif watched == 'yes':
        filt = []
        for pic in out:
            if pic['watched']=='yes':
                filt.append(pic)
        return Response(json.dumps(filt),  mimetype='application/json')
    else:
        return Response(json.dumps(out),  mimetype='application/json')


@app.route('/picker')
def picker():
    fp = open(this_dir+"/oscars/static/data/oscarsData.json", 'r')
    jsonData = json.load(fp)
    pick = {}
    while 1>0:
        pick = choice(jsonData)
        if pick['watched']=='no':
            break
    print pick
    return Response(json.dumps(pick),  mimetype='application/json')


@app.route('/oscarsWatched')
def oscarsWatched():
    uid = request.args.get('uid', None)
    fp = open(this_dir+"/oscars/static/data/oscarsData.json", 'r')
    jsonData = json.load(fp)
    fp.close()
    newData = []
    pick = {}
    for pic in jsonData:
        if pic['uid'] == int(uid):
            pic['watched'] = 'yes'
        newData.append(pic.copy())
    fp = open(this_dir+"/oscars/static/data/oscarsData.json", 'w')
    json.dump(newData, fp)
    fp.close()
    return Response(json.dumps('[{\'res\':0}]'),  mimetype='application/json')

@app.route('/oscars')
def hashPath():
    """ normal http request to a serve up the page """
    return render_template('index.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)







