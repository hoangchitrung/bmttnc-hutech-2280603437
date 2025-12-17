# Các thuật toán cho AES, DES, Triple DES, RSA
## 1. AES
### Ma trận trạng thái (State Matrix)
  - Luôn sử dụng ma trận 4x4
  - Mỗi ô trong ma trận chứa **1 byte** (8 bit, giá trị 0-255)
  - Dữ liệu được biểu diễn bằng hex từ 0-9 và sau đó A-F (để phù hợp với 16 bytes)
  - Dữ liệu được tổ chức theo cột, từ trên xuống dưới.

**Ví dụ**:
```markdown
┌──────────────────┐
│ 00  44  88  CC   │  ← Cột 1: [00,11,22,33]
│ 11  55  99  DD   │  ← Cột 2: [44,55,66,77]
│ 22  66  AA  EE   │  ← Cột 3: [88,99,AA,BB]
│ 33  77  BB  FF   │  ← Cột 4: [CC,DD,EE,FF]
└──────────────────┘
```
**Tại sao AES sắp xếp theo cột?**
- AES sử dụng các phép toán toán học **ShiftRows** và **MixColumns** để xử lý dữ liệu theo cột và hàng. **Nếu sắp xếp sai, kết quả tính toán sẽ bị lỗi** 

### Các phép toán của Ma trận trạng thái
**1. Chuyển bytes → Ma trận trạng thái:**
- Đầu vào: 16 bytes liên tiếp
- Tổ chức nó thành ma trận theo cột (từ trái sang phải, từ trên xuống dưới theo từng cột)
- Đầu ra: ma trận 4x4

**2. Chuyển Ma trận trạng thái → bytes**
- Đọc ma trận theo cột (từ trái sang phải, từ trên xuống dưới theo từng cột)
- Đầu ra: 16 bytes liên tiếp

**3. Ký hiệu**
- state[i][j] hoặc S$_i$,$_j$
  - i: hàng (0-3)
  - j: cột (0-3)

**4. Hàm**
- **Logic đơn giản**:
```text
Byte đầu vào: 0x95 (hex) = 149 (thập phân)
             ↓
Lấy hàng: 9 (chữ số thứ 1 của 0x95)
Lấy cột: 5 (chữ số thứ 2 của 0x95)
             ↓
S_box[9][5] = 0x2A (giá trị tra cứu từ bảng)
             ↓
Byte đầu ra: 0x2A
```
- **Khi áp dụng trong GUI**
```text
FILE (chữa dữ liệu)
      ↓
Đọc 16 bytes từ file
      ↓
Dữ liệu "bytes" (Là các kí tự nhưng biểu diễn ở dạng số thập phân 0-255, hoặc số hex 0x00-0xFF)
      ↓
create_state_matrix() ← Tạo ma trận 4x4 từ 16 bytes
      ↓
sub_bytes() ← Thay mỗi byte từ S_box
      ↓
state_matrix (sau khi thay thế)
```

**Cách đổi từ Bytes sang SubBytes**
- **0x00**:
  - Hàng: 0 (Số trước)
  - Cột: 0 (Số sau)
→ Vị trí S_Box[0][0] = 0x63
→ Kết quả SubBytes: 63

- **0x44**:
  - Hàng: 4 (Số trước)
  - Cột: 4 (Số sau)
→ Vị trí S_Box[4][4] = 0x1B
→ Kết quả SubBytes: 1B

- **0x11**:
  - Hàng: 1 (Số trước)
  - Cột: 1 (Số sau)
→ Vị trí S_Box[1][1] = 0x82
→ Kết quả SubBytes: 82

**Công thức tổng quát:**
- Hàng = Byte >> 4 hoặc Byte // 16
- Cột = Byte & 0x0F hoặc Byte % 16
- Kết quả: S_box[Hàng][Cột]

**Ví dụ:**

Đầu vào: 44 (thập phân)

↓

Tạo ma trận trạng thái

↓

Hiển thị ma trận: 0x2C (vì 44 / 16 = 2, 44 % 16 = 12, 12 trong hex là C ⇒ 2C)

↓

SubBytes

- Hàng = 44 // 16 = 2
- Cột = 44 % 16 = 12
- S_box[2][12] = 0x71
       ↓
- Đầu ra: 0x71

**Vì sao chia cho 16?**
- Vì hex có 16 ký tự (0-9, A-F),
- S_box là bảng 16×16