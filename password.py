import hashlib
import os

# password = bytes(input('Enter password: '),encoding='utf-8')
# print(password)
# salt = os.urandom(len(password)*2)
# dec_salt = salt.decode('utf-8',errors='ignore')
# print(bytes(dec_salt,encoding='utf-8'))
# print(password+bytes(dec_salt,encoding='utf-8'))
# hash = hashlib.sha512(password+bytes(dec_salt,encoding='utf-8'))
# hex_dig = hash.hexdigest()
# print(hex_dig)
item = ['1','2']
if '2' in item:
    print(1)
