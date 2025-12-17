S_box = [
    [
        0x63,
        0x7C,
        0x77,
        0x7B,
        0xF2,
        0x6B,
        0x6F,
        0xC5,
        0x30,
        0x01,
        0x67,
        0x2B,
        0xFE,
        0xD7,
        0xAB,
        0x76,
    ],
    [
        0xCA,
        0x82,
        0xC9,
        0x7D,
        0xFA,
        0x59,
        0x47,
        0xF0,
        0xAD,
        0xD4,
        0xA2,
        0xAF,
        0x9C,
        0xA4,
        0x72,
        0xC0,
    ],
    [
        0xB7,
        0xFD,
        0x93,
        0x26,
        0x36,
        0x3F,
        0xF7,
        0xCC,
        0x34,
        0xA5,
        0xE5,
        0xF1,
        0x71,
        0xD8,
        0x31,
        0x15,
    ],
    [
        0x04,
        0xC7,
        0x23,
        0xC3,
        0x18,
        0x96,
        0x05,
        0x9A,
        0x07,
        0x12,
        0x80,
        0xE2,
        0xEB,
        0x27,
        0xB2,
        0x75,
    ],
    [
        0x09,
        0x83,
        0x2C,
        0x1A,
        0x1B,
        0x6E,
        0x5A,
        0xA0,
        0x52,
        0x3B,
        0xD6,
        0xB3,
        0x29,
        0xE3,
        0x2F,
        0x84,
    ],
    [
        0x53,
        0xD1,
        0x00,
        0xED,
        0x20,
        0xFC,
        0xB1,
        0x5B,
        0x6A,
        0xCB,
        0xBE,
        0x39,
        0x4A,
        0x4C,
        0x58,
        0xCF,
    ],
    [
        0xD0,
        0xEF,
        0xAA,
        0xFB,
        0x43,
        0x4D,
        0x33,
        0x85,
        0x45,
        0xF9,
        0x02,
        0x7F,
        0x50,
        0x3C,
        0x9F,
        0xA8,
    ],
    [
        0x51,
        0xA3,
        0x40,
        0x8F,
        0x92,
        0x9D,
        0x38,
        0xF5,
        0xBC,
        0xB6,
        0xDA,
        0x21,
        0x10,
        0xFF,
        0xF3,
        0xD2,
    ],
    [
        0xCD,
        0x0C,
        0x13,
        0xEC,
        0x5F,
        0x97,
        0x44,
        0x17,
        0xC4,
        0xA7,
        0x7E,
        0x3D,
        0x64,
        0x5D,
        0x19,
        0x73,
    ],
    [
        0x60,
        0x81,
        0x4F,
        0xDC,
        0x22,
        0x2A,
        0x90,
        0x88,
        0x46,
        0xEE,
        0xB8,
        0x14,
        0xDE,
        0x5E,
        0x0B,
        0xDB,
    ],
    [
        0xE0,
        0x32,
        0x3A,
        0x0A,
        0x49,
        0x06,
        0x24,
        0x5B,
        0xC2,
        0x2E,
        0x8E,
        0xB8,
        0xB4,
        0xB7,
        0xF1,
        0x70,
    ],
    [
        0x75,
        0x71,
        0x72,
        0x5F,
        0x68,
        0x69,
        0x6A,
        0x6B,
        0x6C,
        0x6D,
        0x6E,
        0x6F,
        0x70,
        0x71,
        0x72,
        0x73,
    ],
    [
        0x74,
        0x75,
        0x76,
        0x77,
        0x78,
        0x79,
        0x7A,
        0x7B,
        0x7C,
        0x7D,
        0x7E,
        0x7F,
        0x80,
        0x81,
        0x82,
        0x83,
    ],
    [
        0x84,
        0x85,
        0x86,
        0x87,
        0x88,
        0x89,
        0x8A,
        0x8B,
        0x8C,
        0x8D,
        0x8E,
        0x8F,
        0x90,
        0x91,
        0x92,
        0x93,
    ],
    [
        0x94,
        0x95,
        0x96,
        0x97,
        0x98,
        0x99,
        0x9A,
        0x9B,
        0x9C,
        0x9D,
        0x9E,
        0x9F,
        0xA0,
        0xA1,
        0xA2,
        0xA3,
    ],
    [
        0xA4,
        0xA5,
        0xA6,
        0xA7,
        0xA8,
        0xA9,
        0xAA,
        0xAB,
        0xAC,
        0xAD,
        0xAE,
        0xAF,
        0xB0,
        0xB1,
        0xB2,
        0xB3,
    ],
]


def sub_bytes(state):
    """
    Replace every byte in state with value from S_box

    Input: Ma trận 4x4
    Output: Ma trận 4x4 sau khi thay thế
    """
    for i in range(4):
        for j in range(4):
            byte_value = state[i][j]
            # Lấy hàng (chữ số cao - high nibble)
            row = byte_value >> 4  # Hoặc: byte_value // 16
            # Lấy cột (chữ số thấp - low nibble)
            col = byte_value & 0x0F  # Hoặc: byte_value % 16
            # Tra cứu S_box
            state[i][j] = S_box[row][col]

    return state


def create_state_matrix(input_bytes):
    """
    Convert 16 bytes into 4x4 matrix
    Input: 16 bytes from file
    Example [0x00, 0x11, 0x22, ...]
    Output: Matrix 4x4 nested list
    """
    state = [[0 for _ in range(4)] for _ in range(4)]

    for i in range(16):
        # Row: 0,1,2,3,0,1,2,3
        row = i % 4
        # Col: 0,0,0,0,1,1,1,1
        col = i // 4

        state[row][col] = input_bytes[i]

    return state


def state_matrix_to_bytes(state):
    """
    Convert 4x4 matrix back to 16 bytes

    Input: Ma trận 4x4
    Output: 16 bytes (list)
    """
    result = []

    for col in range(4):
        for row in range(4):
            result.append(state[row][col])

    return result


# ✅ Test với dữ liệu
if __name__ == "__main__":
    # Ví dụ: Dữ liệu từ file
    test_bytes = [
        0x00,
        0x11,
        0x22,
        0x33,
        44,
        55,
        0x66,
        0x77,
        0x88,
        0x99,
        0xAA,
        0xBB,
        0xCC,
        0xDD,
        0xEE,
        0xFF,
    ]

    # Tạo ma trận
    state = create_state_matrix(test_bytes)
    print("State Matrix (trước SubBytes):")
    for row in state:
        print([f"{byte:02X}" for byte in row])

    # Áp dụng SubBytes
    state = sub_bytes(state)
    print("\nState Matrix (sau SubBytes):")
    for row in state:
        print([f"{byte:02X}" for byte in row])

    # Chuyển lại thành bytes
    output = state_matrix_to_bytes(state)
    print("\nOutput bytes:")
    print([f"{byte:02X}" for byte in output])
