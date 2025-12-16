import sys
from PIL import Image


def encode_image(image_path, message):
    # Mở ảnh gốc
    img = Image.open(image_path)  # [cite: 775]
    width, height = img.size  # [cite: 776]

    # Chuyển tin nhắn sang dạng nhị phân (8 bit cho mỗi ký tự)
    # Ví dụ: 'A' -> '01000001'
    binary_message = "".join(
        format(ord(char), "08b") for char in message
    )  # [cite: 778]

    # Thêm chuỗi đánh dấu kết thúc (delimiter) để lúc giải mã biết đâu là điểm dừng
    # Chuỗi này là 16 bit: 1111111111111110
    binary_message += "1111111111111110"  # [cite: 778]

    data_index = 0
    total_pixels = width * height

    # Duyệt qua từng pixel của ảnh
    for row in range(height):  # [cite: 785]
        for col in range(width):  # [cite: 799]
            # Lấy giá trị màu RGB của pixel hiện tại (VD: (100, 200, 50))
            pixel = list(img.getpixel((col, row)))  # [cite: 800]

            # Duyệt qua 3 kênh màu: R, G, B
            for color_channel in range(3):  # [cite: 801]
                if data_index < len(binary_message):
                    # Kỹ thuật LSB: Thay thế bit cuối cùng của màu bằng bit của tin nhắn
                    # pixel[channel] & ~1: Xóa bit cuối (về 0)
                    # | int(...): Cộng với bit tin nhắn (0 hoặc 1)
                    # Đoạn code trong PDF dùng format string, logic tương tự:
                    pixel[color_channel] = int(
                        format(pixel[color_channel], "08b")[:-1]
                        + binary_message[data_index],
                        2,
                    )  # [cite: 803]
                    data_index += 1

            # Cập nhật pixel mới vào ảnh
            img.putpixel((col, row), tuple(pixel))  # [cite: 806]

            # Nếu đã giấu hết tin nhắn thì thoát vòng lặp
            if data_index >= len(binary_message):  # [cite: 807]
                break
        if data_index >= len(binary_message):
            break

    # Lưu ảnh mới dưới dạng PNG (Quan trọng: PNG nén không mất dữ liệu, JPG sẽ làm hỏng bit giấu)
    encoded_image_path = "encoded_image.png"  # [cite: 812]
    img.save(encoded_image_path)  # [cite: 813]
    print(
        "Steganography complete. Encoded image saved as", encoded_image_path
    )  # [cite: 814]


def main():
    # Kiểm tra tham số dòng lệnh
    if len(sys.argv) != 3:  # [cite: 825]
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]  # [cite: 827]
    message = sys.argv[2]  # [cite: 828]
    encode_image(image_path, message)  # [cite: 829]


if __name__ == "__main__":  # [cite: 830]
    main()
