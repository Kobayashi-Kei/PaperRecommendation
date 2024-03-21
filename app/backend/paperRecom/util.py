
class PaperDataClass:
    def __init__(self):
        self.paperDict = {}
        self.paperList = []  # ランダムに論文を選択する都合上、数字のインデックスでアクセスできるようにリストも持っておく
        self.abstList = []
        self.abstEmbList = []
        self.labelList = {  # TF-IDFの処理の都合上、観点毎にリストに切り出す
            'title': [],
            'bg': [],
            'obj': [],
            'method': [],
            'res': [],
            'other': [],
        }


class allPaperDataClass(PaperDataClass):
    def __init__(self):
        super().__init__()
        self.testDataIndex = []
        self.titleToIndex = {}


class testPaperDataClass(PaperDataClass):
    def __init__(self):
        super().__init__()
        self.allDataIndex = []


def extractTestPaperEmbeddings(allPaperEmbeddingList, testPaperAllDataIndex):
    """
    allPaperDataをBOWやTF-IDFなどのベクトルに変換したリストから、testフラグが
    立っているデータを抜き出してtestPaperDataに代入して返す
    """
    testPaperEmbeddingList = []

    if type(allPaperEmbeddingList) != list:
        allPaperEmbeddingList = allPaperEmbeddingList.toarray()

    for i, paper_embedding in enumerate(allPaperEmbeddingList):
        if i in testPaperAllDataIndex:
            testPaperEmbeddingList.append(paper_embedding)

    return testPaperEmbeddingList

