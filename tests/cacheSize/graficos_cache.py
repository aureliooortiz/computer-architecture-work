import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.signal import find_peaks

geral = pd.read_csv("resultados.csv")
fino = pd.read_csv("resultados_finos.csv")

# =========================
# DATAFRAME COMBINADO
# =========================

todos = pd.concat([geral, fino], ignore_index=True)
todos = todos.sort_values("kb").reset_index(drop=True)

# =========================
# DETECÇÃO DE PICOS
# =========================

missrate = todos["miss_rate"].values

indices, _ = find_peaks(
    missrate,
    prominence=0.01,
    distance=2
)

pontos_criticos = [int(todos["kb"].iloc[i]) for i in indices]

# =========================
# ESTIMATIVA DAS CACHES
# =========================

# o tamanho da cache é o ponto anterior ao pico


caches = []

for i in indices:

    pico = todos["miss_rate"].iloc[i]
    limite  = pico -0.02 


    for j in range(i - 1, -1, -1):

        if todos["miss_rate"].iloc[j] <= limite:
            caches.append({
                "kb"     : int(todos["kb"].iloc[j]),
                "idx"    : j,
                "idx_pico": i
            })
            break

labels_cache = []
if len(caches) >= 1:
    labels_cache.append(("L1", caches[0]))
if len(caches) >= 2:
    labels_cache.append(("L3", caches[1]))

print("\n===== PONTOS CRÍTICOS =====")
for kb in pontos_criticos:
    print(f"{kb} KB")

print("\n===== ESTIMATIVA DE CACHES =====")
for label, c in labels_cache:
    print(f"{label}: ~{c['kb']} KB")

# =====================
# MISS RATE
# =====================

fig, ax = plt.subplots(figsize=(8, 5))

# fundo cinza: todos os dados combinados
ax.plot(
    todos["kb"],
    todos["miss_rate"],
    marker=".",
    color="gray",
    alpha=0.4,
    linewidth=0.8,
    label="Combinado"
)

# varredura geral
ax.plot(
    geral["kb"],
    geral["miss_rate"],
    marker="o",
    color="blue",
    label="Varredura geral"
)

# refinamento
if len(fino) > 0:
    ax.scatter(
        fino["kb"],
        fino["miss_rate"],
        marker="o",
        color="red",
        label="Refinamento"
    )

# linhas verticais amarelas nos picos
for kb in pontos_criticos:
    ax.axvline(
        kb,
        linestyle="--",
        color="goldenrod",
        linewidth=1.2,
        label="Pico" if kb == pontos_criticos[0] else ""
    )

# setas e labels para L1 e L3
for label, c in labels_cache:

    kb_cache = c["kb"]
    mr_cache = todos["miss_rate"].iloc[c["idx"]]

    ax.annotate(
        f"{label} ≈ {kb_cache} KB",
        xy=(kb_cache, mr_cache),
        xytext=(kb_cache, mr_cache + 0.03),
        arrowprops=dict(
            arrowstyle="->",
            color="black"
        ),
        fontsize=9,
        ha="center"
    )

ax.set_xscale("log", base=2)
ax.set_xlabel("Tamanho do vetor (KB)")
ax.set_ylabel("Miss Rate")
ax.set_title("Miss Rate vs Tamanho do vetor")
ax.grid(True, which="both")
ax.legend(loc="upper left")

plt.savefig(
    "miss_rate.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =====================
# TEMPO
# =====================

fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(
    todos["kb"],
    todos["time"],
    marker=".",
    color="gray",
    alpha=0.4,
    linewidth=0.8,
    label="Combinado"
)

ax.plot(
    geral["kb"],
    geral["time"],
    marker="o",
    color="blue",
    label="Varredura geral"
)

if len(fino) > 0:
    ax.scatter(
        fino["kb"],
        fino["time"],
        marker="o",
        color="red",
        label="Refinamento"
    )

ax.set_xscale("log", base=2)
ax.set_xlabel("Tamanho do vetor (KB)")
ax.set_ylabel("Tempo (s)")
ax.set_title("Tempo vs Tamanho do vetor")
ax.grid(True, which="both")
ax.legend(loc="upper left")

plt.savefig(
    "tempo.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nGerados:")
print("  miss_rate.png")
print("  tempo.png")