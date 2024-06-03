from PIL import Image
import bitarray as ba


def adjust_bit(b, v):
   return (b & ~1) | v


def conceal_data(data: str, img_path: str, output_name: str):
   hidden_bytes = data.encode('utf-8')
   all_bits = list(iterate_bits(hidden_bytes))
   with Image.open(img_path) as img:
       img_bytes = img.tobytes()

       if len(all_bits) > len(img_bytes):
           raise ValueError("Message too long")

       new_img_bytes = bytearray(len(img_bytes))
       for i, b in enumerate(img_bytes):
           if len(all_bits) != 0:
               new_img_bytes[i] = adjust_bit(b, all_bits[0])
               all_bits.pop(0)
           else:
               new_img_bytes[i] = b

       new_img = Image.frombytes('RGB', img.size, new_img_bytes)
       new_img.save(output_name)

   return new_img_bytes


def extract_data(image_path: str = None):
   extracted_bits = []
   with Image.open(image_path) as img:
       img_bytes = bytearray(img.tobytes())

       for i, b in enumerate(img_bytes):
           extracted_bits.append(bool(b & 1))

   bit_array = ba.bitarray(extracted_bits).tobytes()
   return bit_array.split(b"\0")[0].decode('utf-8', errors='ignore')


def sample():
   with Image.open("grayson.jpg") as img:
       img_bytes = img.tobytes()

       print(len(img_bytes) / 3)

       new_img_bytes = bytearray(len(img_bytes))
       for i, b in enumerate(img_bytes):
           new_img_bytes[i] = b ^ 0b10010110

       new_img = Image.frombytes('RGB', img.size, new_img_bytes)
       new_img.show()

       for bit in iterate_bits(bytes([0b00001111, 0b11110000])):
           print(bit)


def main():
    print("new ")
    conceal_data("Hello world", "grayson.jpg", "new.jpg")


def iterate_bits(input_bytes):
   for b in input_bytes:
       for i in range(8):
           yield b >> (7 - i) & 1


main()