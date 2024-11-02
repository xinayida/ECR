import struct
from ecr_message import ECRMessage


def echoMsg():
    ecr = ECRMessage()
    ecr.set_version(b"\x03")
    ecr.set_trans_type("17")  # echoMsg
    # ecr.set_dcc_flag("N")
    return ecr


def decimal_to_two_hex(number):
    high_byte = number // 100  # 获取高字节
    low_byte = number % 100  # 获取低字节

    print(high_byte, low_byte)
    # 将高低字节转换为字节对象
    return bytes([high_byte, low_byte])


def to_hex(byte_array):
    hex_string = " ".join([hex(b)[2:].zfill(2) for b in byte_array])
    return hex_string
    # print(hex_string)


def wrap_message(data):
    """
    发送消息函数

    Args:
        data (str): 要发送的消息数据

    Returns:
        bytes: 封装后的消息字节流
    """

    # 计算消息长度
    length_bytes = b"\x01" + b"\x50"  # struct.pack(">H", len(data))

    # 计算LRC（从length_bytes开始，包含data和ETX）
    lrc = 0
    message_content = length_bytes + data + b"\x03"
    for byte in message_content:
        lrc ^= byte
    print("original: ", to_hex(data))
    # 构造完整消息
    message = b"\x02" + message_content + bytes([lrc])
    print("after framed: ", to_hex(message))

    return message


if __name__ == "__main__":
    msg = echoMsg().build()
    wrap_message(msg)
    # print(to_hex(decimal_to_two_hex(150)))

    # number = 50
    # result = b'\x01' + b'\x50'# bytes([number, 30])
    # print(to_hex(result))
    # print(b'\x50')
    # # 转换为十六进制字符串
    # hex_str = hex(lrc)[2:]  # 去掉0x前缀
    # # 转换为字节对象
    # byte_data = bytes(hex_str, 'ascii')
