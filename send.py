import wrap
from ecr_message import ECRMessage
from response_message_parser import ResponseMessageParser
import serial
import binascii

from datetime import datetime
import libusb_package
import usb.core
import usb.backend.libusb1


def echoMsg():
    ecr = ECRMessage()
    ecr.set_version(b"\x03")
    ecr.set_trans_type("17")  # echoMsg
    return ecr


def saleDebitMsg():
    ecr = ECRMessage()
    ecr.set_version(b"\x03")
    ecr.set_trans_type("01")
    ecr.set_trans_amount("5725")
    ecr.set_pan("1688700627201892")
    ecr.set_expiry_date("2510")
    return ecr


def parseResponse(data):
    # 解析字节数组
    parser = ResponseMessageParser()
    response = parser.parse(data[3:-2])

    if response:
        print("Successfully parsed response message:")
        print(response)

        # 访问特定字段
        print(f"\nTransaction Type: {response.trans_type}")
        print(f"Transaction Amount: {response.trans_amount}")

        # 如果是日期时间字段，可以转换为datetime对象
        try:
            trans_date = datetime.strptime(
                f"{response.date}{response.time}", "%Y%m%d%H%M%S"
            )
            print(f"Transaction DateTime: {trans_date}")
        except ValueError:
            print("Invalid date/time format")
    else:
        print("Failed to parse response message")


def sendBylibusb():
    libusb1_backend = usb.backend.libusb1.get_backend(
        find_library=libusb_package.find_library
    )
    # print(list(usb.core.find(find_all=True, backend=libusb1_backend)))

    # dev = usb.core.find(idVendor=0x0B00, idProduct=0x0055, backend=libusb1_backend)
    dev = usb.core.find(
        idVendor=0x1E0E, idProduct=0x902B, backend=libusb1_backend
    )  # Fiuu
    # 打开设备
    if dev is None:
        raise ValueError("Device not found")

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    # 发送命令
    endpoint_in = 0x81
    # endpoint_out = 0x2
    endpoint_out = 0x1  # for Fiuu

    # dev.write(endpoint_out, wrap.wrap_message(cmd))
    hex_string = "02004336303030303030303030313030303030301C303000203030303030303030303030303030303030301C0357"
    byte_array = bytes.fromhex(hex_string)
    print(byte_array)
    dev.write(endpoint_out, byte_array)

    # 读取返回数据
    while True:
        try:
            data = dev.read(endpoint_in, 64, timeout=2)
            print("Received data:", data)
            if len(data) > 1:
                parseResponse(data)
        except usb.core.USBTimeoutError as e:
            print("time out: ", e)
            break
        except usb.core.USBError as e:
            if e.errno == 84:
                print("USB数据传输溢出：", e)
            break

    dev.write(endpoint_out, b"\x06")


ser = serial.Serial(port="/dev/tty.usbmodem1301", baudrate=11520, timeout=2)


def sendACK():
    ser.write(b"\x06")


def sendBySerial(bytes):
    ser.write(bytes)
    return ser.readline()
    # print(ser.readline())
    # print(ser.readline())
    # ser.write("\x06")


if __name__ == "__main__":
    # Fiuu test message
    # hex_string = "02009236303030303030303030313032303030301C30300020303030303030303030303030303030303030301C3636002030303032303233303632303039303931323937311C34300012303030303030303030303130301C4D31000230301C03DA"
    # byte_array = binascii.a2b_hex(hex_string)

    # BCA test message
    # cmd = echoMsg().build()
    cmd = saleDebitMsg().build()
    byte_array = wrap.wrap_message(cmd)
    code = sendBySerial(byte_array)
    if code == b"\x06":
        i = 0
        while i < 5:
            response = ser.readline()
            print("response:", wrap.to_hex(response))
            if len(response) > 1:
                parseResponse(response)
                sendACK()
                break
            i += 1
