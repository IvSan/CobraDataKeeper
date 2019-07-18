import argparse

from peer import Peer


def chainer():
    args = parse_args()

    peer = Peer()
    peer.store_data(args.data)
    peer.keep_chain(args.number)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', nargs='*')
    parser.add_argument('-n', '--number', type=int, default=1)
    return parser.parse_args()


if __name__ == '__main__':
    chainer()
