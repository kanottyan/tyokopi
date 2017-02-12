#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages/")
import cv2
from flask import Flask, redirect, url_for, request, g, jsonify
from random import randint

app = Flask(__name__)
 
fortune_strings = [u"大おっぱい", u"少おっぱい",u"大おっぱい"]

@app.route('/')
def hello():
    return redirect(url_for('py_result', number=randint(0,len(fortune_strings)-1)))
 
@app.route('/<int:number>/')
def py_result(number):
    if not 0 <= number < len(fortune_strings):
        number = -1
 
    html = u'<h1>{0}</h1>'.format(fortune_strings[number])
    html += u'<a href="{0}">引き直す</a>'.format(url_for('hello'))
 
    return html

@app.route('/compare', methods=['GET'])
def is_gakki():
    if request.method == 'GET':
        target_img = request.args.get("image", "")        

    IMG_DIR = os.path.abspath(os.path.dirname(__file__))
    IMG_SIZE = (200, 200)
    files = os.listdir(IMG_DIR + "/image_picture")
    IMG_SIZE = (200, 200)
    TARGET_FILE= "/target_imgs" + "/" + target_img

    threshold = 0.5
    response = {}
    response['score'] = {}
    target_img_path = IMG_DIR + TARGET_FILE
    try:
        target_img = cv2.imread(target_img_path)
        target_img = cv2.resize(target_img, IMG_SIZE)
        target_hist = cv2.calcHist([target_img], [0], None, [256], [0, 256])
    except:
        print("can't find the img from directory : " + target_img_path)
        response.update( {"status": "0"} )
        return jsonify( result = response )

    print('TARGET_FILE: %s' % (TARGET_FILE))
    for file in files:
        if file == '.DS_Store':
            continue
        try:
            comparing_img_path = IMG_DIR + "/image_picture/" + file
            comparing_img = cv2.imread(comparing_img_path)
            comparing_img = cv2.resize(comparing_img, IMG_SIZE)
            comparing_hist = cv2.calcHist([comparing_img], [0], None, [256], [0, 256])
            ret = cv2.compareHist(target_hist, comparing_hist, 0)
            if ret >= threshold:
                response.update({ "status" : "1"})
            #print response
            response['score'][str(file)] = str(ret)   
        except Exception as e:
            print e
    if not response.has_key('status'):
        response.update({"status" : "0"})
    print( response )
    return jsonify(result= response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="4999")
