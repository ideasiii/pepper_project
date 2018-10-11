import json

from iii.dsi.more.socket.socket_module import CMPCommandIdSet
from iii.dsi.more.thread.thread_moudle import CMPThread


class SemanticWord(object):

    def __init__(self, type_id):
        self.__type_id = type_id

    def send_word(self, str_word):
        json_data = json.dumps(
                {"id": SemanticWordMessageID.get_id(), "type": self.__type_id, "word": str_word, "total": 0,
                 "number": 0})

        thread = CMPThread(0, "this is a socket thread", SemanticWordServerInfo.get_ip(),
                           SemanticWordServerInfo.get_port(),
                           CMPCommandIdSet.semantic_word_request,
                           json_data)
        thread.start()
        thread.join()
        return thread.get_result()


class SemanticWordStory(SemanticWord):

    def __init__(self):
        super().__init__(SemanticWordTypeID.STORY_TYPE_ID)

    def send_word(self, str_word):
        super().send_word(str_word)


class SemanticWordFuzzy(SemanticWord):
    def __init__(self):
        super().__init__(SemanticWordTypeID.UNKNOWN_TYPE_ID)

    def send_word(self, str_word):
        super().send_word(str_word)


class SemanticWordTypeID:
    UNKNOWN_TYPE_ID = 0
    STORY_TYPE_ID = 4


class SemanticWordMessageID:
    __id = 0

    @staticmethod
    def get_id():
        SemanticWordMessageID.__id += 1
        return SemanticWordMessageID.__id


class SemanticWordServerInfo:
    __str_ip = "175.98.119.121"
    __n_port = 2310

    @staticmethod
    def get_ip():
        return SemanticWordServerInfo.__str_ip

    @staticmethod
    def get_port():
        return SemanticWordServerInfo.__n_port
