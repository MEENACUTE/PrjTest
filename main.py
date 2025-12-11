import argparse
import sys
from peer import P2PPeer
import threading

def main():
    parser = argparse.ArgumentParser(description="P2P File Transfer Peer")
    parser.add_argument('--port', type=int, required=True, help='Port to listen on')
    parser.add_argument('--peer_ip', type=str, help='IP of the other peer')
    parser.add_argument('--peer_port', type=int, help='Port of the other peer')
    args = parser.parse_args()

    peer = P2PPeer(port=args.port, peer_ip=args.peer_ip, peer_port=args.peer_port)
    threading.Thread(target=peer.start_server).start()

    print("Enter commands: 'send <filename>' to send file, 'exit' to quit.")
    while True:
        cmd = input("> ").strip()
        if cmd.startswith('send '):
            filename = cmd.split(' ', 1)[1]
            peer.send_file(filename)
        elif cmd == 'exit':
            sys.exit(0)

if __name__ == "__main__":
    main()