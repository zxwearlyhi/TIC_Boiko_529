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

# ===============================
# ПРАКТИЧНА 4
# ===============================

levels = [4, 16, 64, 256]

variance_quant = []
snr_quant = []

for level in levels:

    # минимум и максимум сигнала
    signal_min = np.min(filtered_signal)
    signal_max = np.max(filtered_signal)

    # шаг квантования
    q_step = (signal_max - signal_min) / level

    # квантование
    quantized_signal = np.round(
        (filtered_signal - signal_min) / q_step
    ) * q_step + signal_min

    # ошибка
    error = quantized_signal - filtered_signal

    # дисперсия и SNR
    var_signal = np.var(filtered_signal)
    var_error = np.var(error)

    variance_quant.append(var_error)
    snr_quant.append(var_signal / var_error)

    # ===============================
    # ГРАФИК КВАНТОВАННОГО СИГНАЛА
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
    spectrum_quant = fft.fft(quantized_signal)
    spectrum_quant = np.abs(fft.fftshift(spectrum_quant))

    plot_graph(
        freqs,
        spectrum_quant,
        f"Спектр {level} рівнів",
        "Частота",
        "Амплітуда",
        f"spectrum_quant_{level}"
    )

    # ===============================
    # ВЫВОД ТАБЛИЦЫ
    # ===============================
    print("\n=======================")
    print(f"Рівнів квантування: {level}")
    print("=======================")

    print("Перші 20 значень:")

    for i in range(20):

        value = quantized_signal[i]

        # код числа
        code = int((value - signal_min) / q_step)

        # количество бит
        bits = int(np.log2(level))

        # перевод в двоичный код
        binary = format(code, f'0{bits}b')

        print(
            f"{i}: "
            f"{round(value, 2)} -> "
            f"{code} -> "
            f"{binary}"
        )

# ===============================
# ФИНАЛЬНЫЕ ГРАФИКИ
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

print("\nПрактична 4 завершено!")