from flask import request, jsonify
import json
from datetime import datetime

def submit_scores():
    data = request.json
    date = data['date']  # フロントエンドから送信された日付を使用
    scores = data['scores']
    ranks = data['ranks']

    try:
        with open('results.json', 'r') as file:
            try:
                results = json.load(file)
            except json.JSONDecodeError:
                results = {}
    except FileNotFoundError:
        results = {}

    if date not in results:
        results[date] = []
    results[date].append({"scores": scores, "ranks": ranks})

    with open('results.json', 'w') as file:
        json.dump(results, file, indent=4)

    return jsonify(success=True)