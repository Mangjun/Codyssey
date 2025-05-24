TARGET_FILE = './password.txt'
RESULT_FILE = './result.txt'
DICT_FILE = './text_dict.txt'

CHARSET = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
SEPARATOR = ' '
ENCODING = 'utf-8'

def caesar_cipher_decode(target_text, shift):
    decoded_text = ''
    upper = False
    for char in target_text:
        if char.isalpha():
            if char.isupper():
                upper = True
                char = char.lower()
            index = CHARSET.index(char)
            if upper:
                decoded_text += CHARSET[index + shift].upper()
                upper = False
            else:
                decoded_text += CHARSET[index + shift]
        else:
            decoded_text += char
    return decoded_text

if __name__ == "__main__":
    with open(TARGET_FILE, 'r', encoding=ENCODING) as f:
        target_text = f.read()
    
    text_dict = []
    with open(DICT_FILE, 'r', encoding=ENCODING) as f:
        for line in f:
            line = line.strip()
            if line:
                text_dict += [item.lower().strip() for item in line.split(SEPARATOR)]
    
    shift = 0
    len = len(CHARSET) // 2
    
    while shift < len:
        decode_text = caesar_cipher_decode(target_text, shift)
        print(f'Attempt {shift} : {decode_text}')
        text = decode_text.split()
        text = [item.lower() for item in text]
        if any(item in text_dict for item in text):
            print('Word found in dictionary!')
            break
        shift += 1
    
    user_shift = int(input("Enter the shift: "))

    with open(RESULT_FILE, 'w', encoding=ENCODING) as f:
        f.write(caesar_cipher_decode(target_text, user_shift))
    
    print(f"Decoded text saved to {RESULT_FILE}")