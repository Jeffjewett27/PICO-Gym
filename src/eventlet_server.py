#!/usr/bin/env python

import json
import eventlet
from eventlet import wsgi, websocket
from config import host, port

@websocket.WebSocketWSGI
def pico_handle(ws):
    while True:
        message = ws.wait()
        if message is None: return
            
        # data = json.loads(message)
        # pico_message = data['pico'] + ' message'
        ws.send(json.dumps({ 'input': 5 }))

def site(env, start_response):
    if env['PATH_INFO'] == '/greeting':
        return greeting_handle(env, start_response)
    elif env['PATH_INFO'] == '/pico':
        return pico_handle(env, start_response)
    else:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Eventlet running...']

def run_test():
    # print('Server starting at: ' + 'ws://{}:{}'.format(host, port))
    listener = eventlet.listen((host, port))
    wsgi.server(listener, site)

if __name__ == '__main__':
    run_test()