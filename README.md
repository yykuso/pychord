# Chord Network

## 仕様
main.pyを実行することによって，リング状のネットワークの生成・Stabilize処理を行う．

Nodeクラスはそのノードの接続情報を操る．

NetworkクラスはStabilizeのタイミングや所属する全Nodeの情報を保持してある．
このクラスは実際の実装の際は必要がないが，シミュレーションの仕様上作成した．

ノードの離脱に関しては実装が間に合わなかった．


## 動作環境

Python 2.7.15にて実行確認


## 実行方法

```python
python main.py
```

main.py ファイル内のnetwork.single_join(node_ip)の数を多くすればノード参加数が増える．
network.time_elapsed(times)の数を多くすれば，より時間が進みStabilizeがさせる．

Stabilizeはランダムで行われるので，回数を少なくすると正しいネットワークが出来上がらない．

ちなみにnode.single_join()は論文内でいう単一のノードしか同時に参加しない実装．



# pychord
