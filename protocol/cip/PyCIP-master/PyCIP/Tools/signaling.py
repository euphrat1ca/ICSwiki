#from multiprocessing import Queue
from queue import Queue, Empty

class Signaler():
    signal_subscriber_table = {}
    instance_id = 1

    def __init__(self):
        self.id = self.instance_id
        self.instance_id += 1
        self.message_queue = Queue()

    def register(self, signal_id):
        if signal_id not in self.signal_subscriber_table:
            self.signal_subscriber_table[signal_id] = []
        if self.message_queue not in self.signal_subscriber_table[signal_id]:
            self.signal_subscriber_table[signal_id].append(self.message_queue)

    def unregister(self, signal_id):
        if signal_id not in self.signal_subscriber_table:
            return None
        if self.message_queue in self.signal_subscriber_table[signal_id]:
            index = self.signal_subscriber_table[signal_id].index(self.message_queue)
            del self.signal_subscriber_table[signal_id][index]

    def send_message(self, signal_id, message):
        message_s = MessageStruct(signal_id, self.id, message)
        for sub in self.signal_subscriber_table[signal_id]:
            sub.put(message_s)

    def get_message(self,time_out=None):
        try:
            return self.message_queue.get(True, time_out)
        except Empty:
            return None

class SignalerM2M():
    signal_message_table = {}
    instance_id = 1

    def __init__(self):
        self.id = self.instance_id
        self.instance_id += 1

    def register(self, signal_id):
        if signal_id not in self.signal_message_table:
            self.signal_message_table[signal_id] = Queue()

    def unregister(self, signal_id):
        del self.signal_message_table[signal_id]

    def send_message(self, signal_id, message):
        signal_id = int(signal_id)
        message_s = MessageStruct(signal_id, self.id, message)
        self.signal_message_table[signal_id].put(message_s)

    def get_message(self, signal_id, time_out=None):
        try:
            return self.signal_message_table[signal_id].get(True, time_out)
        except Empty:
            return None


class MessageStruct():
    def __init__(self, signal_id, sender_id, message):
        self.signal_id = signal_id
        self.sender_id = sender_id
        self.message   = message






