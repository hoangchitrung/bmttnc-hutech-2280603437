from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
app = Flask(__name__)

# Caesar cipher algorithm
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypted_text(cipher_text, key)
    return jsonify({'decrypted_message' : decrypted_text})

# Vigenere Cipher
from cipher.vigenere import VigenereCipher
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    encryped_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encrypted_message': encryped_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    encrypted_text = data['cipher_text']
    key = data['key']
    decrypted_text = vigenere_cipher.vigenere_decrypt(encrypted_text, key)
    return jsonify({'decrypted_message': decrypted_text})

# rail fence cipher
from cipher.railfence import RailFenceCipher
railfence_cipher = RailFenceCipher()

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = railfence_cipher.railfence_encrypt(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = railfence_cipher.railfence_decrypt(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})

# main fucntion
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)