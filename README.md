# PyRanSim
**PyRanSim** is a simple ransomware simulation program in python, which is designed for educational purposes. It aims to demonstrate how a basic ransomware functions, including encryption and decryption of files, key management, and basic command-and-control (C2) techniques using Discord webhooks.
<br>
<br>

## Program Files

This repository contains:
- **`encryptor.py`**: A basic encryption program, that encrypts specified files in a given folder using a symmetric key. 
- **`encryptor_v2.py`**: A bit advanced version of `encryptor.py` with additional command-and-control (C2) functionality. This version allows the encryption key to be exfiltrated to a Discord webhook, either in clear text or RSA-encrypted format.
- **`decryptor.py`**: Decrypts files encrypted by `encryptor.py` and `encryptor_v2.py` using the saved symmetric key.
- **`C2.private`**: The RSA private key corresponding to the public key hardcoded in `encryptor_v2.py`. This is used in decrypting the RSA-encrypted symmetric key when testing C2 functionality.
- **`demo_files` folder**: Contains sample files (e.g., `.txt`, `.jpg`, `.png`, `.docx`, `.xlsx`) for testing the encryption and decryption processes.
<br>
<br>

## Installation and Support

This program requires **Python 3.x** and has been tested on **Windows OS**. To use the program, ensure you have the required dependencies `cryptography` and `requests` libraries installed.

Install dependencies:
```cmd
pip install cryptography requests
OR
pip3 install cryptography requests
```
<br>
<br>

## Usage Instructions

### 1. `encryptor.py`
Encrypts files within a specified directory. Accepts a single `-p` argument to specify the path.

**Command Usage:**
```cmd
python encryptor.py -p <path_to_folder>
```

**Example:**
```cmd
python encryptor.py -p "C:\path\to\demo_files"
```
<br>

### 2. `encryptor_v2.py`
This is a bit advanced version of encryptor with C2 functionality. It accepts `-p` to specify the folder path for encryption and `-x` to choose the exfiltration method (`clear` or `encrypted`). Edit this script file and replace 'Your_Discord_Webhook_URL' with your actual discord webhook url.

**Create a Webhook in Discord**
1. Go to the **Discord server** and **channel** where you want to send the message.
2. Click on the **Settings** for the channel, then go to **Integrations**.
3. Under **Webhooks**, click **Create Webhook**.
4. Give your webhook a **name** and **select the channel** where it will send messages.
5. Click **Copy Webhook URL** – save this URL as you’ll need it in the code.

<br>

**Command Usage:**
```cmd
python encryptor_v2.py -p <path_to_folder> -x <exfiltration_type>
```

**Example:**
```cmd
python encryptor_v2.py -p "C:\path\to\demo_files" -x clear
```

<br>

### 3. `decryptor.py`
Decrypts files encrypted by either `encryptor.py` or `encryptor_v2.py` using the saved symmetric key. Accepts `-p` for the path to the encrypted files and `-k` for the encryption key file.

**Command Usage:**
```cmd
python decryptor.py -p <path_to_folder> -k <path_to_key_file>
```

**Example:**
```cmd
python decryptor.py -p "C:\path\to\demo_files" -k ransom_key.key
```
<br>
<br>

## Disclaimer

These scripts are intended solely for EDUCATIONAL and ETHICAL purposes to demonstrate the mechanics of a basic ransomware in a controlled environment. Any misuse of these scripts to encrypt files or perform ransomware activities on unauthorized systems is illegal and can be punishable under law. The author is not responsible for any damage, loss or other harm resulting from these scripts, whether intentional or accidental. Any use of this code outside of its intended educational purpose, is strictly prohibited and may be illegal. Use responsibly and only on systems you own or have permission to test.
