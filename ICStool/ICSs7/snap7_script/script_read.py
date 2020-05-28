# import ctypes
import snap7
from snap7 import util


conf = {
    "host": "127.0.0.1",
    "port": 1102,
}


def connect(conf):
    """"""
    client = snap7.client.Client()
    client.connect(conf['host'], 0, 2, conf['port'])
    return client


def query(client):
    """"""
    # db read db, start, size
    # attention!!! size is byte
    data1 = client.db_read(1, 1, 2)
    print(data1)
    data_1 = util.get_int(data1, 0)
    print(data_1)

    data2 = client.db_read(1, 2, 4)
    print(data2)
    data_2 = util.get_dword(data2, 0)
    print(data_2)

    data2 = client.db_read(1, 1, 10)
    print(data2)


def main():
    """"""
    client = connect(conf)
    query(client)


if __name__ == '__main__':
    main()
