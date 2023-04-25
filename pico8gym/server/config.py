import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--host', default='0.0.0.0')
parser.add_argument('-p', '--port', default=5001, type=int)

args = parser.parse_args()
host, port = args.host, args.port