# Function to decrypt using Vigenère cipher
def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key_length = len(key)
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % key_length].upper()) - ord('A')
            if char.isupper():
                plaintext += chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            elif char.islower():
                plaintext += chr((ord(char) - shift - ord('a')) % 26 + ord('a'))
            key_index += 1
        else:
            plaintext += char
    
    return plaintext

# Ciphertext from part four of Kryptos
ciphertext_part4 = "NGHIJLMNQUVWXZKRYPTOSABCDEFGHIJLOHIJLMNQUVWXZKRYPTOSABCDEFGHIJLPIJLMNQUVWXZKRYPTOSABCDEFGHIJLMQJLMNQUVWXZKRYPTOSABCDEFGHIJLMNRLMNQUVWXZKRYPTOSABCDEFGHIJLMNQSMNQUVWXZKRYPTOSABCDEFGHIJLMNQUTNQUVWXZKRYPTOSABCDEFGHIJLMNQUVUQUVWXZKRYPTOSABCDEFGHIJLMNQUVWVUVWXZKRYPTOSABCDEFGHIJLMNQUVWXWVWXZKRYPTOSABCDEFGHIJLMNQUVWXZXWXZKRYPTOSABCDEFGHIJLMNQUVWXZKYXZKRYPTOSABCDEFGHIJLMNQUVWXZKRZZKRYPTOSABCDEFGHIJLMNQUVWXZKRYABCDEFGHIJKLMNOPQRSTUVWXYZABCD"

# Key inferred from patterns (KRYPTOS as a potential key)
key = "KryptosPartfourisincode"

# Decrypt using Vigenère cipher
decrypted_text = vigenere_decrypt(ciphertext_part4, key)

# Print decrypted text
print("Decrypted Text:", decrypted_text)
