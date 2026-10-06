import hashlib

def hash_file(filename):
    with open(filename, "rb") as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()

if __name__ == "__main__":
    file = input("Enter file path: ")
    print("SHA256 Hash:", hash_file(file))
