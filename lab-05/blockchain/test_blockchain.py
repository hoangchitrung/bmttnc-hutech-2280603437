from blockchain import (
    Blockchain,
)  # Import class Blockchain từ file blockchain.py [cite: 658]

# 1. Khởi tạo Blockchain
my_blockchain = Blockchain()  # [cite: 661]

print("--- Bắt đầu tạo giao dịch ---")

# 2. Thêm các giao dịch (Transactions) vào hàng chờ
# Alice chuyển cho Bob 10 coin
my_blockchain.add_transaction("Alice", "Bob", 10)  # [cite: 664]
# Bob chuyển cho Charlie 5 coin
my_blockchain.add_transaction("Bob", "Charlie", 5)  # [cite: 668]
# Charlie chuyển lại cho Alice 3 coin
my_blockchain.add_transaction("Charlie", "Alice", 3)  # [cite: 671]

print("--- Đang đào khối mới (Mining)... ---")

# 3. Quá trình Đào (Mining) khối mới
# B1: Lấy khối cuối cùng hiện tại để biết đâu là điểm nối tiếp
previous_block = my_blockchain.get_previous_block()  # [cite: 673, 678]
previous_proof = previous_block.proof  # [cite: 674, 679]
previous_hash = previous_block.hash  # [cite: 676, 681]

# B2: Chạy thuật toán Proof of Work để tìm con số may mắn (proof)
new_proof = my_blockchain.proof_of_work(previous_proof)  # [cite: 675, 680]

# B3: Thưởng cho thợ đào (Miner) vì đã tìm ra proof (Giao dịch từ 'Genesis' -> 'Miner')
my_blockchain.add_transaction("Genesis", "Miner", 1)  # [cite: 682]

# B4: Đóng gói tất cả giao dịch và tạo khối mới
new_block = my_blockchain.create_block(new_proof, previous_hash)  # [cite: 683, 684]

print(f"--- Đã tạo khối mới thành công! Hash: {new_block.hash[:10]}... ---")
print("\n--- HIỂN THỊ TOÀN BỘ BLOCKCHAIN ---")

# 4. Hiển thị thông tin chuỗi khối
for block in my_blockchain.chain:  # [cite: 687]
    print(f"Block #{block.index}")  # [cite: 689]
    print(f"Timestamp: {block.timestamp}")  # [cite: 691]
    print(f"Transactions: {block.transactions}")  # [cite: 693]
    print(f"Proof: {block.proof}")  # [cite: 695]
    print(f"Previous Hash: {block.previous_hash}")  # [cite: 697]
    print(f"Hash: {block.hash}")  # [cite: 699]
    print("-" * 30)  # [cite: 701, 703]

# 5. Kiểm tra tính toàn vẹn của chuỗi
print(
    f"Is Blockchain Valid: {my_blockchain.is_chain_valid(my_blockchain.chain)}"
)  # [cite: 705, 706]
