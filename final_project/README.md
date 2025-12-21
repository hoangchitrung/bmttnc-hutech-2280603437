# Ứng Dụng Mã Hóa File GUI - Thuật Toán

## Tóm Tắt

Ứng dụng Desktop cho phép mã hóa/giải mã file sử dụng 4 thuật toán mã hóa được code từ đầu:
- AES (Advanced Encryption Standard)
- DES (Data Encryption Standard)
- 3DES (Triple DES)
- RSA (Rivest-Shamir-Adleman)

---

## Chi Tiết Các Thuật Toán

### AES (Advanced Encryption Standard)

**Nguyên lý:**
- Mã hóa khối (block cipher), block size 16 bytes
- Hỗ trợ độ dài khóa: 128, 192, hoặc 256 bits
- Số vòng: 10 (AES-128), 12 (AES-192), 14 (AES-256)
- Chuẩn hiện đại, được sử dụng rộng rãi (WiFi, HTTPS, etc)

**Quá trình mã hóa:**
1. AddRoundKey: XOR plaintext với khóa
2. 9/11/13 vòng (9 cho AES-128):
   - SubBytes: Thay thế byte bằng S-box
   - ShiftRows: Xoay vòng các hàng
   - MixColumns: Trộn các cột
   - AddRoundKey: XOR với round key
3. Vòng cuối cùng (không MixColumns):
   - SubBytes
   - ShiftRows
   - AddRoundKey

**Chi tiết cài đặt:**
- Code: 1,183 dòng
- S-box chuẩn: 256 giá trị
- Key expansion: Từ khóa gốc tạo 11 khóa vòng
- Tất cả xử lý byte-level

### DES (Data Encryption Standard)

**Nguyên lý:**
- Mã hóa khối, block size 8 bytes
- Độ dài khóa: 56 bits (8 bytes, mỗi byte có 1 bit parity)
- Sử dụng Feistel network, 16 vòng
- Chuẩn cũ nhưng quan trọng cho học tập

**Cấu trúc Feistel (mỗi vòng):**
- Chia block thành 2 nửa: Left (32 bits), Right (32 bits)
- Mở rộng Right từ 32 → 48 bits (E permutation)
- XOR với round key (48 bits)
- Đi qua 8 S-boxes → 32 bits
- Permutation P (32 bits)
- XOR với Left
- Swap: Left' = Right, Right' = Left XOR f(Right)

**Giải mã:**
- Sử dụng cùng quá trình nhưng subkeys theo thứ tự ngược lại

**Chi tiết cài đặt:**
- Code: 500 dòng
- 8 S-boxes riêng biệt
- Permutation tables: IP, FP, E, P, PC1, PC2
- Key schedule tạo 16 subkeys

### 3DES (Triple DES)

**Nguyên lý:**
- Áp dụng DES ba lần: Encrypt → Decrypt → Encrypt (EDE mode)
- Sử dụng 3 khóa độc lập (mỗi khóa 56 bits, tổng 168 bits)
- Mạnh hơn DES đơn lẻ, tương thích ngược

**Quá trình mã hóa:**
```
Plaintext
    ↓ DES Encrypt (Key 1)
Temp1
    ↓ DES Decrypt (Key 2)
Temp2
    ↓ DES Encrypt (Key 3)
Ciphertext
```

**Giải mã (quá trình ngược):**
```
Ciphertext
    ↓ DES Decrypt (Key 3)
Temp1
    ↓ DES Encrypt (Key 2)
Temp2
    ↓ DES Decrypt (Key 1)
Plaintext
```

**Lợi ích:**
- 168 bits key khó bị brute force hơn 56 bits
- Tương thích với DES nếu K1 = K2 = K3

**Chi tiết cài đặt:**
- Code: 109 dòng
- Tận dụng DES 3 lần
- Hỗ trợ 3 khóa độc lập

### RSA (Rivest-Shamir-Adleman)

**Nguyên lý:**
- Mã hóa công khai (asymmetric)
- Khóa công khai (e, n), khóa riêng (d, n)
- An toàn dựa trên độ khó phân tích n = p × q

**Quá trình sinh khóa:**
1. Chọn 2 số nguyên tố lớn p, q (kiểm tra bằng Miller-Rabin)
2. Tính n = p × q
3. Tính φ(n) = (p-1) × (q-1)
4. Chọn e: 1 < e < φ(n), gcd(e, φ(n)) = 1
   - Thường e = 65537 (Fermat prime)
5. Tính d bằng extended Euclidean algorithm:
   - d × e ≡ 1 (mod φ(n))

**Mã hóa:**
```
Ciphertext = Plaintext^e mod n
```

**Giải mã:**
```
Plaintext = Ciphertext^d mod n
```

**Tại sao an toàn:**
- e và n công khai, nhưng tính d cần biết p và q
- Phân tích n = p × q rất khó khi p, q là số nguyên tố lớn
- Độ khó tăng theo kích thước bit (512, 1024, 2048 bits)

**Chi tiết cài đặt:**
- Code: 349 dòng
- Miller-Rabin: Kiểm tra tính nguyên tố
- Extended Euclidean: Tính d từ e
- Modular exponentiation: Tính M^e mod n hiệu quả
- Key storage: JSON format

---

## So Sánh Thuật Toán

| Thuật Toán | Type       | Key Size      | Block Size | Vòng  | Cài Đặt    |
| ---------- | ---------- | ------------- | ---------- | ----- | ---------- |
| AES        | Symmetric  | 128-256 bits  | 16 bytes   | 10-14 | 1,183 dòng |
| DES        | Symmetric  | 56 bits       | 8 bytes    | 16    | 500 dòng   |
| 3DES       | Symmetric  | 168 bits      | 8 bytes    | 48    | 109 dòng   |
| RSA        | Asymmetric | 512-4096 bits | Variable   | N/A   | 349 dòng   |

---

## Xử Lý File

**Chế độ Block:**
- AES: 16-byte blocks
- DES/3DES: 8-byte blocks
- RSA: Integer blocks (bit-dependent)

**Padding:**
- Nếu block cuối < block size → thêm null bytes
- Khi decrypt: xóa padding ở cuối

**Binary I/O:**
- Mở file mode 'rb' (read binary), 'wb' (write binary)
- Hỗ trợ mọi loại file: txt, pdf, jpg, mp3, doc, etc

---

## Verification

**Round-Trip Test:**
```
plaintext → encrypt(key) → ciphertext
ciphertext → decrypt(key) → plaintext (giống hệt)
```

**Không dùng external crypto libraries:**
- Kiểm tra: grep -r "pycryptodome|cryptography|python-rsa"
- Kết quả: Không tìm thấy

---

## Tổng Thống Kê

- Tổng code thuật toán: ~2,800 dòng
- Áp dụng từ đầu: 4 thuật toán
- Thư viện Python: random, math, json
- GUI Framework: PyQt5
- External crypto libs: 0

---

Trường: HUTECH
Ngày: 21/12/2025
