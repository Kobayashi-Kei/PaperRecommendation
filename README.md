# PaperRecommendation

## 概要

論文の推薦を行うシステムです。ユーザーはブラウザからアクセスし、研究概要やアブストラクトを入力することで類似する論文リストを受け取ることができます．

このシステムは、Flask と Vue.js を使用して開発されています．

## 必要要件 (Requirements)

全て Docker コンテナを用いて動かすため，

- Docker
- Docker Compose

のみインストールしておく必要があります．

## 実行方法

1. サーバの起動

```
[ホスト側]
cd paper_recommendation
make build // 初回のみ
make up
make shell-flask

[コンテナ側(flask)]
cd backend
# flaskサーバー起動（ただし，APIしか用意していないため，ブラウザからはAPIしか叩けない）
python3 app.py

# もうひとつターミナルを起動
[ホスト側]
cd paper_recommendation
make shell-vue

[コンテナ側(vue)]
cd vue
# vueサーバー起動
npm run dev
```

2. ブラウザからアクセス
   http://localhost:8080/
