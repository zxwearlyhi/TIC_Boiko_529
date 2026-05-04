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
# ГЕНЕРАЦИЯ СИГНАЛА
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
# ФУНКЦИЯ ГРАФИКА
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
# СИГНАЛ
# ===============================
plot_graph(
    t,
    filtered_signal,
    f"Сигнал F_max = {F_max} Гц",
    "Час",
    "Амплітуда",
    "signal"
)

# ===============================
# СПЕКТР
# ===============================
spectrum = fft.fft(filtered_signal)
spectrum = np.abs(fft.fftshift(spectrum))

freqs = fft.fftfreq(n, 1 / Fs)
freqs = fft.fftshift(freqs)

plot_graph(
    freqs,
    spectrum,
    "Спектр сигналу",
    "Частота",
    "Амплітуда",
    "spectrum"
)

# ===============================
# ПРАКТИЧНА 3
# ===============================

Dt_values = [2, 4, 8, 16]

variances = []
snr_values = []

# фильтр для восстановления (ОДИН раз)
F_filter = 10
w_filter = F_filter / (Fs / 2)
sos_filter = signal.butter(3, w_filter, 'low', output='sos')

for Dt in Dt_values:

    # дискретизация
    discrete_signal = np.zeros(n)
    for i in range(0, n, Dt):
        discrete_signal[i] = filtered_signal[i]

    # спектр
    spec = fft.fft(discrete_signal)
    spec = np.abs(fft.fftshift(spec))

    # восстановление
    restored_signal = signal.sosfiltfilt(sos_filter, discrete_signal)

    # ошибка
    error = restored_signal - filtered_signal

    # дисперсия и SNR
    var_signal = np.var(filtered_signal)
    var_error = np.var(error)

    variances.append(var_error)
    snr_values.append(var_signal / var_error)

    # графики
    plot_graph(t, discrete_signal, f"Dt = {Dt}", "Час", "Амплітуда", f"discrete_{Dt}")
    plot_graph(freqs, spec, f"Спектр Dt = {Dt}", "Частота", "Амплітуда", f"spectrum_{Dt}")
    plot_graph(t, restored_signal, f"Відновлений Dt = {Dt}", "Час", "Амплітуда", f"restored_{Dt}")

# ===============================
# ФИНАЛЬНЫЕ ГРАФИКИ
# ===============================
plot_graph(Dt_values, variances, "Дисперсія", "Dt", "Дисперсія", "variance")
plot_graph(Dt_values, snr_values, "Сигнал/шум", "Dt", "SNR", "snr")

# ===============================
# ВЫВОД
# ===============================
print("Готоо! Всі графіки збережені")