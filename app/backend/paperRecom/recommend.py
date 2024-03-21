import sys
sys.path.append('/app/backend')
sys.path.append('/app/backend/paperRecom')
from sklearn import preprocessing
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from paperRecom.util import extractTestPaperEmbeddings
from paperRecom.util import allPaperDataClass, testPaperDataClass
import abst_classify
import embedding
import json
import numpy as np
import subprocess

# def recommend(emb, paper_dict):

#     return emb


# def main():
#     input_abst = 'To augment datasets used for scientific-document writing support research, we extract texts from “Related Work” sections and citation information in PDF-formatted papers published in English. The previous dataset was constructed entirely with Tex-formatted papers, from which it is easy to extract citation information. However, since many publicly available papers in various fields are provided only in PDF format, a dataset constructed using only Tex papers has limited utility. To resolve this problem, we augment the existing dataset by extracting the titles of sections using the visual features of PDF documents and extracting the Related Work section text using the explicit title information. Since text generated from the figures and footnotes appearing in the extraction target areas is considered noise, we remove instances of such text. Moreover, we map the cited paper’s information obtained using existing tools to citation marks detected by regular expression rules, resulting in pairs of cited paper information and text of the Related Work section. By evaluating body text extraction and citation mapping in the constructed dataset, the accuracy of the proposed dataset was found to be close to that of the previous dataset. Accordingly, we demonstrated the possibility of building a significantly augmented dataset.'
#     recommend(input_abst, None, 'axcell')

def recommend(input_abst, year, event, title=''):
    # 入力アブストを分類
    abst_label_pairs = abst_classify.classify(input_abst)
    label_dict = abst_classify.abst_label_pair_to_label_dict(abst_label_pairs)
    # print(label_dict)

    # 入力アブストの埋め込みを作成
    label_emb = embedding.emb(abst_label_pairs, input_abst, title)
    # print(label_emb)

    # 推薦
    input = {
        'abst': input_abst,
        'label_dict' : label_dict, 
        'label_emb' : label_emb
    }
    if event == 'axcell':
        data_dir = "/dataserver/axcell/medium-pretrain_average_pooling"
    
    recommend_list = rank_list(data_dir, input)
    # print(recommend_list)
    return recommend_list, abst_label_pairs

def rank_list(data_dir, query):
    allPaperData = allPaperDataClass()

    """
    データファイルの読み込み
    """
    path = data_dir + "/paperDict.json"
    with open(path, 'r') as f:
        allPaperData.paperDict = json.load(f)

    path = data_dir + "/embLabel/labeledAbstSpecter.json"
    with open(path, 'r') as f:
        labeledAbstDict = json.load(f)

    """
    データの整形
    """
    labelList = ['title', 'bg', 'obj', 'method', 'res']

    for title, paper in allPaperData.paperDict.items():
        # Vectorizerに合うようにアブストラクトのみをリストに抽出
        allPaperData.abstList.append(paper["abstract"])

        # 分類されたアブストラクトごとにリストに抽出
        labelAbst = labeledAbstDict[paper["title"]]
        for label in labelList:
            allPaperData.labelList[label].append(labelAbst[label])

    # 辞書をリストに変換
    allPaperData.paperList = list(allPaperData.paperDict.values())

    # 推薦論文リストを生成
    # TF-IDF
    method = 'specter'
    if method == 'tf-idf':
        vectorizer = TfidfVectorizer()
        simMatrixDict = calcSimMatrixForLaveled(
            allPaperData, query['label_emb'], labelList, vectorizer=vectorizer)
        mergeSimMatrix = calcMergeSimMatrix(simMatrixDict, labelList)
    else:
        simMatrixDict = calcSimMatrixForLaveled(
            allPaperData, query['label_emb'], labelList)
    
    mergeSimMatrix = calcMergeSimMatrix(simMatrixDict, labelList)

    # 類似度が高い順にソートしてインデックスを取得
    sorted_indices = np.argsort(-mergeSimMatrix[0])

    # トップNの論文を推薦リストとして出力（ここではN=20）
    recommended_papers = []
    # for idx in sorted_indices[:20]:
    for idx in sorted_indices:
        recommended_papers.append({
            'title': allPaperData.paperList[idx]['title'],
            'abst': allPaperData.paperList[idx]['abstract'],
            "scoreOfSimilarity": mergeSimMatrix[0][idx],
            "labelScoreOfSimilarity": {
                "title": simMatrixDict['title'][0][idx],
                "bg": simMatrixDict['bg'][0][idx],
                "obj": simMatrixDict['obj'][0][idx],
                "method": simMatrixDict['method'][0][idx],
                "res": simMatrixDict['res'][0][idx],
                # "other": simMatrixDict['other'],
            }
        })

    return recommended_papers


"""
Class & Methods
"""
def calcSimMatrixForLaveled(allPaperData: allPaperDataClass, query_emb, labelList, vectorizer=None):
    # 背景、手法などの類似度を計算した行列を格納する辞書
    simMatrixDict = {v: [] for v in labelList}

    # TF-IDFやbowの計算を行う
    if vectorizer:
        # 全体の語彙の取得とTF-IDF(bow)の計算の実行、返り値はScipyのオブジェクトとなる
        # vectorizer.fit(allPaperData.abstList)
        vectorizer.fit(allPaperData.abstList + allPaperData.labelList['title'])

    for key in labelList:
        # (query_size, allData_size) 
        # そのラベルに分類された文章がないことで、ベクトルがNoneとなっているものを記憶しておく
        isNotNoneMatrix = np.ones(
            (1, len(allPaperData.paperList)))
        if vectorizer:
            tmpVectorList = []
            # ベクトルに変換
            for i, text in enumerate(allPaperData.labelList[key]):
                if text:
                    # ここで行列に変換されてしまうため[0]を参照する
                    vector = vectorizer.transform([text]).toarray().tolist()[0]
                else:
                    # cosine_simをまとめて計算するために、Noneではなく0(なんでもいい)を代入しておく
                    vector = [0]*len(vectorizer.get_feature_names_out())
                    # その場合のインデックスを覚えておく
                    isNotNoneMatrix[:, i] = 0
                tmpVectorList.append(vector)

            # TODO: queryのそのkey(label)に対応するアブストが無い場合
        else:
            tmpVectorList = allPaperData.labelList[key]

            # queryのそのkey(label)に対応するアブストが無い場合
            if query_emb[key] == None:
                isNotNoneMatrix = np.zeros(
                    (1, len(allPaperData.paperList)))
                query_emb[key] = [0]*768

            # 推薦候補の論文アブストにそのlabelに対応するアブストがない場合
            for i, vector in enumerate(tmpVectorList):
                if vector == None:
                    # cosine_simをまとめて計算するために、Noneではなく0(なんでもいい)を代入しておく
                    tmpVectorList[i] = [0]*768  # BERTの次元数
                    # その場合のインデックスを覚えておく
                    isNotNoneMatrix[:, i] = 0

        # TF-IDFやBOWの場合は疎行列となるため、csr_sparse_matrixに変換して速度を上げる
        if vectorizer:
            testPaperVectorList = csr_matrix(testPaperVectorList)
            tmpVectorList = csr_matrix(tmpVectorList)

        # simMatrix = euclidean_distances(testPaperVectorList, tmpVectorList)
        simMatrix = cosine_similarity([query_emb[key]], tmpVectorList)

        # 本来はテキストがなかったものをNanに変換する
        simMatrix = simMatrix*isNotNoneMatrix
        simMatrixDict[key] = np.where(simMatrix == 0, np.nan, simMatrix)

    return simMatrixDict


def calcMergeSimMatrix(simMatrixDict, labelList):
    # simMatrixDictのラベルごとの各要素で平均を取る
    mergeSimMatrix = np.zeros(
        (len(simMatrixDict[labelList[0]]), len(simMatrixDict[labelList[0]][0])))

    # 要素がnanでなければ1、nanなら0を立てた行列をラベル毎に格納した辞書
    notNanSimMatrixDict = {}
    for key in simMatrixDict:
        notNanSimMatrixDict[key] = np.where(np.isnan(simMatrixDict[key]), 0, 1)

    # nanでない要素数の合計をもとめる
    notNanSam = sum([notNanSimMatrixDict[key] for key in notNanSimMatrixDict])

    # 正規化
    for key in simMatrixDict:
        simMatrixDict[key] = preprocessing.scale(simMatrixDict[key], axis=1)

    # ndarrayの加算の都合上、simMatrixのnanを0に変換する
    for key in simMatrixDict:
        simMatrixDict[key] = np.where(
            np.isnan(simMatrixDict[key]), 0, simMatrixDict[key])

    # 全てのsimMatrixの要素の平均を出す
    # 手法1. 平均を出す
    mergeSimMatrix = sum([simMatrixDict[key]
                         for key in simMatrixDict]) / notNanSam
    # np.set_printoptions(threshold=np.inf)
    # print(notNanSam)
    # 手法2. 累乗してから足し合わせて平均を出す
    # mergeSimMatrix = sum([simMatrixDict[key]**5 for key in simMatrixDict]) / notNanSam
    # mergeSimMatrix = sum([simMatrixDict[key] for key in simMatrixDict]) / notNanSam

    return mergeSimMatrix


if __name__ == '__main__':
    main()