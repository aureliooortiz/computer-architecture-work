import pandas as pd

df = pd.read_csv("resultados_gerais.csv")

ratios = []

for i in range(1, len(df)):
    ratios.append(
        df["miss_rate"][i] /
        df["miss_rate"][i - 1]
    )

idx = ratios.index(max(ratios)) + 1

stride = int(df["stride"][idx])

anterior = int(df["stride"][idx - 1])

with open("regiao.txt", "w") as f:
    f.write(f"{anterior} {stride*2}\n")

print("Maior salto em:", stride)