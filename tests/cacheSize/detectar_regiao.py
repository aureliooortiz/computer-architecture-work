import pandas as pd
from scipy import stats

geral = pd.read_csv("resultados.csv")

# ── detector de picos (z-score na derivada) ──────────────────────────────────
diffs = geral["miss_rate"].diff().fillna(0)
z = stats.zscore(diffs)
pontos = list(geral.index[z > 1.5])

# ── gerador de candidatos de cache ───────────────────────────────────────────

def cache_candidates(kb_prev, kb_curr):
    """
    Retorna potências de 2 e seus múltiplos (1x, 1.5x, 2x, 3x)
    que estejam dentro ou perto do intervalo [kb_prev, kb_curr].
    Inclui 1 ponto fora de cada lado pra garantir cobertura.
    """
    candidates = set()

    # gera potências de 2 de 4 KB até 131072 KB (128 MB)
    pot = 4
    while pot <= 131072:
        # também considera 1.5x a potência (ex: 48, 96, 192...)
        for mult in [1, 1.5, 2, 3]:
            v = int(pot * mult)
            candidates.add(v)
        pot *= 2

    # filtra os que estão no intervalo, mais 1 vizinho de cada lado
    dentro = sorted(c for c in candidates if kb_prev <= c <= kb_curr)

    if not dentro:
        # intervalo muito pequeno, pega os mais próximos
        abaixo = max((c for c in candidates if c < kb_prev), default=None)
        acima  = min((c for c in candidates if c > kb_curr), default=None)
        dentro = [x for x in [abaixo, acima] if x is not None]

    # 1 vizinho antes do primeiro e depois do último
    todos = sorted(candidates)
    idx_first = todos.index(dentro[0])  if dentro[0]  in todos else -1
    idx_last  = todos.index(dentro[-1]) if dentro[-1] in todos else -1

    result = set(dentro)
    if idx_first > 0:
        result.add(todos[idx_first - 1])   # 1 antes
    if idx_last >= 0 and idx_last + 1 < len(todos):
        result.add(todos[idx_last + 1])    # 1 depois

    return sorted(result)


# ── saída ─────────────────────────────────────────────────────────────────────
print("\n===== PONTOS CRÍTICOS =====")

regioes = set()

with open("regioes.txt", "w") as f:
    for idx in pontos:
        anterior = int(geral["kb"].iloc[idx - 1])
        atual    = int(geral["kb"].iloc[idx])

        print(f"{anterior} KB -> {atual} KB")

        vals = cache_candidates(anterior, atual)

        for v in vals:
            f.write(f"{v}\n")
            regioes.add(v)

print("\nRegiões geradas (ordenadas):")
print(sorted(regioes))