from block import Block
import hashlib
import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Tạo khối genesis (khối đầu tiên)
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        # Tạo khối mới
        block = Block(
            len(self.chain) + 1,
            previous_hash,
            time.time(),
            self.current_transactions,
            proof,
        )
        # Reset danh sách giao dịch hiện tại
        self.current_transactions = []
        # Thêm khối vào chuỗi
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # Thuật toán hash để tìm proof: hash(new_proof^2 - previous_proof^2)
            # Yêu cầu: 4 ký tự đầu của hash phải là '0000'
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()
            ).hexdigest()

            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def add_transaction(self, sender, receiver, amount):
        # Thêm giao dịch vào danh sách tạm thời
        self.current_transactions.append(
            {"sender": sender, "receiver": receiver, "amount": amount}
        )
        # Trả về index của khối tiếp theo sẽ chứa giao dịch này
        return self.get_previous_block().index + 1

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]

            # 1. Kiểm tra hash của khối trước đó có khớp không
            if block.previous_hash != previous_block.hash:
                return False

            # 2. Kiểm tra Proof of Work có hợp lệ không (có bắt đầu bằng 0000 không)
            previous_proof = previous_block.proof
            proof = block.proof
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()
            ).hexdigest()

            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1

        return True
