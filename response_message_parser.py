from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ResponseMessage:
    """响应消息数据类，用于存储解析后的字段"""
    version: str
    trans_type: str
    trans_amount: str
    other_amount: str
    pan: str
    expiry_date: str
    resp_code: str
    rrn: str
    approval_code: str
    date: str
    time: str
    merchant_id: str
    terminal_id: str
    offline_flag: str
    cardholder_name: str
    pan_cashier_card: str
    invoice_number: str
    batch_number: str
    issuer_id: str
    installment_flag: str
    dcc_flag: str
    redeem_flag: str
    information_amount: str
    dcc_decimal_place: str
    dcc_currency_name: str
    dcc_exchange_rate: str
    coupon_flag: str
    filler: str

    def __str__(self):
        """格式化输出响应消息的内容"""
        return (
            f"Version: {self.version}\n"
            f"Transaction Type: {self.trans_type}\n"
            f"Transaction Amount: {self.trans_amount}\n"
            f"Other Amount: {self.other_amount}\n"
            f"PAN: {self.pan}\n"
            f"Expiry Date: {self.expiry_date}\n"
            f"Response Code: {self.resp_code}\n"
            f"RRN: {self.rrn}\n"
            f"Approval Code: {self.approval_code}\n"
            f"Date: {self.date}\n"
            f"Time: {self.time}\n"
            f"Merchant ID: {self.merchant_id}\n"
            f"Terminal ID: {self.terminal_id}\n"
            f"Offline Flag: {self.offline_flag}\n"
            f"Cardholder Name: {self.cardholder_name}\n"
            f"PAN Cashier Card: {self.pan_cashier_card}\n"
            f"Invoice Number: {self.invoice_number}\n"
            f"Batch Number: {self.batch_number}\n"
            f"Issuer ID: {self.issuer_id}\n"
            f"Installment Flag: {self.installment_flag}\n"
            f"DCC Flag: {self.dcc_flag}\n"
            f"Redeem Flag: {self.redeem_flag}\n"
            f"Information Amount: {self.information_amount}\n"
            f"DCC Decimal Place: {self.dcc_decimal_place}\n"
            f"DCC Currency Name: {self.dcc_currency_name}\n"
            f"DCC Exchange Rate: {self.dcc_exchange_rate}\n"
            f"Coupon Flag: {self.coupon_flag}\n"
            f"Filler: {self.filler}"
        )

class ResponseMessageParser:
    """响应消息解析器"""
    
    # 字段定义：(字段名, 长度)
    FIELDS = [
        ('version', 1),
        ('trans_type', 2),
        ('trans_amount', 12),
        ('other_amount', 12),
        ('pan', 19),
        ('expiry_date', 4),
        ('resp_code', 2),
        ('rrn', 12),
        ('approval_code', 6),
        ('date', 8),
        ('time', 6),
        ('merchant_id', 15),
        ('terminal_id', 8),
        ('offline_flag', 1),
        ('cardholder_name', 26),
        ('pan_cashier_card', 16),
        ('invoice_number', 6),
        ('batch_number', 6),
        ('issuer_id', 2),
        ('installment_flag', 1),
        ('dcc_flag', 1),
        ('redeem_flag', 1),
        ('information_amount', 12),
        ('dcc_decimal_place', 1),
        ('dcc_currency_name', 3),
        ('dcc_exchange_rate', 8),
        ('coupon_flag', 1),
        ('filler', 8)
    ]

    @staticmethod
    def _decode_bytes(data: bytes) -> str:
        """将字节数据解码为字符串，去除空白"""
        try:
            return data.decode('ascii').strip()
        except UnicodeDecodeError:
            return data.hex().upper()

    @classmethod
    def parse(cls, data: bytes) -> Optional[ResponseMessage]:
        """
        解析字节数组为ResponseMessage对象
        
        Args:
            data: 要解析的字节数组
            
        Returns:
            ResponseMessage对象或None（如果解析失败）
        """
        try:
            if not data:
                raise ValueError("Empty data received")

            # 创建字段值字典
            field_values = {}
            current_pos = 0

            # 解析每个字段
            for field_name, length in cls.FIELDS:
                if current_pos + length > len(data):
                    raise ValueError(f"Data too short for field {field_name}")
                
                field_data = data[current_pos:current_pos + length]
                field_values[field_name] = cls._decode_bytes(field_data)
                current_pos += length

            # 创建ResponseMessage对象
            return ResponseMessage(**field_values)

        except Exception as e:
            print(f"Error parsing message: {e}")
            return None

    @classmethod
    def parse_hex(cls, hex_string: str) -> Optional[ResponseMessage]:
        """
        解析十六进制字符串为ResponseMessage对象
        
        Args:
            hex_string: 十六进制字符串
            
        Returns:
            ResponseMessage对象或None（如果解析失败）
        """
        try:
            # 移除可能的空白符和0x前缀
            hex_string = hex_string.strip().replace('0x', '')
            # 转换为字节数组
            data = bytes.fromhex(hex_string)
            return cls.parse(data)
        except Exception as e:
            print(f"Error parsing hex string: {e}")
            return None

# 使用示例
def example_usage():
    # 创建示例数据（实际使用时替换为真实数据）
    sample_data = bytearray(200)  # 创建200字节的空数组
    
    # 填充一些示例数据
    sample_data[0:1] = b'2'  # Version
    sample_data[1:3] = b'01'  # TransType
    sample_data[3:15] = b'000000001000'  # TransAmount
    # ... 其他字段的示例数据
    
    # 解析字节数组
    parser = ResponseMessageParser()
    response = parser.parse(sample_data)
    
    if response:
        print("Successfully parsed response message:")
        print(response)
        
        # 访问特定字段
        print(f"\nTransaction Type: {response.trans_type}")
        print(f"Transaction Amount: {response.trans_amount}")
        
        # 如果是日期时间字段，可以转换为datetime对象
        try:
            trans_date = datetime.strptime(f"{response.date}{response.time}", "%Y%m%d%H%M%S")
            print(f"Transaction DateTime: {trans_date}")
        except ValueError:
            print("Invalid date/time format")
    else:
        print("Failed to parse response message")

if __name__ == "__main__":
    example_usage()