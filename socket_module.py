import socket
import struct
import threading


class Controller:
    CMP_HEADER_SIZE = 16
    CODE_TYPE = "utf-8"
    SOCKET_TIME_OUT = 10

    @staticmethod
    def cmp_request(str_ip, n_port, n_command, str_body, response_data):

        #if threading.current_thread() is threading.main_thread():
         #   print("[Controller] WARRING: YOU ARE USE MAIN THREAD!, please run this socket by other thread")

        if not (isinstance(response_data, CMPResponseData)) or not (isinstance(str_ip, str)) or not (
                isinstance(str_body, str)) or not (isinstance(n_port, int)) or not (isinstance(n_command, int)):
            return_status = CMPErrorCode.ERR_INVALID_PARAM

        else:

            return_status = CMPErrorCode.ERR_NO_ERROR

            try:
                socket_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                if socket_connect is None:
                    return_status = CMPErrorCode.ERR_SOCKET_INVALID
                else:
                    socket_connect.settimeout(Controller.SOCKET_TIME_OUT)
                    socket_connect.connect((str_ip, n_port))

                    # add Null-terminated strings for our server judge
                    str_body += "\0"

                    # get this packet length
                    # length  = header size + body size(null-terminated string included)
                    n_length = Controller.CMP_HEADER_SIZE + len(str_body.encode(Controller.CODE_TYPE))

                    # > is mean big ending format, 4i is mean four integer included, s is mean char included
                    str_format = ">4i" + str(len(str_body.encode(Controller.CODE_TYPE))) + "s"

                    send_seq_id = CMPSocketSequence.get_sequence()

                    byte_structs_data = struct.pack(str_format, n_length, n_command, CMPSocketPacketStatus.STATUS_ROK,
                                                    send_seq_id, str_body.encode(Controller.CODE_TYPE))

                    # send data
                    socket_connect.send(byte_structs_data)

                    # receive data
                    receive_header_data = socket_connect.recv(16)

                    if Controller.__check_receive_header_data(receive_header_data, n_command) is True:
                        rep_total_len = struct.unpack(">4i", receive_header_data)[0] - Controller.CMP_HEADER_SIZE
                        rep_remain_len = rep_total_len
                        rep_body_data = b''

                        while rep_remain_len > 0:
                            rep_body_partial_data = socket_connect.recv(rep_remain_len)

                            rep_remain_len -= len(rep_body_partial_data)

                            rep_body_data += rep_body_partial_data

                        response_data.n_sequence_id = send_seq_id
                        response_data.n_body_length = rep_total_len
                        response_data.n_command_id = n_command
                        response_data.str_response_message = rep_body_data

                        return_status = CMPErrorCode.ERR_NO_ERROR

                    else:
                        return_status = CMPErrorCode.ERR_PACKET_CONVERT
                        print("ERROR CODE: " + str(struct.unpack(">4i", receive_header_data)[2]))

                    socket_connect.close()
            except socket.error as e:
                return_status = CMPErrorCode.ERR_IO_EXCEPTION

        return return_status

    @staticmethod
    def __check_receive_header_data(data, n_command):

        header_tuple_data = struct.unpack(">4i", data)
        if header_tuple_data[2] == CMPSocketPacketStatus.STATUS_ROK and (
                n_command == (header_tuple_data[1] & CMPSocketPacketStatus.SHIFT)):
            return True

        return False


"""CMP socket packet status set"""


class CMPSocketPacketStatus:
    STATUS_ROK = 0x00000000  # No Error
    STATUS_RINVMSGLEN = 0x00000001  # Message Length is invalid
    STATUS_RINVCMDLEN = 0x00000002  # Command Length is invalid
    STATUS_RINVCMDID = 0x00000003  # Invalid Command ID
    STATUS_RINVBNDSTS = 0x00000004  # Incorrect BIND Status for given  command
    STATUS_RALYBND = 0x00000005  # Already in Bound State

    STATUS_SYSBUSY = 0x00000006  # Controller System Busy

    STATUS_RSYSERR = 0x00000008  # System Error
    STATUS_RBINDFAIL = 0x00000010  # Bind Failed
    STATUS_RINVBODY = 0x00000040  # Invalid Packet Body Data
    STATUS_RINVCTRLID = 0x00000041  # Invalid Controller ID
    STATUS_RINVJSON = 0x00000042  # Invalid JSON Data
    SHIFT = 0x00ffffff


"""CMP error code return"""


class CMPErrorCode:
    ERR_CMP = -1000
    ERR_NO_ERROR = 1000 + ERR_CMP
    ERR_PACKET_LENGTH = -6 + ERR_CMP
    ERR_PACKET_SEQUENCE = -7 + ERR_CMP
    ERR_REQUEST_FAIL = -8 + ERR_CMP
    ERR_SOCKET_INVALID = -9 + ERR_CMP
    ERR_INVALID_PARAM = -10 + ERR_CMP
    ERR_LOG_DATA_LENGTH = -11 + ERR_CMP
    ERR_EXCEPTION = -12 + ERR_CMP
    ERR_IO_EXCEPTION = -13 + ERR_CMP
    ERR_PACKET_CONVERT = -14 + ERR_CMP


"""CMP Command ID Set"""


class CMPCommandIdSet:
    generic_neck = 0x80000000
    bind_request = 0x00000001
    bind_response = 0x80000001
    authentication_request = 0x00000002
    authentication_response = 0x80000002
    access_log_request = 0x00000003
    access_log_response = 0x80000003
    initial_request = 0x00000004
    initial_response = 0x80000004
    sign_up_request = 0x00000005
    sign_up_response = 0x80000005
    unbind_request = 0x00000006
    unbind_response = 0x80000006
    update_request = 0x00000007
    update_response = 0x80000007
    reboot_request = 0x00000010
    reboot_response = 0x80000010
    config_request = 0x00000011
    config_response = 0x80000011
    power_port_set_request = 0x00000012
    power_port_set_response = 0x80000012
    power_port_state_request = 0x00000013
    power_port_state_response = 0x80000013
    ser_api_sign_in_request = 0x00000014
    ser_api_sign_in_response = 0x80000014
    enquire_link_request = 0x00000015
    enquire_link_response = 0x80000015
    rdm_login_request = 0x00000016
    rdm_login_response = 0x80000016
    rdm_operate_request = 0x00000017
    rdm_operate_response = 0x80000017
    rdm_logout_request = 0x00000018
    rdm_logout_response = 0x80000018
    device_control_request = 0x00000019
    device_control_response = 0x80000019
    device_state_request = 0x00000020
    device_state_response = 0x80000020
    semantic_request = 0x00000030
    semantic_response = 0x80000030
    amx_control_command_request = 0x00000040
    amx_control_command_response = 0x80000040
    amx_status_command_request = 0x00000041
    amx_status_command_response = 0x80000041
    amx_broadcast_status_command_request = 0x00000042
    amx_broadcast_status_command_response = 0x80000042
    semantic_word_request = 0x00000057
    semantic_word_response = 0x80000057


class CMPSocketSequence:
    __sequence = 0

    @staticmethod
    def get_sequence():
        print("now seq num: " + str(CMPSocketSequence.__sequence))
        CMPSocketSequence.__sequence += 1
        return CMPSocketSequence.__sequence


class CMPResponseData:
    str_response_message = ""
    n_sequence_id = 0
    n_command_id = 0
    n_body_length = 0
