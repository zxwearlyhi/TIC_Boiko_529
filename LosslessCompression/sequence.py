import numpy as np
import matplotlib.pyplot as plt

# ===============================
# СОЗДАНИЕ СЛУЧАЙНОЙ ПОСЛЕДОВАТЕЛЬНОСТИ
# ===============================

np.random.seed(1)

sequence = np.random.randint(0, 10, 100)

# ===============================
# СОХРАНЕНИЕ ПОСЛЕДОВАТЕЛЬНОСТИ
# ===============================

with open("sequence.txt", "w") as file:

    for number in sequence:
        file.write(str(number) + " ")

# ===============================
# ПОДСЧЕТ СИМВОЛОВ
# ===============================

unique, counts = np.unique(sequence, return_counts=True)

# вероятность
probabilities = counts / len(sequence)

# ===============================
# ЭНТРОПИЯ
# ===============================

entropy = 0

for p in probabilities:
    entropy += -p * np.log2(p)

# ===============================
# ВЫВОД В ФАЙЛ
# ===============================

with open("results_sequence.txt", "w") as file:

    file.write("Символ | Кількість | Ймовірність\n")

    for i in range(len(unique)):

        file.write(
            f"{unique[i]} | "
            f"{counts[i]} | "
            f"{round(probabilities[i], 3)}\n"
        )

    file.write("\n")
    file.write(f"Ентропія: {round(entropy, 3)}")

# ===============================
# ГРАФИК
# ===============================

plt.figure(figsize=(8, 5))

plt.bar(unique, counts)

plt.xlabel("Символ")
plt.ylabel("Кількість")
plt.title("Частота символів")

plt.grid()

plt.savefig("sequence_plot.png", dpi=300)

plt.close()

print("практична 5 завершена!")