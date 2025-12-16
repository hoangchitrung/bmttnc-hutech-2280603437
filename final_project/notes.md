# Algorithms for AES, DES, Triple DES, RSA
## 1. AES
### State Matrix
  - Always use 4x4 matrix
  - Every cells in matrix contain **1 byte** (8 bit, value 0-255)
  - Data visual by hex from 0-9 and then A-F (to fit 16 bytes)
  - Data is organized by columns. from top to bottom.

**Example**:
```markdown
┌──────────────────┐
│ 00  44  88  CC   │  ← Cột 1: [00,11,22,33]
│ 11  55  99  DD   │  ← Cột 2: [44,55,66,77]
│ 22  66  AA  EE   │  ← Cột 3: [88,99,AA,BB]
│ 33  77  BB  FF   │  ← Cột 4: [CC,DD,EE,FF]
└──────────────────┘
```
**Why AES order by column?**
- AES using mathematical operations **ShiftRows** and **MixColumns** to process data follow by columns and rows. **If the order is incorrect, the calculations will be fail** 

### State Matrix Operations
**1. Convert bytes → State Matrix:**
- Input: 16 bytes repeatedly
- Organize it into matrix by column (from left to right, top to bottom per columns)
- Output: 4x4 matrix

**2. Convert State Matrix → bytes**
- Read the matrix by columns (from the left to right, top to bottom per columns)
- Output: 16 bytes repeatedly

**3. Symbols**
- state[i][j] or S$_i$,$_j$
  - i: rows (0-3)
  - j: cols (0-3)

**4. Functions**
- Logic:
```text
Input byte: 0x95 (hex) = 149 (decimal)
             ↓
Lấy hàng: 9 (chữ số thứ 1 của 0x95)
Lấy cột: 5 (chữ số thứ 2 của 0x95)
             ↓
S_box[9][5] = 0x2A (giá trị tra cứu từ bảng)
             ↓
Output byte: 0x2A
```