name = "average-rating"
title = "Средний рейтинг по брендам"

def generate(data):
    if not data:
        return []

    sums = {}
    counts = {}
    for row in data:
        b = row["brand"] 
        r = float(row["rating"])
        sums[b] = sums.get(b, 0.0) + r
        counts[b] = counts.get(b, 0) + 1

    result = [
        {"brand": b, "average_rating": round(sums[b] / counts[b], 2)}
        for b in sums
    ]
    result.sort(key=lambda x: x["average_rating"], reverse=True)
    return result