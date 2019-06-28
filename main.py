#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from google.appengine.api import urlfetch
import json
import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="templates/") # このディレクトリーからテンプレートを読み込む設定が含まれているオブジェクトを作る。
templateEnv = jinja2.Environment(loader=templateLoader) # テンプレートを上のtemplateLoaderを使って読み込む環境を用意する。
pataTmpl = templateEnv.get_template("pata.html") # パタトクカシーー用のテンプレートを"pata.htmlから読み込む。
networkTmpl = templateEnv.get_template("norikae.html")  # 乗換案内用のテンプレートを"norikae.html"から読み込む。

networkJson = urlfetch.fetch("https://tokyo.fantasy-transit.appspot.com/net?format=json").content  # ウェブサイトから電車の線路情報をJSON形式でダウンロードする
network = json.loads(networkJson.decode('utf-8'))  # JSONとしてパースする（stringからdictのlistに変換する）

# このRequestHandlerでパタトカシーーのリクエストを処理して、結果を返す。
class Root(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
    self.response.write('''
<h1>Hello!</h1>
  <ul>
    <li><a href=/pata>パタトクカシーー</a></li>
    <li><a href=/norikae>乗換案内</a></li>
  </ul>
''')

# このRequestHandlerでパタトカシーーのリクエストを処理して、結果を返す。
class Pata(webapp2.RequestHandler):
    def get(self):
        a = self.request.get('a', '')
        b = self.request.get('b', '')
        pata = ''
        if len(a)>len(b):
            length = len(a)
        elif len(b)>len(a):
            length = len(b)
        else:
            length = len(a)

        for x in range(length):
            pata += a[x:x+1] + b[x:x+1]
        # とりあえずAとBをつなぐだけで返事を作っていますけど、パタタコカシーーになるように自分で直してください！
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        # テンプレートの内容を埋め込んで、返事を返す。
        self.response.write(pataTmpl.render(pata=pata, request=self.request))

class Norikae(webapp2.RequestHandler):

    def get(self):
        departure = self.request.get('departure', '')
        arrival = self.request.get('arrival', '')
        next= False
        transfer = []
"""
        for line in network:
            for station in line["Stations"]:
                if departure == station:
                    transfer.append(line["Name"])
                if arrival == station:
                    break
"""
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.write(networkTmpl.render(request=self.request,network=network))


app = webapp2.WSGIApplication([
    ('/', Root),
    ('/pata', Pata),
    ('/norikae', Norikae),
], debug=True)
