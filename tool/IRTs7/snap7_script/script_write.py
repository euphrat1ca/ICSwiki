# import ctypes
import snap7
#  from snap7 import util


conf = {
    "host": "127.0.0.1",
    "port": 1102,
}


def connect(conf):
    """"""
    client = snap7.client.Client()
    client.connect(conf['host'], 0, 2, conf['port'])
    return client


def write(client):
    """"""
    # db read db, start, size
    # attention!!! size is byte
    client.db_write(1, 7, (30).to_bytes(1, byteorder='big'))


def main():
    """"""
    client = connect(conf)
    write(client)


if __name__ == '__main__':
    main()
