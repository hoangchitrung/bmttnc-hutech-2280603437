import sys
from PIL import Image


def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)  # [cite: 840]
    width, height = img.size  # [cite: 844]

    binary_message = ""

    # Duyệt qua từng pixel để lấy lại các bit đã giấu
    for row in range(height):  # [cite: 849]
        for col in range(width):  # [cite: 850]
            pixel = img.getpixel((col, row))  # [cite: 851]

            for color_channel in range(3):  # [cite: 852]
                # Lấy bit cuối cùng của từng kênh màu
                binary_message += format(pixel[color_channel], "08b")[-1]  # [cite: 853]

    # Chuyển đổi nhị phân về lại văn bản
    message = ""
    # Chuỗi đánh dấu kết thúc (Delimiter)
    delimiter = "1111111111111110"

    # Cắt chuỗi nhị phân theo từng byte (8 bit)
    for i in range(0, len(binary_message), 8):  # [cite: 872]
        byte = binary_message[i : i + 8]

        # Kiểm tra xem có gặp chuỗi kết thúc chưa (ở đây logic PDF hơi khác thực tế một chút)
        # Để code chạy tốt, ta kiểm tra đoạn 16 bit sắp tới có phải delimiter không
        if binary_message[i : i + 16] == delimiter:
            break

        # Chuyển 8 bit thành ký tự
        if len(byte) == 8:
            char = chr(int(byte, 2))  # [cite: 873]
            message += char  # [cite: 876]

    return message


def main():
    if len(sys.argv) != 2:  # [cite: 878]
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]  # [cite: 880]

    decoded_message = decode_image(encoded_image_path)  # [cite: 894]
    print("Decoded message:", decoded_message)  # [cite: 895]


if __name__ == "__main__":  # [cite: 890]
    main()
