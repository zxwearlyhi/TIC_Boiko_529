import math
import collections

# =========================
# ЗЧИТУВАННЯ ФАЙЛУ
# =========================

with open("sequence.txt", "r", encoding="utf-8") as file:

    data = file.read().split()

sequence = ""

for number in data:
    sequence += number

sequences = [sequence]

# =========================
# RLE КОДУВАННЯ
# =========================

def rle_encode(sequence):

    result = ""

    count = 1

    for i in range(1, len(sequence)):

        if sequence[i] == sequence[i - 1]:
            count += 1

        else:
            result += str(count) + sequence[i - 1]
            count = 1

    result += str(count) + sequence[-1]

    return result


# =========================
# RLE ДЕКОДУВАННЯ
# =========================

def rle_decode(sequence):

    result = ""

    number = ""

    for symbol in sequence:

        if symbol.isdigit():
            number += symbol

        else:
            result += symbol * int(number)
            number = ""

    return result


# =========================
# LZW КОДУВАННЯ
# =========================

def lzw_encode(sequence):

    dictionary = {}

    for i in range(256):
        dictionary[chr(i)] = i

    current = ""

    result = []

    code = 256

    for symbol in sequence:

        temp = current + symbol

        if temp in dictionary:
            current = temp

        else:

            result.append(dictionary[current])

            dictionary[temp] = code

            code += 1

            current = symbol

    if current != "":
        result.append(dictionary[current])

    return result


# =========================
# ЗАПИС РЕЗУЛЬТАТІВ
# =========================

with open("results_rle_lzw.txt", "w", encoding="utf-8") as file:

    for index, sequence in enumerate(sequences):

        # =========================
        # ЕНТРОПИЯ
        # =========================

        counts = collections.Counter(sequence)

        probabilities = []

        for value in counts.values():
            probabilities.append(value / len(sequence))

        entropy = 0

        for p in probabilities:
            entropy -= p * math.log2(p)

        # =========================
        # RLE
        # =========================

        encoded_rle = rle_encode(sequence)

        decoded_rle = rle_decode(encoded_rle)

        # =========================
        # LZW
        # =========================

        encoded_lzw = lzw_encode(sequence)

        # =========================
        # РОЗМІРИ
        # =========================

        original_bits = len(sequence) * 16

        rle_bits = len(encoded_rle) * 16

        lzw_bits = len(encoded_lzw) * 16

        rle_ratio = round(original_bits / rle_bits, 2)

        lzw_ratio = round(original_bits / lzw_bits, 2)

        # =========================
        # ЗАПИС У ФАЙЛ
        # =========================

        file.write("\n====================\n")

        file.write(f"Послідовність {index + 1}\n\n")

        file.write(f"Original:\n{sequence}\n\n")

        file.write(f"Ентропія: {round(entropy, 3)}\n\n")

        file.write(f"RLE encoded:\n{encoded_rle}\n")
        file.write(f"RLE decoded:\n{decoded_rle}\n")
        file.write(f"RLE compression ratio: {rle_ratio}\n\n")

        file.write(f"LZW encoded:\n{encoded_lzw}\n")
        file.write(f"LZW compression ratio: {lzw_ratio}\n\n")

print("Практична 6 завершена!")