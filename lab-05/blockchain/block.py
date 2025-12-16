import hashlib
import time


class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof):
        """
        Hàm khởi tạo (Constructor) cho một khối mới.
        """
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        # Tự động tính toán hash ngay khi khối được tạo
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Hàm tạo chuỗi băm (hash) SHA-256 cho khối hiện tại
        dựa trên các thông tin của nó.
        """
        # 1. Gom tất cả thông tin lại thành một chuỗi string
        data = (
            str(self.index)
            + str(self.previous_hash)
            + str(self.timestamp)
            + str(self.transactions)
            + str(self.proof)
        )

        # 2. Mã hóa chuỗi đó thành bytes và băm bằng SHA-256
        return hashlib.sha256(data.encode()).hexdigest()
