import cv2
import numpy as np
import os
from colorama import init, Fore, Style
from termcolor import colored


init(autoreset=True)

def to_bin(data):
    """Convert data to binary format as a string."""
    if isinstance(data, str):
        return ''.join(format(ord(i), "08b") for i in data)
    elif isinstance(data, bytes):
        return ''.join(format(i, "08b") for i in data)
    elif isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image_name, secret_data, n_bits=2):
    """Encodes secret_data into image_name using n_bits LSB steganography."""
    try:
        if not os.path.exists(image_name):
            print(Fore.RED + "[❌] Error: Image not found! Please check the path.")
            return None

        image = cv2.imread(image_name)
        if image is None:
            print(Fore.RED + "[❌] Error: Cannot open image. It might be corrupted.")
            return None

        h, w, _ = image.shape  
        n_bytes = (h * w * 3 * n_bits) // 8  

        print(Fore.YELLOW + f"[*] Image Size: {h}x{w}, Maximum bytes to encode: {n_bytes}")
        print(Fore.CYAN + f"[*] Data Size: {len(secret_data)} bytes")

        if len(secret_data) > n_bytes:
            print(Fore.RED + f"[❌] Error: Data too large for this image! Use a bigger image.")
            return None

        print(Fore.GREEN + "[✔] Encoding data...")

        # Append stopping sequence
        if isinstance(secret_data, str):
            secret_data += "====="
        elif isinstance(secret_data, bytes):
            secret_data += b"====="

        binary_secret_data = to_bin(secret_data)
        data_index = 0
        data_len = len(binary_secret_data)

        for row in image:
            for pixel in row:
                if data_index >= data_len:
                    break  

                r, g, b = to_bin(pixel)

                if data_index < data_len:
                    pixel[0] = int(r[:-n_bits] + binary_secret_data[data_index:data_index + n_bits], 2)
                    data_index += n_bits
                if data_index < data_len:
                    pixel[1] = int(g[:-n_bits] + binary_secret_data[data_index:data_index + n_bits], 2)
                    data_index += n_bits
                if data_index < data_len:
                    pixel[2] = int(b[:-n_bits] + binary_secret_data[data_index:data_index + n_bits], 2)
                    data_index += n_bits

        return image
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
        return None

def decode(image_name, n_bits=2, in_bytes=False):
    """Decodes hidden data from an image."""
    try:
        print(Fore.GREEN + "[✔] Decoding...")

        if not os.path.exists(image_name):
            print(Fore.RED + "[❌] Error: Image file not found!")
            return None

        image = cv2.imread(image_name)
        if image is None:
            print(Fore.RED + "[❌] Error: Cannot open the image. It might be corrupted.")
            return None

        binary_data = ""

        for row in image:
            for pixel in row:
                r, g, b = to_bin(pixel)

                binary_data += r[-n_bits:]  
                binary_data += g[-n_bits:]  
                binary_data += b[-n_bits:]  

        all_bytes = [binary_data[i : i + 8] for i in range(0, len(binary_data), 8)]
        
        if in_bytes:
            decoded_data = bytearray()
            for byte in all_bytes:
                decoded_data.append(int(byte, 2))
                if decoded_data[-5:] == b"=====":
                    break
        else:
            decoded_data = ""
            for byte in all_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "=====":
                    break

        return decoded_data[:-5]  
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")
        return None

def main():
    while True:
        print("\n" + colored("🔹 Image Steganography - Hide & Extract Data 🔹", "blue", attrs=["bold"]))
        print(colored("1️⃣ Encode (Hide data in image)", "green"))
        print(colored("2️⃣ Decode (Extract data from image)", "yellow"))
        print(colored("3️⃣ Exit", "red"))

        choice = input("👉 Enter your choice (1/2/3): ").strip()

        if choice == "1":
            image_name = input("\n📂 " + Fore.BLUE + "Enter the image file to hide data in: ").strip()
            data_choice = input(Fore.MAGENTA + "💡 Enter 'T' for text or 'F' for a file: ").strip().upper()

            if data_choice == "T":
                secret_data = input(Fore.CYAN + "🔑 Enter the text to hide: ").strip()
            elif data_choice == "F":
                file_name = input(Fore.CYAN + "📄 Enter the file to hide: ").strip()
                if not os.path.exists(file_name):
                    print(Fore.RED + "[❌] Error: File not found!")
                    continue
                with open(file_name, "rb") as f:
                    secret_data = f.read()
            else:
                print(Fore.RED + "[❌] Invalid choice!")
                continue

            n_bits = int(input(Fore.YELLOW + "🔢 Enter the number of bits to use (1-4, default 2): ") or 2)
            output_image = image_name.split(".")[0] + "_encoded.png"

            encoded_image = encode(image_name, secret_data, n_bits)
            if encoded_image is not None:
                cv2.imwrite(output_image, encoded_image)
                print(Fore.GREEN + f"[✔] Encoded image saved as {output_image}!")

        elif choice == "2":
            image_name = input("\n📂 " + Fore.BLUE + "Enter the encoded image file: ").strip()
            save_choice = input(Fore.MAGENTA + "💾 Do you want to save output as a file? (Y/N): ").strip().upper()

            n_bits = int(input(Fore.YELLOW + "🔢 Enter the number of bits used for encoding (default 2): ") or 2)

            if save_choice == "Y":
                file_name = input(Fore.CYAN + "📄 Enter filename to save extracted data: ").strip()
                decoded_data = decode(image_name, n_bits, in_bytes=True)
                if decoded_data:
                    with open(file_name, "wb") as f:
                        f.write(decoded_data)
                    print(Fore.GREEN + f"[✔] Extracted file saved as {file_name}!")
            else:
                decoded_data = decode(image_name, n_bits)
                if decoded_data:
                    print(Fore.GREEN + f"\n🔓 Extracted Data: {decoded_data}")

        elif choice == "3":
            print(Fore.RED + "\n👋 Exiting... Have a great day!")
            break

        else:
            print(Fore.RED + "[❌] Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
