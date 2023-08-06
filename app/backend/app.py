# render_templete：参照するテンプレートを指定
# jsonify：json出力（WebAPIの出力）
from flask import Flask, render_template, jsonify, request

# CORS：Ajaxのためのライブラリ
from flask_cors import CORS
from random import *

from paperRecom import paperRecommendation_entire

import json, datetime

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
    
    # postで渡された検索クエリを受け取る
    query = request.get_json()['query']

    debug = True
    if debug:
        # ダミーデータ
        with open('paperRecom/dammyPaperList.json') as f:
            response = json.load(f)
        
    else:
        # 検索クエリで論文検索
        method = "tf-idf"
        response = paperRecommendation_entire.recom(method, query)

    # ログを出力
    if not debug:
        logging(query, response)

    # print(response[:10])
    return jsonify(response[:10])

def logging(query, response, logDir='log/'):
    logDict = {
        'query': query,
        'response': response
    }
    outputPath = logDir + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.json'
    with open(outputPath, 'w') as f:
        json.dump(logDict, f, indent=4)

# app.run(host, port)：hostとportを指定してflaskサーバを起動
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
