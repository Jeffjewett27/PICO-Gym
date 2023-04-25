#!/usr/bin/env python

import json
import threading
import atexit
import signal
import eventlet
from eventlet import wsgi, websocket
from .config import host, port
# from pico8gym.img_util import b64_decode_img
# from time import sleep
from pico8gym.envs.pico_env_pool import PicoEnvPool
from pico8gym.components.pico_output import PicoOutput

class SocketServer:
    instance = None

    @staticmethod
    def ensure_instance():
        signal.signal(signal.SIGINT, SocketServer.close_all)
        print(SocketServer.instance)
        if (SocketServer.instance is None):
            print("No instance found. Creating server")
            SocketServer.instance = SocketServer()
        return SocketServer.instance
    
    @staticmethod
    def check_active_connections():
        if not PicoEnvPool.get_instance().connection_exists() \
            and SocketServer.instance is not None:
            SocketServer.instance.close()

    @staticmethod
    def close_all(signal, frame):
        print("CLOSE ALL")
        if SocketServer.instance is not None:
            SocketServer.instance.close()
        raise KeyboardInterrupt()
        
    def __init__(self) -> None:
        self.host = host
        self.port = port
        self.connections = []
        listener = eventlet.listen((host, port))
        self.thread = threading.Thread(target=run_server, args=(listener, host, port))
        self.thread.isDaemon = True
        self.thread.start()
        # atexit.register(self.close)

    def close(self):
        print("CLOSING")
        for ws in self.connections:
            try:
                print(f"CLOSING {ws.environ['REMOTE_PORT']}")
                ws.close()
            except:
                print(f"Difficulty Closing {ws}")
        SocketServer.instance = None

def run_server(listener, host, port):
    print('Server starting at: ' + 'ws://{}:{}'.format(host, port))
    wsgi.server(listener, site)

@websocket.WebSocketWSGI
def pico_handle(ws):
    SocketServer.instance.connections.append(ws)
    print(ws.environ['REMOTE_PORT'])
    env = PicoEnvPool.get_instance().get_orphan_env()
    env.connect(ws)
    while True:
        message = ws.wait()
        if message is None: return
            
        data = json.loads(message)
        if 'event' not in data:
            continue
        event = data['event']
        if event == 'init':
            env.initialize()
        else:
            env.receive(data)

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