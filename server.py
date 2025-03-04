#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, parse_qsl, urlparse
import os
from IPython import embed
#import SocketServer
from ppdbmodel import PPDBModel

class MyModel():
  def getOutput(inputStr):
    return "This is a server output!"

class MyServer(SimpleHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self.path = self.server.wd+self.path
    print(self.path)
    super(MyServer,self).do_GET()
    
  def do_POST(self):
    print(urlparse(self.path))
    print(urlparse(self.path).query)
    params = parse_qs(urlparse(self.path).query)
    # it's a list in case there's duplicates
    inputText = params["inputText"][0] 
    inputText = inputText.replace("|||","\n").strip()
    dimension = params["dimension"][0]
    change = params["change"][0]
    changeDirection = 'High' if change == 'increase' else 'Low'
    self._set_headers()
    # self.wfile.write(('Paraphrasing "' + inputText + '" to ' + changeDirection + ' ' + dimension + '...').encode()) 
    response, possible_words, scores = self.server.nlgModel.getOutput(inputText, dimension, change)
    self.wfile.write((changeDirection + ' ' + dimension + ' paraphrase: ').encode())
    self.wfile.write(response.encode())
    self.wfile.write(('<br/>' + possible_words).encode())
    self.wfile.write(('<br/> PERPLEXITIES').encode())
    sorted_items = sorted(scores, key=scores.get)
    for item in sorted_items:
      self.wfile.write(('<br/>' + item + ' : ' + str(scores[item])).encode())
    
def run(nlg, serverClass=HTTPServer, handlerClass=MyServer):
  serverAddress = ('0.0.0.0', 5678)
  httpd = serverClass(serverAddress, handlerClass)
  
  httpd.nlgModel = nlg
  httpd.wd = os.path.dirname(__file__)
  
  print("Listening at",serverAddress)
  print(httpd.wd)
  httpd.serve_forever()

if __name__ == '__main__':
  run(nlg=PPDBModel()) # run(nlg=MyModel())
