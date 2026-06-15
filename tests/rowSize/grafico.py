import pandas as pd
import matplotlib.pyplot as plt

geral = pd.read_csv("resultados_gerais.csv")
fino = pd.read_csv("resultados_finos.csv")

# ==========================
# Determinar stride crítico
# ==========================

ratios = []

for i in range(1, len(geral)):
    ratios.append(
        geral["miss_rate"].iloc[i] /
        geral["miss_rate"].iloc[i - 1]
    )

idx = ratios.index(max(ratios)) + 1

stride_critico = int(geral["stride"].iloc[idx])

print()
print("===== RESULTADO =====")
print("Stride crítico =", stride_critico)
print("Linha de cache estimada =", stride_critico * 4, "bytes")
print()

# ==========================
# MISS RATE
# ==========================

plt.figure(figsize=(8,5))

plt.plot(
    geral["stride"],
    geral["miss_rate"],
    marker="o",
    color="blue",
    label="Varredura geral"
)

plt.plot(
    fino["stride"],
    fino["miss_rate"],
    marker="o",
    color="red",
    label="Refinamento"
)

plt.axvline(
    stride_critico,
    linestyle="--",
    color="black",
    label=f"Stride crítico = {stride_critico}"
)

plt.xscale("log", base=2)

plt.xlabel("Stride")
plt.ylabel("Miss Rate")
plt.title("Miss Rate da L1")
plt.grid(True, which="both")
plt.legend()

plt.savefig("miss_rate.png", dpi=300, bbox_inches="tight")
plt.close()

# ==========================
# TEMPO
# ==========================

plt.figure(figsize=(8,5))

plt.plot(
    geral["stride"],
    geral["time"],
    marker="o",
    color="blue",
    label="Varredura geral"
)

plt.plot(
    fino["stride"],
    fino["time"],
    marker="o",
    color="red",
    label="Refinamento"
)

plt.axvline(
    stride_critico,
    linestyle="--",
    color="black",
    label=f"Stride crítico = {stride_critico}"
)

plt.xscale("log", base=2)

plt.xlabel("Stride")
plt.ylabel("Tempo (s)")
plt.title("Tempo de execução")
plt.grid(True, which="both")
plt.legend()

plt.savefig("tempo.png", dpi=300, bbox_inches="tight")
plt.close()

print("Gerados:")
print("  miss_rate.png")
print("  tempo.png")
print("  para checar use 'getconf LEVEL1_DCACHE_LINESIZE'")