#!/usr/bin/env python3
"""seoul_spots.csv から index.html を生成する"""
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).parent
CSV_PATH = HERE / "seoul_spots.csv"

spots = []
counters = {}
with open(CSV_PATH, newline="") as f:
    for i, row in enumerate(csv.DictReader(f)):
        area = row["エリア"].strip()
        counters[area] = counters.get(area, 0) + 1
        lat, lng = (float(x) for x in row["緯度経度"].split(","))
        spots.append(
            {
                "id": i,
                "no": counters[area],
                "area": area,
                "name": row["名前"].strip(),
                "category": row["カテゴリ"].strip(),
                "mealSlot": row["食事枠"].strip(),
                "hours": row["営業時間"].strip(),
                "memo": row["メモ"].strip(),
                "address": row["住所"].strip(),
                "lat": lat,
                "lng": lng,
            }
        )

template = (HERE / "template.html").read_text()
html = template.replace("__DATA__", json.dumps(spots, ensure_ascii=False, indent=2))
(HERE / "index.html").write_text(html)
print(f"index.html 生成: {len(spots)} スポット")
