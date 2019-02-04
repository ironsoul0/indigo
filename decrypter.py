SALT_LEN = 15

def decreaseByOne(str):
  text = list(str)
  for i in range(0, len(text)):
    text[i] = chr(ord(text[i]) - 1)
  return ''.join(text)

def decrypt_password(password):
  return decreaseByOne(password[SALT_LEN:])

def process_chat(chat):
  if 'main_password' in chat:
    chat['main_password'] = decrypt_password(chat['main_password'])
  return chat