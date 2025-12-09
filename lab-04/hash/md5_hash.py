import math

# Hàm xoay trái bit (Left Rotate)
def left_rotate(value, shift):
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def md5(message):
    # Khởi tạo các biến ban đầu (Magic numbers)
    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    # Tiền xử lý chuỗi văn bản
    original_length = len(message) * 8
    message += b'\x80'
    
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
        
    message += original_length.to_bytes(8, 'little')

    # Chia chuỗi thành các block 512-bit (64 bytes)
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        words = [int.from_bytes(block[j:j+4], 'little') for j in range(0, 64, 4)]

        a0, b0, c0, d0 = a, b, c, d

        # Vòng lặp chính của thuật toán MD5
        for j in range(64):
            if j < 16:
                f = (b & c) | ((~b) & d)
                g = j
            elif j < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * j + 1) % 16
            elif j < 48:
                f = b ^ c ^ d
                g = (3 * j + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * j) % 16

            # Các hằng số cho thuật toán (thường được fix cứng)
            # Đoạn này trong ảnh không hiển thị hết bảng K, 
            # nhưng logic chuẩn MD5 sử dụng sin:
            k_value = math.floor(2**32 * abs(math.sin(j + 1))) 
            
            # Mảng s (shift amounts) chuẩn của MD5
            s = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
            
            temp = d
            d = c
            c = b
            b = (b + left_rotate((a + f + k_value + words[g]) & 0xFFFFFFFF, s[j])) & 0xFFFFFFFF
            a = temp

        a = (a + a0) & 0xFFFFFFFF
        b = (b + b0) & 0xFFFFFFFF
        c = (c + c0) & 0xFFFFFFFF
        d = (d + d0) & 0xFFFFFFFF

    # Trả về kết quả dạng Hex
    return '{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d)

# Chạy chương trình
if __name__ == "__main__":
    input_string = input("Nhập chuỗi cần băm: ")
    md5_hash = md5(input_string.encode('utf-8'))
    print("Mã băm MD5 của chuỗi '{}' là: {}".format(input_string, md5_hash))