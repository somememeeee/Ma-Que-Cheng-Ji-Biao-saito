from flask import render_template
import json
import matplotlib.pyplot as plt
import japanize_matplotlib  # これを追加
import os

def view():
  results = load_json('results.json')
  users = load_json('users.json')

  # データ整理
  prepared_data, total_scores, daily_totals,daily_average_rank,total_average_rank = prepare_data(results, users)
  
  # グラフ生成
  generate_graph(results)
  
  return render_template('view.html', data=prepared_data, total_scores=total_scores, users=users, daily_totals=daily_totals, daily_average_rank=daily_average_rank, total_average_rank=total_average_rank)

#各機能定義

def load_json(filename):
    with open(filename) as f:
        return json.load(f)

#ok
def prepare_data(results, users):
    prepared_data = {}
    total_scores = {player: 0 for player in users}  # 各プレイヤーの合計スコアを初期化
    daily_totals = {}  # 日付ごとの合計スコアを保存する辞書
    daily_ranks = {date: {player: [] for player in users} for date in results}  # 日付ごとの順位を保存する辞書
    total_ranks = {player: [] for player in users}  # 全期間の順位を保存する辞書

    for date, matches in results.items():
        prepared_data[date] = []
        daily_total = {player: 0 for player in users}  # その日の合計スコアを初期化
        for match in matches:
            prepared_data[date].append(match)
            for player_key, score in match["scores"].items():
                score_scaled = int(score * 10)  # スコアを10倍して整数に
                player = player_key.replace('Score', '')  # 'player1Score' を 'player1' に変換
                total_scores[player] += score_scaled  # 合計スコアを加算
                daily_total[player] += score_scaled  # その日の合計スコアを加算

                # 順位の追加
                rank = match["ranks"][player_key]
                daily_ranks[date][player].append(rank)
                total_ranks[player].append(rank)

        # その日の合計を10で割って元のスケールに戻す
        for player in daily_total:
            daily_total[player] = daily_total[player] / 10

        daily_totals[date] = daily_total  # その日の合計を保存

    # 日別平均順位の計算（小数点以下2桁に丸める）
    daily_average_rank = {
        date: {player: round(sum(ranks) / len(ranks), 2) for player, ranks in daily_ranks[date].items()}
        for date in daily_ranks
    }

    # 全期間平均順位の計算（小数点以下2桁に丸める）
    total_average_rank = {
        player: round(sum(ranks) / len(ranks), 2) for player, ranks in total_ranks.items()
    }


    # 全体の合計も10で割って元のスケールに戻す
    for player in total_scores:
        total_scores[player] = total_scores[player] / 10

    pd=prepared_data
    ts=total_scores
    dt=daily_totals
    dar=daily_average_rank
    tar=total_average_rank
    return pd,ts,dt,dar,tar 

    


def generate_graph(data):
  # プレイヤー名と対応する色を定義
  player_colors = {
      "player1": {"name": "あやと", "color": "red"},
      "player2": {"name": "かずと", "color": "blue"},
      "player3": {"name": "かいじ", "color": "green"},
      "player4": {"name": "なおき", "color": "yellow"}
  }

  # グラフのパスを設定し保存
  graph_path = 'static'  # 保存するパス
  graph_filename = 'static/points_graph.png'

  #グラフの画像ファイルが既に存在するか確認
  if os.path.exists(graph_filename):
  #画像ファイルが存在する場合は何もせずに終了
      return
  
  # プレイヤーごとのポイントを初期化
  player_points = {player: 0 for player in player_colors.keys()}

  plt.figure(figsize=(10, 6))
  plt.title("ポイント推移")
  plt.xlabel("試合数")
  plt.ylabel("縦ポイント")

  # 背景色を灰色に設定
  plt.gca().set_facecolor('lightgrey')

  for player, info in player_colors.items():
      scores = []
      match_count = 0  # 試合数をカウントする変数を追加
      for date in data.keys():
          for match in data[date]:
              # 試合ごとのポイントを加算
              player_points[player] += match["scores"][f"{player}Score"]
              scores.append(player_points[player])
              match_count += 1  # 試合数をカウントアップ
      plt.plot(range(1, match_count + 1), scores, label=info["name"], color=info["color"])

  plt.xticks(range(1, match_count + 1))  # x軸の刻みを1刻みで整数表示に設定
  plt.legend(loc="upper left")
  plt.grid(True, linestyle="--", alpha=0.7)

  plt.savefig(f'{graph_path}/points_graph.png')
  plt.close()