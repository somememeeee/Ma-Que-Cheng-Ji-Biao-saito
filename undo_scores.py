from flask import jsonify
import json

def undo_scores():
    try:
        # results.jsonファイルを読み込み
        with open('results.json', 'r') as file:
            results = json.load(file)

        # 最後の変更を元に戻す処理
        # ここでは単純化のために、最後の日付のデータを削除します。
        # 実際には、より複雑なロジックが必要になるかもしれません。
        if results:
            last_date = sorted(results.keys())[-1]
            if results[last_date]:
                results[last_date].pop()
                if not results[last_date]:  # 日付のデータが空になったらキーも削除
                    del results[last_date]

        # 変更を保存
        with open('results.json', 'w') as file:
            json.dump(results, file, indent=4)

        return jsonify({'success': True, 'message': 'Last submission undone.'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
