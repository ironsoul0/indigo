from cryptography.fernet import Fernet

key = b'W-RcadGWZRMz_odFQqg1GuGIomHOPCIub0KNaitcpqQ='
print('Key is ', key)
cipher_suite = Fernet(key)
kek = "A really secret message. Not for prying eyes."
cipher_text = cipher_suite.encrypt(kek.encode())
plain_text = cipher_suite.decrypt(cipher_text).decode()
print(plain_text)