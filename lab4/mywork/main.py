from pwn import *
import re
import Solve
import json

io = remote("172.26.201.17", 2134)
recv = io.recvline().decode("utf-8")
print(recv)
num_question = input("Choose num question: ")
io.sendline(num_question.encode("utf-8"))
match num_question:
    case "1":
        question_text = io.recvrepeat(timeout=0.5).decode("utf-8")
        print(question_text)
        prime_number = re.findall(r"Prime:\ (.*)", question_text)[0]
        prime_number = int(prime_number)
        # z = {1,2,3,...,prime - 1}
        g = str()
        print("Finding generator...")
        for i in range(2,prime_number):
            print(i)
            if(Solve.generator(i,prime_number)):
                print("Found")
                g = str(i) 
                break
            else:
                print("Not")
                continue
        io.sendline(g.encode("utf-8"))

        question_text2 = io.recvrepeat(timeout=6).decode("utf-8")
        print(question_text2)
        my_private_key = 5
        my_public_key = pow(int(g),my_private_key,prime_number)
        my_public_key = Solve.public_key(int(g),my_private_key,prime_number)
        teacher_public_key = re.findall(r'My\ public\ key:\ (.*)',question_text2)[0]
        io.sendline(str(my_public_key).encode("utf-8"))

        share_key = Solve.create_share_key(int(teacher_public_key),my_private_key,prime_number)
        print(share_key)

        question_text3 = io.recvrepeat(timeout=0.5).decode("utf-8")
        json_text = re.findall(r'\{.*\}',question_text3)[0]
        print(question_text3)
        data = json.loads(json_text)
        plaintext = Solve.encryption_key(share_key,data["nonce"],data["header"],data["ciphertext"],data["tag"])
        print(plaintext)

    case "2": 
        question_text = io.recvrepeat(timeout=0.5).decode("utf-8")
        print(question_text)
        my_private_key = 5
        prime_hex = re.findall(r'Prime:\ (.*)',question_text)[0]
        generator_hex = re.findall(r'Generator:\ (.*)',question_text)[0]
        prime_number = int(prime_hex,16)
        generator_number = int(generator_hex,16)
        my_public_key = Solve.public_key(generator_number,my_private_key,prime_number) 
        io.sendline(str(my_public_key).encode("utf-8"))


        question_text2 = io.recvrepeat(timeout=0.5).decode("utf-8")
        print(question_text2)
        teacher_public_key = re.findall(r'My\ public\ key\ \(in hex\):\ (.*)',question_text2)[0]
        share_key = Solve.create_share_key(int(teacher_public_key,16),my_private_key,prime_number)
        json_text = re.findall(r'\{.*\}',question_text2)[0]
        data = json.loads(json_text)
        plaintext = Solve.encryption_key(share_key,data["nonce"],data["header"],data["ciphertext"],data["tag"])
        print(plaintext)


    case "3":
        question_text = io.recvrepeat(timeout=0.5).decode("utf-8")
        print(question_text)
        my_private_key = 5
        prime_hex = re.findall(r'Prime:\ (.*)',question_text)[0]
        generator_hex = re.findall(r'Generator:\ (.*)',question_text)[0]
        prime_number = int(prime_hex,16)
        generator_number = int(generator_hex,16)
        my_public_key = Solve.public_key(generator_number,my_private_key,prime_number)
        io.sendline(str(my_public_key).encode("utf-8"))
        
        question_text2 = io.recvrepeat(timeout=0.5).decode("utf-8")
        print(question_text2)
        json_text = re.findall(r'\{.*\}',question_text2)[0]
        data = json.loads(json_text)

    case "4":
        question_text = io.recvrepeat(timeout=2).decode("utf-8")
        print(question_text)
        pem_text = re.findall(r'-----BEGIN PUBLIC KEY-----\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n-----END PUBLIC KEY-----',question_text)[0]
        intercept_message = re.findall(r'Intercepted message \(in hex\):\n(.*)',question_text)[0][2:]
        RSA_factor = re.findall(r'RSA\ factor\ (.*)',question_text)[0]
        plaintext = Solve.RSA_format(pem_text,intercept_message,RSA_factor)
        print(plaintext)
