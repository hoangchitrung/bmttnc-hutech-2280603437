class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I")  # Chuyển "J" thành "I" trong khóa
        key = key.upper()
        key_set = set()
        matrix = []
        
        # Thêm các ký tự từ key vào ma trận
        for char in key:
            if char not in key_set and char.isalpha():
                matrix.append(char)
                key_set.add(char)
        
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        
        # Thêm các ký tự còn lại từ bảng chữ cái
        for char in alphabet:
            if char not in key_set:
                matrix.append(char)
                
        # Chuyển thành ma trận 5x5
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper()
        encrypted_text = ""
        
        # Xử lý văn bản thành các cặp ký tự
        i = 0
        while i < len(plain_text):
            char1 = plain_text[i]
            if i + 1 < len(plain_text):
                char2 = plain_text[i+1]
                if char1 == char2:
                    char2 = "X"
                    i += 1
                else:
                    i += 2
            else:
                char2 = "X"
                i += 1
            
            row1, col1 = self.find_letter_coords(matrix, char1)
            row2, col2 = self.find_letter_coords(matrix, char2)
            
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
                
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypted_text = ""
        
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        # Xử lý loại bỏ ký tự 'X' được thêm vào (Logic theo tài liệu)
        banro = ""
        for i in range(0, len(decrypted_text)-2, 2):
            if decrypted_text[i] == decrypted_text[i+2]: # Logic phát hiện ký tự trùng lặp gốc
                banro += decrypted_text[i]
            else:
                banro += decrypted_text[i] + "" + decrypted_text[i+1]
        
        if len(decrypted_text) > 2:
             if decrypted_text[-1] == "X":
                banro += decrypted_text[-2]
             else:
                banro += decrypted_text[-2] + decrypted_text[-1]
        else: # Trường hợp chuỗi ngắn
             banro = decrypted_text

        return banro