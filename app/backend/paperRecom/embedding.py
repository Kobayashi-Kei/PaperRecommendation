# python module
import json
import traceback
import os
import time
import shutil
import glob

# torch
import torch

# transformers
from transformers import AutoTokenizer


import sys
sys.path.append('/specter/source/pytorch_lightning_training_script')
from pretrain_average_pooling import Specter

"""
SPECTER + Average Pooling を用いて、BERTの最終層の全ての出力を用いて
観点ごとの論文埋め込みを取得する
"""


def emb(abst_label_pairs, abst, title):
    modelParamPath = f"/dataserver/model_outputs/specter/pretrain_average_pooling/checkpoints" + "/*"

    # 用いる観点をリストで入力
    labelList = ["title", "bg", "obj", "method", "res"]

    # モデルパラメータのパス
    epoch = 1
    files = glob.glob(modelParamPath)
    for filePath in files:
        if f"ep-epoch={epoch}" in filePath:
            modelCheckpoint = filePath
            break

    # モデルのロード
    tokenizer = AutoTokenizer.from_pretrained('allenai/specter')
    model = Specter.load_from_checkpoint(modelCheckpoint)
    model.cuda()
    model.eval()

    # 処理
    # 出力用の辞書
    output_emb = {}

    # Title + [SEP] + Abstract
    title_abs = title + \
        tokenizer.sep_token + abst
    input = tokenizer(
        title_abs,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
        max_length=512
    )

    # input['input_ids'][0](トークナイズされた入力文)と同じ長さで、その位置のトークンのラベルを格納するリスト
    label_positions = [None for i in range(len(
        input['input_ids'][0].tolist()))]

    # titleの位置にラベルを格納する
    # SEPトークンの位置を特定する
    sep_pos = input['input_ids'][0].tolist().index(102)
    for i in range(1, sep_pos):
        label_positions[i] = 'title'
    # print(input['input_ids'][0].tolist())
    # print(sep_pos)
    # print(label_positions)
    # exit()

    # 各トークンの観点をlabel_positionsに格納
    for text_label_pair in abst_label_pairs:
        text = text_label_pair[0]
        label = text_label_pair[1]

        # 1文単位でtokenizeする
        tokenizedText = tokenizer(
            text,
            return_tensors="pt",
            max_length=512
        )
        # 先頭の101([CLS])と末尾の102([SEP])を取り除く
        tokenizedText_input_ids = tokenizedText['input_ids'][0][1:-1].tolist()
        # print(tokenizedText_input_ids)
        # exit()

        start, end = find_subarray(
            input['input_ids'][0].tolist(), tokenizedText_input_ids)
        for i in range(start, end+1):
            label_positions[i] = label
        # print(start, end)
        # print(label_positions)
    # print(input)

    # exit()
    # 各トークンをBERTに通す
    input = input.to('cuda:0')
    output = model.bert(**input)[0][0]

    # 観点ごとにBERT最終層出力を配列にまとめる
    label_last_hideen_state = {label: [] for label in labelList}
    for i, tensor in enumerate(output):
        # print(tensor)
        # [CLS]or [SEP]の時
        if label_positions[i] == None or label_positions[i] == "other":
            continue
        label_last_hideen_state[label_positions[i]].append(
            tensor.tolist())

    # 観点ごとのBERT出力でaverage pooling
    for label in labelList:
        if len(label_last_hideen_state[label]) == 0:
            output_emb[label] = None
            continue
        # print(label_last_hideen_state[label])
        # poolingInput = torch.tensor(
        #     label_last_hideen_state[label]).unsqueeze(0).to('cuda:0')
        poolingInput = torch.tensor(
            label_last_hideen_state[label]).to('cuda:0')
        out = poolingInput.mean(dim=0)
        # print(out)
        # print(out.size())
        # exit()
        # 出力用の辞書に格納
        output_emb[label] = out.tolist()
    
    return output_emb



def find_subarray(arr, subarr):
    n = len(arr)
    m = len(subarr)

    # サブ配列が配列に含まれるかどうかを調べる
    for i in range(n - m + 1):
        j = 0
        while j < m and arr[i + j] == subarr[j]:
            j += 1
        if j == m:
            return (i, i + m - 1)

    # サブ配列が配列に含まれない場合は None を返す
    return None


if __name__ == '__main__':
    main()
