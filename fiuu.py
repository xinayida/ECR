import serial
from ecr_message import ECRMessage
import wrap

def echoMsg():
    ecr = ECRMessage()
    ecr.set_version(b"\x03")
    ecr.set_trans_type("17")  # echoMsg
    # ecr.set_dcc_flag("N")
    return ecr

# 打开串口，替换为你的实际端口
ser = serial.Serial('/dev/cu.EZVALOLYYD01', 9600)  # 9600是波特率，根据你的设备调整

cmd = echoMsg().build()
msg = wrap.wrap_message(cmd)
# 发送数据
ser.write(msg)

# 读取数据
data = ser.read(10)  # 读取10个字节
print(data)

# 关闭串口
ser.close()