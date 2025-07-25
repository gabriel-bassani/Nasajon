import pandas as pd
from dateutil.relativedelta import relativedelta

df = pd.DataFrame([
    {"cpf": "111", "matricula": "001", "nome": "Ana", "codigo_rubrica": "BONUS", "tipo_rubrica": "RENDIMENTO", "ano_calculo": 2023, "mes_calculo": 1, "valor": 500},
    {"cpf": "111", "matricula": "001", "nome": "Ana", "codigo_rubrica": "BONUS", "tipo_rubrica": "RENDIMENTO", "ano_calculo": 2023, "mes_calculo": 2, "valor": 0},
    {"cpf": "111", "matricula": "001", "nome": "Ana", "codigo_rubrica": "BONUS", "tipo_rubrica": "RENDIMENTO", "ano_calculo": 2024, "mes_calculo": 1, "valor": 500},
    {"cpf": "222", "matricula": "002", "nome": "Bruno", "codigo_rubrica": "INSS", "tipo_rubrica": "DESCONTO", "ano_calculo": 2024, "mes_calculo": 1, "valor": 300},
    {"cpf": "222", "matricula": "002", "nome": "Bruno", "codigo_rubrica": "INSS", "tipo_rubrica": "DESCONTO", "ano_calculo": 2024, "mes_calculo": 2, "valor": 305},
    {"cpf": "222", "matricula": "002", "nome": "Bruno", "codigo_rubrica": "INSS", "tipo_rubrica": "DESCONTO", "ano_calculo": 2024, "mes_calculo": 3, "valor": 450},
])

df["data"] = pd.to_datetime(df["ano_calculo"].astype(str) + "-" + df["mes_calculo"].astype(str) + "-01")

df = df.sort_values(["cpf", "codigo_rubrica", "data"])

alerts = []

rendimentos = df[df["tipo_rubrica"] == "RENDIMENTO"]

for (cpf, rubrica), group in rendimentos.groupby(["cpf", "codigo_rubrica"]):
    group = group[group["valor"] > 0] 
    group = group.sort_values("data")
    for i in range(1, len(group)):
        currentDate = group.iloc[i]["data"]
        previousDate = group.iloc[i-1]["data"]
        interval = relativedelta(currentDate, previousDate)
        difference = interval.years * 12 + interval.months
        if difference >= 6:
            alerts.append({
                "cpf": cpf,
                "rubrica": rubrica,
                "problema": f"Rendimento reapareceu após {difference} meses.",
                "data": currentDate.strftime("%Y-%m")
            })

discounts = df[df["tipo_rubrica"] == "DESCONTO"]

for (cpf, rubrica), group in discounts.groupby(["cpf", "codigo_rubrica"]):
    group = group.sort_values("data")
    group["media_ultimos"] = group["valor"].rolling(window=3, min_periods=2).mean()
    group["variacao_%"] = abs((group["valor"] - group["media_ultimos"]) / group["media_ultimos"]) * 100
    anomalias = group[group["variacao_%"] >= 5]
    for _, linha in anomalias.iterrows():
        alerts.append({
            "cpf": cpf,
            "rubrica": rubrica,
            "problema": f"Desconto variou {linha['variacao_%']:.1f}%",
            "data": linha["data"].strftime("%Y-%m")
        })

print("\nalerts:")
for alert in alerts:
    print(f"- [{alert['data']}] CPF {alert['cpf']} / Rubrica {alert['rubrica']}: {alert['problema']}")
