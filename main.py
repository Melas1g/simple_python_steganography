from PIL import Image
import sys
import os


def text_to_binary(text, encoding='utf-8', errors='surrogatepass'):
    binary_str = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return binary_str.zfill(8 * ((len(binary_str) + 7) // 8))


def text_from_binary(binary_str, encoding='utf-8', errors='surrogatepass'):
    num = int(binary_str, 2)
    return num.to_bytes((num.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def convert_base(num, to_base=10, from_base=10):
    # first convert to decimal number
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]


def binary_to_color_delta(binary_str):
    color_deltas = []
    for i in range(0, len(binary_str), 2):
        color_deltas.append(int(convert_base(binary_str[i:i+2], from_base=2)))

    while len(color_deltas) % 3 != 0:
        color_deltas.insert(0, 0)

    color_triplets = []
    for i in range(0, len(color_deltas), 3):
        color_triplets.append((color_deltas[i], color_deltas[i+1], color_deltas[i+2]))

    return color_triplets


def color_delta_to_binary(color_delta_list):
    binary_str = ''
    for delta in color_delta_list:
        if delta == 0:
            binary_str += '00'
        elif delta == 1:
            binary_str += '01'
        elif delta == 2:
            binary_str += '10'
        elif delta == 3:
            binary_str += '11'
        else:
            return binary_str
    return binary_str


def hide_message_in_image(image, message):
    binary_message = text_to_binary(message)
    color_deltas = binary_to_color_delta(binary_message)

    width, height = image.size
    pixel_data = image.load()

    r, g, b, a = pixel_data[0, 0]

    i = 1
    for color_delta in color_deltas:
        if i >= width:
            break
        pixel_data[i, 0] = r + color_delta[0], g + color_delta[1], b + color_delta[2], 255
        i += 1

    if i < width:
        pixel_data[i, 0] = r + 4, g + 4, b + 4, 255

    return image


def extract_message_from_image(image):
    width, height = image.size
    pixel_data = image.load()

    r, g, b, a = pixel_data[0, 0]

    color_deltas = []
    for x in range(1, width):
        r_current, g_current, b_current, a_c = pixel_data[x, 0]

        color_deltas.append(r_current - r)
        color_deltas.append(g_current - g)
        color_deltas.append(b_current - b)

    return text_from_binary(color_delta_to_binary(color_deltas))


def main():
    if len(sys.argv) < 3:
        print("Usage: -e <image_path> '<text_to_hide>' OR python script.py -d <image_path>")
        sys.exit(1)

    mode = sys.argv[1]
    image_path = sys.argv[2]

    if mode == '-e':
        if len(sys.argv) != 4:
            print("Usage: python script.py -e <image_path> '<text_to_hide>'")
            sys.exit(1)
        text_to_hide = sys.argv[3]

        # load image
        try:
            original_image = Image.open(image_path).convert("RGBA")
        except Exception as e:
            print(f"Error opening image: {e}")
            sys.exit(1)

        # hide message
        output_image = hide_message_in_image(original_image, text_to_hide)

        # save output image in the same directory as input image
        dir_path = os.path.dirname(image_path)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = os.path.join(dir_path, f"{base_name}_encrypted.png")
        output_image.save(output_path)

        print(f"Saved as: {output_path}")

    elif mode == '-d':
        # load image
        try:
            original_image = Image.open(image_path).convert("RGBA")
        except Exception as e:
            print(f"Error opening image: {e}")
            sys.exit(1)

        # Get hidden message
        hidden_text = extract_message_from_image(original_image)
        print(hidden_text)

    else:
        print("Invalid mode. Use -e for encrypt or -d for decrypt.")
        sys.exit(1)


if __name__ == "__main__":
    main()