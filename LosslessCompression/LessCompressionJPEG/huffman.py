import os
from PIL import Image
import matplotlib.pyplot as plt
from huffman import HuffmanTree

# ==========================
# СПИСОК ИЗОБРАЖЕНИЙ
# ==========================

images = [
    "image_one.jpg",
    "image_two.jpg",
    "image_three.jpg"
]

qualities = [100, 80, 50, 20]

results = []

# ==========================
# ОБРАБОТКА ИЗОБРАЖЕНИЙ
# ==========================

for image_name in images:

    # размер оригинала
    original_size = os.path.getsize(image_name)

    # открытие изображения
    image = Image.open(image_name)

    # перевод в оттенки серого
    gray = image.convert("L")

    # получение пикселей
    pixels = list(gray.getdata())

    # дерево Хаффмана
    tree = HuffmanTree(pixels)

    table = tree.value_to_bitstring_table()

    # средняя длина кода
    total_bits = 0

    for pixel in pixels:
        total_bits += len(table[pixel])

    avg_bits = round(total_bits / len(pixels), 2)

    image_result = []

    # JPEG сжатие
    for quality in qualities:

        compressed_name = f"{image_name[:-4]}_{quality}.jpg"

        image.save(compressed_name, quality=quality)

        compressed_size = os.path.getsize(compressed_name)

        ratio = round(original_size / compressed_size, 2)

        image_result.append(ratio)

    results.append((image_result, avg_bits))

# ==========================
# ЗАПИСЬ В ФАЙЛ
# ==========================

with open("results_jpeg.txt", "w", encoding="utf-8") as file:

    for i in range(len(images)):

        file.write(f"{images[i]}\n")

        file.write(f"Average Huffman bits: {results[i][1]}\n")

        for j in range(len(qualities)):

            file.write(
                f"Quality {qualities[j]} -> "
                f"Compression ratio: {results[i][0][j]}\n"
            )

        file.write("\n")

# ==========================
# ГРАФИК
# ==========================

plt.figure(figsize=(8, 5))

for i in range(len(images)):

    plt.plot(
        qualities,
        results[i][0],
        marker="o",
        label=images[i]
    )

plt.xlabel("JPEG quality")
plt.ylabel("Compression ratio")

plt.title("Практична 8")

plt.legend()

plt.grid()

plt.savefig("jpeg_plot.png")

plt.show()

print("Практична 8 завершена!")