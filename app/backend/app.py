# render_templete：参照するテンプレートを指定
# jsonify：json出力（WebAPIの出力）
from flask import Flask, render_template, jsonify, request

# CORS：Ajaxのためのライブラリ
from flask_cors import CORS
from random import *

from paperRecom import paperRecommendation_entire

import json

app = Flask(__name__)

app.config.from_object(__name__)

CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch(path):
    return render_template("../paper-recommendation/index.html")


# '/rand'が叩かれた時、乱数を生成
@app.route('/rand')
def random():
    response = {
        'randomNum': randint(1,100)
    }
    return jsonify(response)

@app.route('/search', methods=['POST'])
# @app.route('/search', methods=['POST'])
def searchPaper():
    # app.logger.debug(request.get_json())
    
    debug = True
    if debug:
        # ダミーデータ
        with open('paperRecom/dammyPaperList.json') as f:
            response = json.load(f)
    
    else:
        # postで渡された検索クエリを受け取る
        query = request.get_json()['query']
        # 検索クエリで論文検索
        method = "tf-idf"
        response = paperRecommendation_entire.recom(method, query)

    print(response[:10])
    return jsonify(response[:10])

# app.run(host, port)：hostとportを指定してflaskサーバを起動
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
