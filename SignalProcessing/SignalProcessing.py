import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
import os

# ===============================
# ПАРАМЕТРЫ (ВАРИАНТ 1)
# ===============================
n = 500
Fs = 1000
F_max = 3

# ===============================
# СОЗДАНИЕ ПАПКИ ДЛЯ ГРАФИКОВ
# ===============================
if not os.path.exists("SignalProcessing/figures"):
    os.makedirs("SignalProcessing/figures")

# ===============================
# ГЕНЕРАЦИЯ СЛУЧАЙНОГО СИГНАЛА
# ===============================
random_signal = np.random.normal(0, 10, n)

# ===============================
# ВРЕМЯ
# ===============================
t = np.arange(n) / Fs

# ===============================
# ФИЛЬТР (ФНЧ)
# ===============================
w = F_max / (Fs / 2)
sos = signal.butter(3, w, 'low', output='sos')

filtered_signal = signal.sosfiltfilt(sos, random_signal)

# ===============================
# ФУНКЦИЯ ПОСТРОЕНИЯ ГРАФИКА
# ===============================
def plot_graph(x, y, title, xlabel, ylabel, filename):
    fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))

    ax.plot(x, y, linewidth=1)

    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_title(title, fontsize=14)

    ax.grid()

    fig.savefig(f"SignalProcessing/figures/{filename}.png", dpi=600)
    plt.close()

# ===============================
# ГРАФИК СИГНАЛА
# ===============================
plot_graph(
    t,
    filtered_signal,
    f"Сигнал з максимальною частотою F_max = {F_max} Гц",
    "Час (секунди)",
    "Амплітуда сигналу",
    "signal"
)

# ===============================
# СПЕКТР
# ===============================
spectrum = fft.fft(filtered_signal)
spectrum = np.abs(fft.fftshift(spectrum))

freqs = fft.fftfreq(n, 1 / Fs)
freqs = fft.fftshift(freqs)

# ===============================
# ГРАФИК СПЕКТРА
# ===============================
plot_graph(
    freqs,
    spectrum,
    f"Спектр сигналу з максимальною частотою F_max = {F_max} Гц",
    "Частота (Гц)",
    "Амплітуда спектру",
    "spectrum"
)

# ===============================
# ВЫВОД
# ===============================
print("Готово! Графіки збережені у папці SignalProcessing/figures")