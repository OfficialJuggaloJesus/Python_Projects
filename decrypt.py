def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    key_length = len(key)
    for i, c in enumerate(ciphertext):
        if 'A' <= c <= 'Z':
            shift = ord(key[i % key_length]) - ord('A')
            decrypted_char = chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(c)
    return ''.join(decrypted_text)

# Ciphertext from Kryptos Section 4
ciphertext = "NGHIJLMNQUVWXZKRYPTOSABCDEFGHIJLOHIJLMNQUVWXZKRYPTOSABCDEFGHIJLPIJLMNQUVWXZKRYPTOSABCDEFGHIJLMQJLMNQUVWXZKRYPTOSABCDEFGHIJLMNRLMNQUVWXZKRYPTOSABCDEFGHIJLMNQSMNQUVWXZKRYPTOSABCDEFGHIJLMNQUTNQUVWXZKRYPTOSABCDEFGHIJLMNQUVUQUVWXZKRYPTOSABCDEFGHIJLMNQUVWVUVWXZKRYPTOSABCDEFGHIJLMNQUVWXWVWXZKRYPTOSABCDEFGHIJLMNQUVWXZXWXZKRYPTOSABCDEFGHIJLMNQUVWXZKYXZKRYPTOSABCDEFGHIJLMNQUVWXZKRZZKRYPTOSABCDEFGHIJLMNQUVWXZKRYABCDEFGHIJKLMNOPQRSTUVWXYZABCD"

# List of keys to try
keys = [
    "eastberlinclocknorth",
    "clockeastnorthberlin",
    "berlineastnorthclock",
    "eastnortheastberlinclock",
    "berlineastnorthclockeastnorth",
    "northclockberlineast",
    "eastberlinnorthclock",
    "eastberlinclocknorth",
]

# Decrypt using each key and print the result
for key in keys:
    decrypted_message = vigenere_decrypt(ciphertext, key)
    print(f"Key: {key}")
    print(f"Decrypted Message:")
    print(decrypted_message)
    print("-" * 50)
