import json

from socket_module import CMPCommandIdSet
from thread_moudle import CMPThread



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
    __str_ip = "54.199.198.94"
    __n_port = 2310

    @staticmethod
    def get_ip():
        return SemanticWordServerInfo.__str_ip

    @staticmethod
    def get_port():
        return SemanticWordServerInfo.__n_port



class SemanticWordSync:

    def __init__(self, type_id):
        self.__type_id = type_id


    def send_word(self, str_word):
        json_data = json.dumps(
                {"id": SemanticWordMessageID.get_id(), "type": self.__type_id, "word": str_word, "total": 0,
                 "number": 0})

        import socket_module
        self.__response = socket_module.CMPResponseData()

        self.__error_code = socket_module.Controller.cmp_request(SemanticWordServerInfo.get_ip(),SemanticWordServerInfo.get_port(),
                                                                  CMPCommandIdSet.semantic_word_request,json_data,
                                                                 self.__response)

        if self.__error_code == socket_module.CMPErrorCode.ERR_NO_ERROR:
            print("server response: No ERROR")

        else:
            print("ERROR CODE: " + str(self.__error_code))

        return self.__error_code
    

    def get_result(self):
        
        return self.__response.str_response_message
  

class SemanticWord(object):
    
    
    def __init__(self, type_id, str_ip,n_port):
        import sys;
        reload(sys);
        sys.setdefaultencoding("utf8");
        self.__str_ip = str_ip
        self.__n_port = n_port
        self.__type_id = type_id
        
    def send_word(self, str_word):
        #self.logger.info("[SemanticWord] send word: "+str_word)
        json_data = json.dumps(
                {"id": SemanticWordMessageID.get_id(), "type": self.__type_id, "word": str_word, "total": 0,
                 "number": 0})

        thread = CMPThread(0, "this is a socket thread", self.__str_ip,
                           self.__n_port,
                           CMPCommandIdSet.semantic_word_request,
                           json_data)
        thread.start()
        thread.join()
        return {"result_code":thread.get_result_code(),"result_data":thread.get_result_data()}
    
    


class SemanticWordStory(SemanticWord):

    def __init__(self, str_ip, n_port):
        super(SemanticWordStory, self).__init__(SemanticWordTypeID.STORY_TYPE_ID,str_ip, n_port)

  


class SemanticWordFuzzy(SemanticWord):
    def __init__(self, str_ip, n_port):
        super(SemanticWordFuzzy, self).__init__(SemanticWordTypeID.UNKNOWN_TYPE_ID,str_ip, n_port)

   



