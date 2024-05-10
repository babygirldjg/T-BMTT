import tkinter as tk
from tkinter import ttk

def toLowerCase(text):
    return text.lower()

def removeSpaces(text):
    return ''.join(text.split())

def Diagraph(text):
    diagraph = []
    group = 0
    for i in range(2, len(text), 2):
        diagraph.append(text[group:i])
        group = i
    diagraph.append(text[group:])
    return diagraph

def FillerLetter(text):
    k = len(text)
    if k % 2 == 0:
        for i in range(0, k, 2):
            if text[i] == text[i + 1]:
                text = text[:i + 1] + 'x' + text[i + 1:]
                text = FillerLetter(text)
                break
    else:
        text += 'x'  # Thêm một ký tự 'z' vào cuối nếu độ dài là số lẻ
        for i in range(0, k, 2):
            if text[i] == text[i + 1]:
                text = text[:i + 1] + 'x' + text[i + 1:]
                text = FillerLetter(text)
                break
    return text


def generateKeyTable(word, list1):
    # Tạo ma trận khóa từ từ khóa
    key_letters = []
    for char in word:
        if char not in key_letters and char in list1:  # Chỉ thêm các ký tự không trùng lặp từ từ khóa
            key_letters.append(char)
    
    # Thêm các ký tự còn thiếu từ danh sách list1
    for char in list1:
        if char not in key_letters:
            key_letters.append(char)

    # Xây dựng ma trận khóa từ danh sách các ký tự đã tạo
    matrix = []
    while key_letters:
        matrix.append(key_letters[:5])
        key_letters = key_letters[5:]

    return matrix



def search(mat, element):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == element:
                return i, j

def encrypt_RowRule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[e1r][0] if e1c == 4 else matr[e1r][e1c + 1]
    char2 = matr[e2r][0] if e2c == 4 else matr[e2r][e2c + 1]
    return char1, char2

def encrypt_ColumnRule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[0][e1c] if e1r == 4 else matr[e1r + 1][e1c]
    char2 = matr[0][e2c] if e2r == 4 else matr[e2r + 1][e2c]
    return char1, char2

def encrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[e1r][e2c]
    char2 = matr[e2r][e1c]
    return char1, char2


def encryptByPlayfairCipher(Matrix, plainList):
    CipherText = []
    for i in range(len(plainList)):
        c1, c2 = '', ''
        ele1_x, ele1_y = search(Matrix, plainList[i][0])
        ele2_x, ele2_y = search(Matrix, plainList[i][1])

        if ele1_x == ele2_x:
            c1, c2 = encrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        elif ele1_y == ele2_y:
            c1, c2 = encrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else:
            c1, c2 = encrypt_RectangleRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

        cipher = c1 + c2
        CipherText.append(cipher)
    return CipherText

def decryptByPlayfairCipher(Matrix, cipherList):
    plaintextList = []
    for cipher in cipherList:
        ele1_x, ele1_y = search(Matrix, cipher[0])
        ele2_x, ele2_y = search(Matrix, cipher[1])

        if ele1_x == ele2_x:
            char1, char2 = decrypt_RowRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        elif ele1_y == ele2_y:
            char1, char2 = decrypt_ColumnRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else:
            char1, char2 = decrypt_RectangleRule(Matrix, ele1_x, ele1_y, ele2_x, ele2_y)

        plaintextList.append(char1 + char2)

    return plaintextList

def decrypt_RowRule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[e1r][-1] if e1c == 0 else matr[e1r][e1c - 1]
    char2 = matr[e2r][-1] if e2c == 0 else matr[e2r][e2c - 1]
    return char1, char2

def decrypt_ColumnRule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[-1][e1c] if e1r == 0 else matr[e1r - 1][e1c]
    char2 = matr[-1][e2c] if e2r == 0 else matr[e2r - 1][e2c]
    return char1, char2

def decrypt_RectangleRule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[e1r][e2c]
    char2 = matr[e2r][e1c]
    return char1, char2

def encrypt_playfair():
    key = key_entry.get()
    plaintext = plaintext_entry.get()

    key = toLowerCase(key)
    list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    Matrix = generateKeyTable(key, list1)

    plaintext = removeSpaces(toLowerCase(plaintext))
    plaintext_list = Diagraph(FillerLetter(plaintext))
    if len(plaintext_list[-1]) != 2:
        plaintext_list[-1] = plaintext_list[-1] + 'z'

    cipher_list = encryptByPlayfairCipher(Matrix, plaintext_list)
    ciphertext = ''.join(cipher_list)

    result_label.config(text=f"Ciphertext: {ciphertext}")

def decrypt_playfair():
    key = key_entry.get()
    ciphertext = plaintext_entry.get()

    key = toLowerCase(key)
    list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    Matrix = generateKeyTable(key, list1)

    ciphertext = removeSpaces(toLowerCase(ciphertext))
    ciphertext_list = Diagraph(ciphertext)

    plaintext_list = decryptByPlayfairCipher(Matrix, ciphertext_list)
    plaintext = ''.join(plaintext_list)

    result_label.config(text=f"Plaintext: {plaintext}")

root = tk.Tk()
root.title("Playfair Cipher Encoder/Decoder")

frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

key_label = ttk.Label(frame, text="Key:")
key_label.grid(column=0, row=0, sticky=tk.W)

key_entry = ttk.Entry(frame, width=30)
key_entry.grid(column=1, row=0, sticky=tk.W)

plaintext_label = ttk.Label(frame, text="Text:")
plaintext_label.grid(column=0, row=1, sticky=tk.W)

plaintext_entry = ttk.Entry(frame, width=30)
plaintext_entry.grid(column=1, row=1, sticky=tk.W)

encrypt_button = ttk.Button(frame, text="Encrypt", command=encrypt_playfair)
encrypt_button.grid(column=1, row=2, sticky=tk.W)

decrypt_button = ttk.Button(frame, text="Decrypt", command=decrypt_playfair)
decrypt_button.grid(column=1, row=3, sticky=tk.W)

result_label = ttk.Label(frame, text="")
result_label.grid(column=0, row=4, columnspan=2, sticky=tk.W)

root.mainloop()
