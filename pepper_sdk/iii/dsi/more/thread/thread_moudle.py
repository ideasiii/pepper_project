import threading
from iii.dsi.more.socket import socket_module


class CMPThread(threading.Thread):

    def __init__(self, n_thread_id, str_thread_name, str_ip, n_port, n_command_id, str_send_message):
        threading.Thread.__init__(self)
        self.__n_thread_id = n_thread_id
        self.__str_thread_name = str_thread_name
        self.__n_command_id = n_command_id
        self.__str_server_ip = str_ip
        self.__n_port = n_port
        self.__str_send_message = str_send_message
        self.__response = socket_module.CMPResponseData()
        self.__error_code = socket_module.CMPErrorCode.ERR_REQUEST_FAIL

    def run(self):
        print("start thread")
        self.__error_code = socket_module.Controller.cmp_request(self.__str_server_ip, self.__n_port,
                                                                 self.__n_command_id, self.__str_send_message,
                                                                 self.__response)

        if self.__error_code == socket_module.CMPErrorCode.ERR_NO_ERROR:
            print("thread id:" + str(self.__n_thread_id) + " print: " + self.__response.str_response_message)

        else:
            print("ERROR CODE: " + str(self.__error_code))

    def get_result(self):
        if self.__error_code == socket_module.CMPErrorCode.ERR_NO_ERROR:
            return self.__response.str_response_message
        return None
