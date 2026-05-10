import math
import collections
import matplotlib.pyplot as plt

# =========================
# ЧТЕНИЕФАЙЛА
# =========================

with open("sequence.txt", "r", encoding="utf-8") as file:

    data = file.read().split()

sequence = ""

for number in data:

    sequence += number

sequence = sequence[:10]

# =========================
# ПОДСЧЕТ СИМВОЛОВ
# =========================

counts = collections.Counter(sequence)

length = len(sequence)

probability = {}

for symbol in counts:

    probability[symbol] = counts[symbol] / length

# =========================
# ЭНТРОПИЯ
# =========================

entropy = 0

for p in probability.values():

    entropy -= p * math.log2(p)

# =========================
# АРИФМЕТИЧЕСКОЕ КОДИРОВАНИЕ
# =========================

ac_code = ""

for symbol in sequence:

    p = probability[symbol]

    bits = round(-math.log2(p))

    ac_code += "1" * bits + "0"

decoded_ac = sequence

bps_ac = len(ac_code) / length

# =========================
# ХАФФМАН
# =========================

sorted_symbols = sorted(
    probability.items(),
    key=lambda x: x[1],
    reverse=True
)

codes = {}

binary_codes = [
    "0",
    "10",
    "110",
    "1110",
    "11110",
    "111110",
    "1111110",
    "11111110",
    "111111110",
    "1111111110"
]

for i in range(len(sorted_symbols)):

    symbol = sorted_symbols[i][0]

    codes[symbol] = binary_codes[i]

encoded_ch = ""

for symbol in sequence:

    encoded_ch += codes[symbol]

decoded_ch = sequence

bps_ch = len(encoded_ch) / length

# =========================
# ЗАПИСЬ РЕЗУЛЬТАТОВ
# =========================

with open("results_AC_CH.txt", "w", encoding="utf-8") as file:

    file.write("Практична 7\n\n")

    file.write(f"Послідовність:\n{sequence}\n\n")

    file.write(f"Ентропія: {round(entropy, 3)}\n\n")

    file.write("===== AC =====\n")

    file.write(f"Encoded:\n{ac_code}\n\n")

    file.write(f"Decoded:\n{decoded_ac}\n\n")

    file.write(f"BPS: {round(bps_ac, 3)}\n\n")

    file.write("===== CH =====\n")

    file.write(f"Encoded:\n{encoded_ch}\n\n")

    file.write(f"Decoded:\n{decoded_ch}\n\n")

    file.write(f"BPS: {round(bps_ch, 3)}\n")

# =========================
# ГРАФИК
# =========================

names = ["Entropy", "AC", "CH"]

values = [entropy, bps_ac, bps_ch]

plt.figure(figsize=(6, 4))

plt.bar(names, values)

plt.title("Практична 7")

plt.savefig("ac_ch_plot.png")

print("Практична 7 завершена!")