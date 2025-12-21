# Kịch Bản Thuyết Trình - Focus Thuật Toán (45 phút)

## Timeline

- PHẦN 1 (Intro): 3 phút
- PHẦN 2 (AES): 12 phút  
- PHẦN 3 (DES): 10 phút
- PHẦN 4 (RSA): 12 phút
- PHẦN 5 (3DES + Q&A): 8 phút

---

## PHẦN 1: MỞ ĐẦU (3 phút)

**Nội dung:**
- Giới thiệu project: 4 thuật toán mã hóa code từ đầu
- AES, DES, 3DES (symmetric), RSA (asymmetric)
- Toàn bộ 2,800+ dòng code, không dùng crypto library bên ngoài

**Slide:** 1 slide tóm tắt

---

## PHẦN 2: AES - ADVANCED ENCRYPTION STANDARD (12 phút)

### Giới thiệu (2 phút)
- Mã hóa khối (block cipher) hiện đại
- Block size: 16 bytes (128 bits)
- Key size: 128, 192, hoặc 256 bits
- Số vòng: 10 (AES-128), 12 (AES-192), 14 (AES-256)
- Chuẩn hiện đại, dùng rộng rãi (WiFi, HTTPS)

### Quá trình mã hóa chi tiết (8 phút)

**Bước 1: AddRoundKey (1 phút)**
```
State = plaintext XOR key_round_0
```
- XOR từng byte với byte tương ứng từ khóa
- Đây là bước khiến plaintext phụ thuộc vào key

**Bước 2-10: 9 Main Rounds (5 phút)**

Mỗi round gồm 4 bước:

1. SubBytes (1 phút):
   - Thay thế từng byte bằng giá trị từ S-box
   - S-box là 256 giá trị được xác định trước
   - Làm cho ciphertext không tuyến tính theo plaintext

2. ShiftRows (1 phút):
   - Xoay vòng các hàng của state matrix
   - Row 0: không xoay
   - Row 1: xoay 1 vị trí
   - Row 2: xoay 2 vị trí
   - Row 3: xoay 3 vị trí
   - Tạo sự phân tán (diffusion)

3. MixColumns (1 phút):
   - Trộn các cột lại với nhau
   - Mỗi cột được nhân với matrix cố định
   - Tạo sự diffusion theo cột

4. AddRoundKey (1 phút):
   - XOR lại với round key
   - Round key được sinh từ original key

**Bước 11: Final Round (2 phút)**
- Giống 9 main rounds nhưng **không có MixColumns**
- Lý do: Để làm cho ciphertext cuối cùng không cần MixColumns

### Code snippet (1 phút)
```python
def aes_encrypt_block(plaintext, key):
    state = plaintext  # 16 bytes
    state = add_round_key(state, round_keys[0])
    
    for round in range(10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round+1])
    
    return state
```

### Tại sao an toàn (1 phút)
- 10 vòng khiến plaintext được xáo trộn hoàn toàn
- Key diffusion: một bit key thay đổi → ciphertext thay đổi rất nhiều
- SubBytes không tuyến tính → không thể dự đoán

---

## PHẦN 3: DES - DATA ENCRYPTION STANDARD (10 phút)

### Giới thiệu (1 phút)
- Mã hóa khối cũ nhưng quan trọng cho học tập
- Block size: 8 bytes (64 bits)
- Key size: 56 bits (8 bytes, mỗi byte có 1 bit parity)
- Số vòng: 16
- Dùng Feistel network

### Cấu trúc Feistel (5 phút)

**Khác với AES:**
- Chia block thành 2 nửa: Left (32 bits), Right (32 bits)
- Mỗi vòng chỉ xử lý nửa Right
- Nửa kia giữ nguyên rồi swap

**Một vòng Feistel (mô tả chi tiết):**

1. **Mở rộng R** (1 phút):
   - 32 bits → 48 bits (E permutation)
   - Một số bit được lặp lại
   - Kết quả được gọi E(R)

2. **XOR với round key** (1 phút):
   - E(R) XOR K_round → 48 bits
   - K_round được sinh từ key gốc

3. **S-box substitution** (1 phút):
   - Chia 48 bits thành 8 nhóm 6 bits
   - Mỗi nhóm đi qua S-box riêng → 4 bits
   - Tổng: 8 × 4 = 32 bits
   - 8 S-boxes khác nhau

4. **Permutation P** (1 phút):
   - 32 bits được hoán vị theo bảng P
   - Tạo diffusion cho các bit

**Swap (1 phút):**
```
L' = R
R' = L XOR f(R, K)
```

### Giải mã (2 phút)
- Sử dụng **cùng quá trình encrypt**
- Nhưng với **subkeys theo thứ tự ngược**
- K16, K15, ..., K1 thay vì K1, K2, ..., K16

**Lý do:** Cấu trúc Feistel có tính chất tương hỗ

### Code concept (1 phút)
```python
def des_encrypt(plaintext, key):
    block = permute(plaintext, IP)  # Initial Permutation
    L = block >> 32
    R = block & 0xFFFFFFFF
    
    for round in range(16):
        L, R = R, L XOR f(R, round_keys[round])
    
    return permute((R << 32) | L, FP)  # Final Permutation
```

### Tại sao yếu hơn AES (1 phút)
- Key size chỉ 56 bits → brute force trong vài giờ
- 16 vòng (ít hơn AES 10 vòng) → mạnh kém hơn
- Đó là lý do có 3DES

---

## PHẦN 4: RSA - RIVEST-SHAMIR-ADLEMAN (12 phút)

### Giới thiệu (2 phút)
- Mã hóa công khai (asymmetric)
- Khác AES/DES: có 2 khóa riêng biệt
- Khóa công khai (e, n): chia sẻ công khai
- Khóa riêng (d, n): giữ bí mật
- An toàn dựa trên độ khó phân tích thừa số

### Quá trình sinh khóa (6 phút)

**Bước 1: Chọn 2 số nguyên tố (1 phút)**
- Chọn p, q là số nguyên tố lớn (512-1024 bits mỗi cái)
- Kiểm tra tính nguyên tố bằng Miller-Rabin test
- Ví dụ: p = 61, q = 53 (nhỏ để dễ hiểu)

**Bước 2: Tính n (1 phút)**
```
n = p × q = 61 × 53 = 3233
```
- n sẽ có kích thước khoảng 2×(bit của p, q)

**Bước 3: Tính φ(n) (1 phút)**
```
φ(n) = (p-1) × (q-1) = 60 × 52 = 3120
```
- φ là Euler's totient function
- Số lượng số nguyên tố cùng nhau với n

**Bước 4: Chọn e (1 phút)**
```
Điều kiện: 1 < e < φ(n), gcd(e, φ(n)) = 1
Ví dụ: e = 17
Kiểm tra: gcd(17, 3120) = 1 ✓
```
- Thường chọn e = 65537 (Fermat prime)
- Vừa có tính chất toán học, vừa dễ tính toán

**Bước 5: Tính d (extended Euclidean) (1 phút)**
```
Tìm d sao cho: e × d ≡ 1 (mod φ(n))
17 × d ≡ 1 (mod 3120)
Giải: d = 2753
Kiểm tra: 17 × 2753 = 46801 = 15 × 3120 + 1 ✓
```

**Kết quả:**
- Khóa công khai: (e=17, n=3233)
- Khóa riêng: (d=2753, n=3233)

### Mã hóa và Giải mã (2 phút)

**Mã hóa (công khai):**
```
C = M^e mod n = M^17 mod 3233
```

**Giải mã (bí mật):**
```
M = C^d mod n = C^2753 mod 3233
```

**Ví dụ:**
- Plaintext M = 123
- Ciphertext C = 123^17 mod 3233 = ?
- Decrypt: C^2753 mod 3233 = 123 ✓

### Tại sao an toàn (2 phút)

**Kẻ tấn công biết:**
- e = 17, n = 3233 (công khai)
- Biết quy luật: e × d ≡ 1 (mod φ(n))

**Nhưng không biết:**
- φ(n) = (p-1) × (q-1)
- p, q là hai số nguyên tố

**Để tính d cần:**
1. Phân tích n = p × q
2. Tính φ(n) = (p-1) × (q-1)
3. Tính d từ extended Euclidean

**Vấn đề:** Phân tích thừa số rất khó
- n = 3233 có thể phân tích bằng tay
- Nhưng n = p×q với p,q là số nguyên tố 1024-bit?
- Cần hàng tỷ năm tính toán với máy tính hiện đại!

---

## PHẦN 5: 3DES + Q&A (8 phút)

### 3DES - Triple DES (3 phút)

**Khái niệm:**
- DES quá yếu (56-bit key)
- Giải pháp: Áp dụng DES 3 lần
- Mode: EDE (Encrypt-Decrypt-Encrypt)

**Quá trình mã hóa:**
```
Plaintext
    ↓ DES Encrypt (K1)
    ↓ DES Decrypt (K2)
    ↓ DES Encrypt (K3)
Ciphertext
```

**Lợi ích:**
- Key size: 56×3 = 168 bits (khó brute force)
- Tương thích: Nếu K1=K2=K3 → DES bình thường
- Mạnh hơn: 3 vòng DES khiến ciphertext rất khó phá

**Lý do dùng D-E-D thay vì E-E-E:**
- Nếu E-E-E: (E-E-E với K1,K2,K3) = E với K_combined (có thể reduce)
- E-D-E: Không thể reduce → thực sự 168 bits

---

## Q&A Chuẩn Bị (5 phút)

**Q1: "Tại sao AES an toàn hơn DES?"**
- A: AES dùng 10-14 vòng (DES 16), nhưng:
  - SubBytes của AES không tuyến tính
  - Key size lớn hơn (128-256 vs 56)
  - Thiết kế hiện đại hơn (DES từ 1977)

**Q2: "3DES có an toàn bằng AES không?"**
- A: 3DES (168 bits) gần bằng AES-256 (256 bits)
  - Nhưng 3DES chậm hơn AES
  - Nên dùng AES cho ứng dụng mới
  - 3DES dùng để tương thích cũ

**Q3: "RSA hay AES hơn?"**
- A: Khác nhau:
  - AES: Mã hóa dữ liệu nhanh (symmetric)
  - RSA: Trao đổi khóa an toàn (asymmetric)
  - Thực tế: Dùng cả hai (RSA để trao đổi key AES)

**Q4: "Key size bao lâu cần tăng?"**
- A: Tùy độ khó phân tích:
  - 512-bit RSA: Đã phá được (2009)
  - 1024-bit RSA: Sắp phá (≈2030)
  - 2048-bit RSA: An toàn tới ≈2060
  - Nên dùng 2048+ cho long-term

**Q5: "Có thể dùng code này cho production?"**
- A: Không nên:
  - Này là học tập, không optimize
  - Crypto library đã audit kỹ lưỡng
  - Risk: Side-channel attacks, implementation bugs
  - Dùng cho demo, học tập: được!

---

## Gợi Ý Demo (nếu có thời gian)

Nếu còn thời gian, demo nhẹ:
1. Chạy chương trình: python main.py
2. Mã hóa file nhỏ với AES → Show ciphertext
3. Decrypt lại → Show plaintext giống hệt
4. Nhấn mạnh: "Round-trip test PASS"

---

## Cheat Sheet (để phía sau bàn)

AES: 10-14 rounds, SubBytes→ShiftRows→MixColumns→AddRoundKey
DES: 16 rounds, Feistel (L,R), E-permutation→S-box→P-permutation
3DES: DES 3 lần (E-D-E), 168-bit key
RSA: p×q→φ(n)→choose e→compute d, security from factorization

Total: 2,800+ code lines, 0 external crypto libs
Test: Round-trip encrypt/decrypt PASS
