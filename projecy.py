import hashlib

def hash_password(password):
    hash_value = 0
    for char in password:
        hash_value = (hash_value * 31 + ord(char)) % 30
    return hash_value

def hash_password_in_table(login, password):
    together = login + password
    hash_obj = hashlib.sha256(together.encode())
    account_str = hash_obj.hexdigest()[:16].upper()
    return account_str

def insert():
    while True:
        login = input("Enter login: ")
        if check_login(login):
            print("This login is already exist, please enter different one.")
        else:
            break
    password = input("Enter new password: ")
    info = input("Enter information: ")
    account_str = hash_password_in_table(login, password)
    hash_index = hash_password(password)
    insert_in_table(hash_index, account_str, login, info)

def check_login(login):
    with open("hash.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() != "" and line.strip() != "[DELETED]":
                account_data = line.strip().split(":")
                if account_data[1] == login:
                    return True
    return False

def insert_in_table(index, account_str, login, info):
    with open("hash.txt", "r+") as file:
        lines = file.readlines()
        original_index = index
        while True:
            if index >= len(lines):
                lines.extend(["\n"] * (index - len(lines) + 1))
            if lines[index].strip() == "" or lines[index].strip() == "[DELETED]":
                lines[index] = f"{account_str}:{login}:{info}\n"
                file.seek(0)
                file.writelines(lines)
                print("Account created!")
                break
            index = (index + 1) % 30
            if index == original_index:
                print("Hash table is full. Cannot create account.")
                break

def access_to_account():
    login = input("Enter login: ")
    password = input("Enter your password: ")
    account_str = hash_password_in_table(login, password)
    hash_index = hash_password(password)
    with open("hash.txt", "r") as file:
        lines = file.readlines()
        start_index = hash_index
        while True:
            if hash_index >= len(lines):
                break
            line = lines[hash_index].strip()
            if line != "" and line != "[DELETED]":
                account_data = line.split(":")
                if account_data[0] == account_str:
                    print(f"Information: {account_data[2]}")
                    return
            hash_index = (hash_index + 1) % 30
            if hash_index == start_index:
                break
    print("Account doesn’t exist or invalid login or password.")

def delete_account():
    login = input("Enter login: ")
    password = input("Enter your password: ")
    account_str = hash_password_in_table(login, password)
    with open("hash.txt", "r+") as file:
        lines = file.readlines()
        new_lines = []
        deleted = False
        for i, line in enumerate(lines):
            if line.strip() != "":
                account_data = line.strip().split(":")
                if account_data[0] == account_str and account_data[1] == login:
                    new_lines.append("[DELETED]\n")
                    deleted = True
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        if deleted:
            file.seek(0)
            file.writelines(new_lines)
            file.truncate()
            print("Account deleted!")
        else:
            print("Account doesn't exist or invalid login or password.")

def main():
    while True:
        choice = input("Choose the option:\n1. Create account\n2. Get access to account\n3. Delete account\n4. Exit\nEnter your decision: ")
        if choice == "1":
            insert()
        elif choice == "2":
            access_to_account()
        elif choice == "3":
            delete_account()
        elif choice == "4":
            break
        else:
            print("Invalid decision. Try again.")

if __name__ == "__main__":
    main()
