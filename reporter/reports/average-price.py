name = "average-price"
title = "Средняя цена по брендам"

def generate(data):
    if not data:
        return []

    sums = {}
    counts = {}
    for row in data:
        b = row["brand"] 
        p = float(row["price"]) 
        sums[b] = sums.get(b, 0.0) + p
        counts[b] = counts.get(b, 0) + 1

    result = [
        {"brand": b, "average_price": round(sums[b] / counts[b], 2)}
        for b in sums
    ]
    result.sort(key=lambda x: x["average_price"], reverse=True)
    return result