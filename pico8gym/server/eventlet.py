#!/usr/bin/env python

import json
import threading
import eventlet
from eventlet import wsgi, websocket
from .config import host, port
# from pico8gym.img_util import b64_decode_img
# from time import sleep
from pico8gym.envs.pico_env_pool import PicoEnvPool
from pico8gym.pico_output import PicoOutput

class SocketServer:
    instance = None

    @staticmethod
    def ensure_instance():
        print(SocketServer.instance)
        if (SocketServer.instance is None):
            print("No instance found. Creating server")
            SocketServer.instance = SocketServer()
        return SocketServer.instance
        
    def __init__(self) -> None:
        self.host = host
        self.port = port
        listener = eventlet.listen((host, port))
        self.thread = threading.Thread(target=run_server, args=(listener, host, port))
        self.thread.start()

def run_server(listener, host, port):
    print('Server starting at: ' + 'ws://{}:{}'.format(host, port))
    wsgi.server(listener, site)

@websocket.WebSocketWSGI
def pico_handle(ws):
    print(ws.environ['REMOTE_PORT'])
    env = PicoEnvPool.get_instance().get_orphan_env()
    env.connect(ws)
    while True:
        message = ws.wait()
        if message is None: return
            
        data = json.loads(message)
        output = PicoOutput.from_dict(data)
        env.receive(output)
        # if ('screen' in data):
        #     b64_decode_img(data['screen'])
        # else:
        #     print(f"No Screen Provided: {message}")
        # # pico_message = data['pico'] + ' message'
        # sleep(0.2)
        # ws.send(json.dumps({ 'input': 5 }))

def site(env, start_response):
    if env['PATH_INFO'] == '/pico':
        print("site")
        return pico_handle(env, start_response)
    else:
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Eventlet running...']

def run_test():
    SocketServer.ensure_instance()

if __name__ == '__main__':
    run_test()