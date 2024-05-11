import string
import random

def generate_random_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Sử dụng hàm để tạo mật khẩu
password = generate_random_password(10)
print(password)
