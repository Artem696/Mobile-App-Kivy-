import hashlib
import os
import mysql.connector
from mysql.connector import Error

# password = bytes(input('Enter password: '),encoding='utf-8')
# print(password)
# salt = os.urandom(len(password)*2)
# dec_salt = salt.decode('utf-8',errors='ignore')
# print(bytes(dec_salt,encoding='utf-8'))
# print(password+bytes(dec_salt,encoding='utf-8'))
# hash = hashlib.sha512(password+bytes(dec_salt,encoding='utf-8'))
# hex_dig = hash.hexdigest()
# print(hex_dig)
def query(query,type,count='one'):
          try:
               with mysql.connector.connect(
                    host="127.0.0.1",
                    user=("root"),
                    password=("DcA4~6gfec7K"),
                    database="xerox"
               ) as connection:
                    if type == "select":
                        if count == 'one':
                            with connection.cursor() as cursor:
                                cursor.execute(query)
                                result = cursor.fetchone()[0]
                                return result
                        if count == 'all':
                            with connection.cursor() as cursor:
                                cursor.execute(query)
                                result = cursor.fetchall()
                                return result
                    else:
                         with connection.cursor(buffered=True) as cursor:
                              result = cursor.execute(query)
                              connection.commit()
          except Error as e:
               print(f"The error '{e}' occurred")
answer = query('select * from xerox order by id desc','select','all')
count = query('select count(*) from xerox','select')
for i in range(count):
    print(answer[i][0])
