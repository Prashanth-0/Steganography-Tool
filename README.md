# Steganography-Tool
A Python-based steganography tool that allows you to hide text or files inside images using LSB (Least Significant Bit) encoding. The tool also supports colorful terminal output for better user experience.

## *🚀 Features*
✅ *Hide messages in images* (supports text & binary files)  
✅ *Extract hidden messages from images*  
✅ *Colorful and stylish terminal output* (via colorama and termcolor)  
✅ *User-friendly interactive menu*  
✅ *Error handling for missing files and invalid input*  

## *📦 Installation*
### *Step 1: Clone the Repository*
```bash 
git clone https://github.com/Prashanth-0/Steganography-Tool.git

cd Steganography-Tool
```
### *Step 2: Install Dependencies*
```bash
pip install -r requirements.txt
```
This installs the required libraries: `opencv-python`, `numpy`, `colorama`, `termcolor`.

## *📝 Encoding (Hiding Data)*
This tool allows you to hide text messages or files inside images.

### *1️⃣ Hide a Text Message in an Image*

1. Select option 1️⃣ Encode

2. Enter the image file name (e.g., test.jpg)

3. Enter 'T' for text mode

4. Type the secret message to hide

5. Enter the number of LSB bits to use (1-4, default 2)

6. The encoded image is saved as `test_encoded.png`.

### *2️⃣ Hide a File in an Image*

1. Select option 1️⃣ Encode

2. Enter the image file name (e.g., test.jpg)

3. Enter 'F' for file mode

4. Enter the file name to hide (e.g., secret.pdf)

5. Enter the number of LSB bits to use (1-4, default 2)

6. The encoded image is saved as `test_encoded.png`.

## *🔓 Decryption (Extracting Data)*
To extract the hidden message or file from the encoded image, use the Decode option.

### *1️⃣ Extract a Hidden Text Message*

1. Select option 2️⃣ Decode

2. Enter the encoded image file (e.g., test_encoded.png)

3. Enter the number of LSB bits used for encoding (1-4, default 2)

4. The extracted message appears on the screen.

## *2️⃣ Extract a Hidden File*

1. Select option 2️⃣ Decode

2. Enter the encoded image file (e.g., test_encoded.png)

3. Enter 'Y' to save the output as a file

4. Enter the filename to save the extracted data (e.g., extracted.pdf)

5. The extracted file is saved successfully.

## *⚠ Notes*

You must use the same n-bits value for decoding as was used for encoding.

The larger the n-bits value, the more data can be hidden, but the image quality decreases.

Encoded images should not be recompressed (e.g., avoid saving as JPEG again).

## *👨‍💻 Author*

Created by *Prashanth*


GitHub: https://github.com/your-username 
