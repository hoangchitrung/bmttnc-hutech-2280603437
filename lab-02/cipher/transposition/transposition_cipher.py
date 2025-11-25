class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        encrypted_text = ""
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text

    def decrypt(self, text, key):
        numOfColumns = int(len(text) / key)
        if len(text) % key > 0:
            numOfColumns += 1
        
        numOfRows = key
        numOfShadedBoxes = (numOfColumns * numOfRows) - len(text)
        
        decrypted_text = [''] * numOfColumns
        col = 0
        row = 0
        
        for symbol in text:
            decrypted_text[col] += symbol
            col += 1
            
            if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
                col = 0
                row += 1
                
        return ''.join(decrypted_text)