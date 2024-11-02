import datetime

class ECRMessage:
    def __init__(self):
        self.version = b"\x02"  # fixed with "02h"
        self.trans_type = b"00"
        self.trans_amount = b"0" * 12
        self.other_amount = b"0" * 12
        self.pan = b" " * 19
        self.expiry_date = b"0" * 4
        self.cancel_reason = b"00"
        self.invoice_number = b"0" * 6
        self.auth_code = b" " * 6
        self.installment_flag = b" "
        self.redeem_flag = b" "
        self.dcc_flag = b"N"
        self.installment_plan = b" " * 3
        self.installment_tenor = b" " * 2
        self.generic_data = b" " * 12
        self.reff_number = b" " * 12
        self.original_date = b" " * 4
        self.filler = b" " * 50

    @staticmethod
    def get_formatted_date(format_str="%m%d"):
        """获取格式化后的日期字符串

        Args:
            format_str: 日期格式字符串，默认为"%m%d"

        Returns:
            str: 格式化后的日期字符串
        """

        now = datetime.datetime.now()
        return now.strftime(format_str)
    
    @staticmethod
    def _str_to_bytes(string, length, fillchar=b"0", side="left"):
        """
        将字符串转换为固定长度的字节数组。

        Args:
            string: 要转换的字符串。
            length: 目标字节数组的长度。
            encoding: 编码方式，默认为 utf-8。
            fillchar: 填充字符，默认为 '0'。
            side: 填充位置，'left' 表示左侧填充，'right' 表示右侧填充。

        Returns:
            固定长度的字节数组。
        """
        encoding = "utf-8"
        byte_array = string.encode(encoding)

        if len(byte_array) >= length:
            return byte_array[:length]
        else:
            fill_bytes = fillchar * (length - len(byte_array))
            if side == "left":
                return fill_bytes + byte_array
            else:
                return byte_array + fill_bytes
    def set_version(self, value):
        self.version = value

    def set_trans_type(self, value):
        self.trans_type = self._str_to_bytes(value, 2)

    def set_trans_amount(self, amount):
        self.trans_amount = self._str_to_bytes(amount, 12)

    def set_other_amount(self, amount):
        self.other_amount = self._str_to_bytes(amount, 12)

    def set_pan(self, pan):
        self.pan = self._str_to_bytes(pan, 19, b" ", "right")

    def set_expiry_date(self, date):
        if len(date) != 4:
            raise ValueError("ExpiryDate must be 4 characters (MMDD)")
        self.expiry_date = self._str_to_bytes(date, 4)

    def set_cancel_reason(self, reason):
        self.cancel_reason = self._str_to_bytes(reason, 2)

    def set_invoice_number(self, number):
        self.invoice_number = self._str_to_bytes(number, 6)

    def set_auth_code(self, auth_code):
        self.auth_code = self._str_to_bytes(auth_code, 6)

    def set_installment_flag(self, flag):
        if flag not in ["Y", "N"]:
            raise ValueError("InstallmentFlag must be 'Y' or 'N'")
        self.installment_flag = flag.encode('ascii')

    def set_redeem_flag(self, flag):
        if flag not in ["Y", "N"]:
            raise ValueError("RedeemFlag must be 'Y' or 'N'")
        self.redeem_flag = flag.encode('ascii')

    def set_dcc_flag(self, flag):
        if flag not in ["Y", "N"]:
            raise ValueError("DCCFlag must be 'Y' or 'N'")
        self.dcc_flag = flag.encode('ascii')

    def set_installment_plan(self, plan):
        self.installment_plan = self._str_to_bytes(plan, 3, b" ")

    def set_installment_tenor(self, tenor):
        self.installment_tenor = self._str_to_bytes(tenor, 2, b" ")

    def set_generic_data(self, data):
        self.generic_data = self._str_to_bytes(data, 12, b" ")

    def set_reff_number(self, number):
        self.reff_number = self._str_to_bytes(number, 12, b" ")

    def set_original_date(self, date):
        if len(date) != 4:
            raise ValueError("OriginalDate must be 4 characters (MMDD)")
        self.original_date = self._str_to_bytes(date, 4)

    def build(self):
        """构建150字节的消息"""
        message = (
            self.version
            + self.trans_type
            + self.trans_amount
            + self.other_amount
            + self.pan
            + self.expiry_date
            + self.cancel_reason
            + self.invoice_number
            + self.auth_code
            + self.installment_flag
            + self.redeem_flag
            + self.dcc_flag
            + self.installment_plan
            + self.installment_tenor
            + self.generic_data
            + self.reff_number
            + self.original_date
            + self.filler
        )

        if len(message) != 150:
            raise ValueError(f"Message length is {len(message)}, expected 150")

        return message

    def build_hex(self):
        """构建并返回十六进制字符串"""
        message = self.build()
        return message.hex().upper()



def echoMsg():
    ecr = ECRMessage()
    ecr.set_version(b"\x03")
    ecr.set_trans_type("17")  # echoMsg
    # ecr.set_dcc_flag("N")
    return ecr


if __name__ == "__main__":
    ecr = echoMsg()
    # 获取字节消息
    message_bytes = ecr.build()
    print("Message bytes length:", len(message_bytes))
    print("Raw bytes:", message_bytes)

    # 获取十六进制表示
    message_hex = ecr.build_hex()
    print("Hex representation:", message_hex)

    # 打印每个字段的实际值
    print("\nField values in hex:")
    print(f"Version: {ecr.version.hex()}")
    print(f"TransType: {ecr.trans_type.hex()}")
    print(f"TransAmount: {ecr.trans_amount.hex()}")
    