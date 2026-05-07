import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
import os

# ==================================================
# ПРАКТИЧНА РОБОТА №2
# Генерація сигналів та побудова спектру
# ==================================================

# ===============================
# ПАРАМЕТРИ (ВАРІАНТ 1)
# ===============================
n = 500
Fs = 1000
F_max = 3

# ===============================
# СТВОРЕННЯ ПАПКИ ДЛЯ ГРАФІКІВ
# ===============================
if not os.path.exists("SignalProcessing/figures"):
    os.makedirs("SignalProcessing/figures")

# ===============================
# ГЕНЕРАЦІЯ ВИПАДКОВОГО СИГНАЛУ
# ===============================
random_signal = np.random.normal(0, 10, n)

# ===============================
# ЧАС
# ===============================
t = np.arange(n) / Fs

# ===============================
# ФІЛЬТР НИЗЬКИХ ЧАСТОТ
# ===============================
w = F_max / (Fs / 2)
sos = signal.butter(3, w, 'low', output='sos')

filtered_signal = signal.sosfiltfilt(
    sos,
    random_signal
)

# ===============================
# ФУНКЦІЯ ПОБУДОВИ ГРАФІКІВ
# ===============================
def plot_graph(x, y, title, xlabel, ylabel, filename):

    fig, ax = plt.subplots(
        figsize=(21/2.54, 14/2.54)
    )

    ax.plot(x, y, linewidth=1)

    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_title(title, fontsize=14)

    ax.grid()

    fig.savefig(
        f"SignalProcessing/figures/{filename}.png",
        dpi=600
    )

    plt.close()

# ===============================
# ГРАФІК СИГНАЛУ
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
# СПЕКТР СИГНАЛУ
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

print("Практична робота 2 завершена!")

# ==================================================
# ПРАКТИЧНА РОБОТА №3 (ВАРІАНТ 1)
# Дискретизація сигналу
# ==================================================

Dt_values = [2, 4, 8, 16]

variances = []
snr_values = []

# ===============================
# ФІЛЬТР ДЛЯ ВІДНОВЛЕННЯ СИГНАЛУ
# ===============================
F_filter = 10

w_filter = F_filter / (Fs / 2)

sos_filter = signal.butter(
    3,
    w_filter,
    'low',
    output='sos'
)

for Dt in Dt_values:

    # ===============================
    # ДИСКРЕТИЗАЦІЯ
    # ===============================
    discrete_signal = np.zeros(n)

    for i in range(0, n, Dt):
        discrete_signal[i] = filtered_signal[i]

    # ===============================
    # СПЕКТР
    # ===============================
    spec = fft.fft(discrete_signal)
    spec = np.abs(fft.fftshift(spec))

    # ===============================
    # ВІДНОВЛЕННЯ СИГНАЛУ
    # ===============================
    restored_signal = signal.sosfiltfilt(
        sos_filter,
        discrete_signal
    )

    # ===============================
    # ПОМИЛКА
    # ===============================
    error = restored_signal - filtered_signal

    # ===============================
    # ДИСПЕРСІЯ ТА SNR
    # ===============================
    var_signal = np.var(filtered_signal)
    var_error = np.var(error)

    variances.append(var_error)

    snr_values.append(
        var_signal / var_error
    )

    # ===============================
    # ГРАФІКИ
    # ===============================
    plot_graph(
        t,
        discrete_signal,
        f"Dt = {Dt}",
        "Час",
        "Амплітуда",
        f"discrete_{Dt}"
    )

    plot_graph(
        freqs,
        spec,
        f"Спектр Dt = {Dt}",
        "Частота",
        "Амплітуда",
        f"spectrum_{Dt}"
    )

    plot_graph(
        t,
        restored_signal,
        f"Відновлений Dt = {Dt}",
        "Час",
        "Амплітуда",
        f"restored_{Dt}"
    )

# ===============================
# ФІНАЛЬНІ ГРАФІКИ
# ===============================
plot_graph(
    Dt_values,
    variances,
    "Дисперсія",
    "Dt",
    "Дисперсія",
    "variance"
)

plot_graph(
    Dt_values,
    snr_values,
    "Сигнал/шум",
    "Dt",
    "SNR",
    "snr"
)

print("Практична робота 3 завершена!")

# ==================================================
# ПРАКТИЧНА РОБОТА №4 (ВАРІАНТ 1)
# Квантування сигналу
# ==================================================

levels = [4, 16, 64, 256]

variance_quant = []
snr_quant = []

for level in levels:

    # ===============================
    # МІНІМУМ І МАКСИМУМ СИГНАЛУ
    # ===============================
    signal_min = np.min(filtered_signal)
    signal_max = np.max(filtered_signal)

    # ===============================
    # КРОК КВАНТУВАННЯ
    # ===============================
    q_step = (
        signal_max - signal_min
    ) / level

    # ===============================
    # КВАНТУВАННЯ
    # ===============================
    quantized_signal = np.round(
        (filtered_signal - signal_min)
        / q_step
    ) * q_step + signal_min

    # ===============================
    # ПОМИЛКА
    # ===============================
    error = (
        quantized_signal
        - filtered_signal
    )

    # ===============================
    # ДИСПЕРСІЯ ТА SNR
    # ===============================
    var_signal = np.var(filtered_signal)
    var_error = np.var(error)

    variance_quant.append(var_error)

    snr_quant.append(
        var_signal / var_error
    )

    # ===============================
    # ГРАФІК СИГНАЛУ
    # ===============================
    plot_graph(
        t,
        quantized_signal,
        f"Квантований сигнал {level} рівнів",
        "Час",
        "Амплітуда",
        f"quantized_{level}"
    )

    # ===============================
    # СПЕКТР
    # ===============================
    spectrum_quant = fft.fft(
        quantized_signal
    )

    spectrum_quant = np.abs(
        fft.fftshift(spectrum_quant)
    )

    plot_graph(
        freqs,
        spectrum_quant,
        f"Спектр {level} рівнів",
        "Частота",
        "Амплітуда",
        f"spectrum_quant_{level}"
    )

    # ===============================
    # ВИВІД КОДІВ
    # ===============================
    print("\n=======================")
    print(f"Рівнів квантування: {level}")
    print("=======================")

    for i in range(20):

        value = quantized_signal[i]

        code = int(
            (value - signal_min) / q_step
        )

        bits = int(np.log2(level))

        binary = format(
            code,
            f'0{bits}b'
        )

        print(
            f"{i}: "
            f"{round(value, 2)} -> "
            f"{code} -> "
            f"{binary}"
        )

# ===============================
# ФІНАЛЬНІ ГРАФІКИ
# ===============================
plot_graph(
    levels,
    variance_quant,
    "Дисперсія квантування",
    "Кількість рівнів",
    "Дисперсія",
    "variance_quant"
)

plot_graph(
    levels,
    snr_quant,
    "Сигнал/шум квантування",
    "Кількість рівнів",
    "SNR",
    "snr_quant"
)

print("Практична робота 4 завершено!")