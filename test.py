from ecr_message import ECRMessage
import wrap

def echoMsg():
    ecr = ECRMessage()
    ecr.set_version(b"\x03")
    ecr.set_trans_type("17") #echoMsg
    # ecr.set_dcc_flag("N")
    return ecr


def example_usage():
    ecr = ECRMessage()
    
    # 设置交易信息
    ecr.set_trans_type("01")           # 交易类型
    ecr.set_trans_amount("10")         # 金额10.00
    ecr.set_pan("1234567890123456")    # 卡号
    ecr.set_expiry_date("1224")        # 有效期
    ecr.set_invoice_number("123456")   # 票据号
    # ... 其他字段

if __name__ == "__main__":
    print(wrap.to_hex(b" "))
    # ecr = echoMsg()
    # # 获取字节消息
    # message_bytes = ecr.build()
    # print("Message bytes length:", len(message_bytes))
    # print("Raw bytes:", message_bytes)
    
    # # 获取十六进制表示
    # message_hex = ecr.build_hex()
    # print("Hex representation:", message_hex)
    
    # # 打印每个字段的实际值
    # print("\nField values in hex:")
    # print(f"Version: {ecr.version.hex()}")
    # print(f"TransType: {ecr.trans_type.hex()}")
    # print(f"TransAmount: {ecr.trans_amount.hex()}")

    # result = ECRMessage._str_to_bytes("b", 1)
    # print(result.hex())
    # print(b'\x15')

    # print(ECRMessage.get_formatted_date())