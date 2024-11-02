import os
import sys
import argparse
from cryptography.fernet import Fernet


# This function loads the encryption key from file
def load_key(key_path):
    return open(key_path, "rb").read()


# This function decrypts a single file, remove ".pyransim" extension and restore original file
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    
    decrypted_data = fernet.decrypt(encrypted_data)
    
    original_file_path = file_path.replace(".pyransim", "")
    with open(original_file_path, "wb") as file:
        file.write(decrypted_data)
    print("File decrypted: " + file_path)
    
    os.remove(file_path)


# Function to recursively decrypt all files in the directory
def decrypt_recursive(directory, key):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".pyransim"):
                file_path = os.path.join(root, file_name)
                decrypt_file(file_path, key)


# This function creates a thank you note on users desktop
def thankyou_note():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    note_path = os.path.join(desktop, "Thank_You_from_PyRanSim.txt")
    note_content = """
                    \nThank you for your payment.\n
                    \nYour files have been decrypted by PyRanSim.\n
                    \nHave a nice day!\n
                    """
    with open(note_path, "w") as note:
        note.write(note_content)


# Function to handle command line arguments and help menu
def cmd_args():
    parser = argparse.ArgumentParser(epilog="CMD Example: python decryptor.py -p \"C:\path\\to\demo_files\" -k \"ransom_key.key\"")
    parser.add_argument('-p', '--path', type=str, required=True, help="Directory path to decrypt")
    parser.add_argument('-k', '--key', type=str, required=True, help="Path to encryption key file")
    return parser.parse_args()


# Main function for the decryption script
def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        args = cmd_args()
        sys.exit(1)

    if len(sys.argv) <= 4:
        print("Error: Required arguments missing.")
        print("Help message: python encryptor.py -h or python encryptor.py --help")
        sys.exit(1)

    # Load encryption key, decryt all file and place thank you note on user desktop
    args = cmd_args()
    key = load_key(args.key)
    decrypt_recursive(args.path, key)
    thankyou_note()
    
    print("\n\nAll files have been decrypted. Check the thank you note on your desktop.")

if __name__ == "__main__":
    main()
