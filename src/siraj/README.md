# 強化学習　トレードボット

## 注意点
- 入力データはsigmoid関数に変換しているので、0.5ばかりの配列になる。

## TODO
- いくらでいくつ注文を出したかをモデルの入力として使う。配列で渡す。現在の価格と引き算して、損益を配列に代入する。
- 注文数が100を超えないように、buy/sellの注文の数をモデルの入力として与える。100を超えた場合は、報酬で操作はせずに、100を超えたらbuyやsellがif文を通らないようにする
- buyの注文数が50に近くなった場合は、sellを多めに行う。

- 1回のsellの回数 = int(buy_num / 10)
- 1回のbuyの回数 = int(sell_num / 10)

- 300secおきのデータはあるが、60secおきのデータがない

