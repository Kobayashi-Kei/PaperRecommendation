# PaperRecommendation

## 実行方法

1. サーバの起動

```
[ホスト側]
cd paper_recommendation
make up
make shell-flask

[flaskコンテナ側]
cd backend
# flaskサーバー起動（ただし，APIしか用意していないため，ブラウザからはAPIしか叩けない）
python3 app.py

# ここでもうひとつターミナルを起動
cd paper_recommendation
make shell-vue
cd vue
# vue起動
npm run dev
```

2. ブラウザからアクセス
   http://localhost:8080/
