import argparse

from blockchain.peer import Peer


def chainer():
    args = parse_args()

    peer = Peer(args.file)
    peer.store_data(args.data)
    peer.keep_chain(args.number, args.verbose)

    print('Done!')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose logs, default false')
    parser.add_argument('-n', '--number', type=int, metavar='n', default=1,
                        help='number of blocks to mine for securing the data, default 1')
    parser.add_argument('-f', '--file', type=str, metavar='filename', default='chain',
                        help='file to keep all the data')
    parser.add_argument('data', nargs='*', help='data to store')
    return parser.parse_args()


if __name__ == '__main__':
    chainer()
