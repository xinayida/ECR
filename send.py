import wrap
from ecr_message import ECRMessage
from response_message_parser import ResponseMessageParser

from datetime import datetime
import libusb_package
import usb.core
import usb.backend.libusb1


def echoMsg():
    ecr = ECRMessage()
    ecr.set_version(b"\x03")
    ecr.set_trans_type("17")  # echoMsg
    # ecr.set_dcc_flag("N")
    return ecr


def parseResponse(data):
    # 解析字节数组
    parser = ResponseMessageParser()
    response = parser.parse(data)

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


libusb1_backend = usb.backend.libusb1.get_backend(
    find_library=libusb_package.find_library
)
# print(list(usb.core.find(find_all=True, backend=libusb1_backend)))

dev = usb.core.find(idVendor=0x0B00, idProduct=0x0055, backend=libusb1_backend) 
# dev = usb.core.find(idVendor=0x1e0e, idProduct=0x902b, backend=libusb1_backend) #Fiuu
# 打开设备
if dev is None:
    raise ValueError("Device not found")

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# 发送命令
endpoint_in = 0x81
endpoint_out = 0x2
cmd = echoMsg().build()

dev.write(endpoint_out, wrap.wrap_message(cmd))

# 读取返回数据
while True:
    try:
        data = dev.read(endpoint_in, 64, timeout=2)
        if len(data) > 1:
            parseResponse(data)
        else:
            print("Received data:", data)
    except usb.core.USBTimeoutError as e:
        print("time out: ", e)
        break
    except usb.core.USBError as e:
        if e.errno == 84:
            print("USB数据传输溢出：", e)
        break

dev.write(endpoint_out, b"\x06")
