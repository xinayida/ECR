from ecr_message import ECRMessage
import wrap
import serial


def echoMsg():
    ecr = ECRMessage()
    ecr.set_version(b"\x03")
    ecr.set_trans_type("17")  # echoMsg
    # ecr.set_dcc_flag("N")
    return ecr


def example_usage():
    ecr = ECRMessage()

    # 设置交易信息
    ecr.set_trans_type("01")  # 交易类型
    ecr.set_trans_amount("10")  # 金额10.00
    ecr.set_pan("1234567890123456")  # 卡号
    ecr.set_expiry_date("1224")  # 有效期
    ecr.set_invoice_number("123456")  # 票据号
    # ... 其他字段


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


def to_hex(byte_array):
    hex_string = " ".join([hex(b)[2:].zfill(2) for b in byte_array])
    return hex_string

def test_fiuu():
    ser = serial.Serial(port="/dev/tty.usbmodem11301", baudrate=11520, timeout=2)
    hex_string = "02004336303030303030303030313030303030301C303000203030303030303030303030303030303030301C0357"
    byte_array = bytes.fromhex(hex_string)
    ser.write(byte_array)
    print(ser.readline())

if __name__ == "__main__":
    message_length = 20
    print(message_length.to_bytes(2, byteorder='big'))
    # test_fiuu()
    # 示例
    # bcd = 150
    # print(to_hex(b'02'))
    # bin_str = bcd_to_bin(bcd)
    # bytes_data = bin_to_bytes(bin_str)
    # print(bin_str, to_hex(bytes_data))
    # print(to_hex("150".encode("ascii")), to_hex("150".encode("utf-8")))
