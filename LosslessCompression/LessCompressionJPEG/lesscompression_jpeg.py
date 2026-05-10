import os
from PIL import Image
import matplotlib.pyplot as plt

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
# СЖАТИЕ JPEG
# ==========================

for image_name in images:

    original_size = os.path.getsize(image_name)

    image = Image.open(image_name)

    image_result = []

    for quality in qualities:

        compressed_name = f"{image_name[:-4]}_{quality}.jpg"

        image.save(compressed_name, quality=quality)

        compressed_size = os.path.getsize(compressed_name)

        ratio = round(original_size / compressed_size, 2)

        image_result.append(ratio)

    results.append(image_result)

# ==========================
# ЗАПИСЬ В ФАЙЛ
# ==========================

with open("results_jpeg.txt", "w", encoding="utf-8") as file:

    for i in range(len(images)):

        file.write(f"{images[i]}\n")

        for j in range(len(qualities)):

            file.write(
                f"Quality {qualities[j]} -> "
                f"Compression ratio: {results[i][j]}\n"
            )

        file.write("\n")

# ==========================
# ГРАФИК
# ==========================

plt.figure(figsize=(8, 5))

for i in range(len(images)):

    plt.plot(qualities, results[i], marker="o", label=images[i])

plt.xlabel("JPEG quality")
plt.ylabel("Compression ratio")

plt.title("Практична 8")

plt.legend()

plt.grid()

plt.savefig("jpeg_plot.png")

plt.show()

print("Практична 8 завершена!")