import struct
from ecr_message import ECRMessage

def to_hex(byte_array):
    hex_string = " ".join([hex(b)[2:].zfill(2) for b in byte_array])
    return hex_string
    # print(hex_string)

def bcd_to_bin(bcd):
    binary_str = ""
    for digit in str(bcd):
        # 将每个字符转换为整数
        digit_int = int(digit)
        # 将整数转换为4位二进制字符串
        binary_str += format(digit_int, "04b")
    return binary_str.zfill(16)


def bin_to_bytes(bin_str):
    return bytes(int(bin_str[i : i + 8], 2) for i in range(0, len(bin_str), 8))

def wrap_message(data):
    """
    发送消息函数

    Args:
        data (str): 要发送的消息数据

    Returns:
        bytes: 封装后的消息字节流
    """
    # 计算消息长度
    length = len(data)
    length_bytes = bin_to_bytes(bcd_to_bin(length))
    # length_bytes = struct.pack(">H", len(data))  # b"\x01" + b"\x50"  #

    # 计算LRC（从length_bytes开始，包含data和ETX）
    lrc = 0
    message_content = length_bytes + data + b"\x03"
    for byte in message_content:
        lrc ^= byte
    # print("original: ", data)
    # 构造完整消息
    message = b"\x02" + message_content + bytes([lrc])
    # print("after framed: ", to_hex(message))

    return message


def echoMsg():
    ecr = ECRMessage()
    ecr.set_version(b"\x03")
    ecr.set_trans_type("17")  # echoMsg
    # ecr.set_dcc_flag("N")
    return ecr

if __name__ == "__main__":
    msg = echoMsg().build()
    wraped_msg = wrap_message(msg)
    # print(len(wraped_msg))
    # print(to_hex(decimal_to_two_hex(150)))

    # number = 50
    # result = b'\x01' + b'\x50'# bytes([number, 30])
    # print(to_hex(result))
    # print(b'\x50')
    # # 转换为十六进制字符串
    # hex_str = hex(lrc)[2:]  # 去掉0x前缀
    # # 转换为字节对象
    # byte_data = bytes(hex_str, 'ascii')
