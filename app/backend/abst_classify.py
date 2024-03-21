import json
import subprocess
import nltk
import os

label_dict = {
    'background_label': 'bg',
    'objective_label': 'obj',
    'method_label': 'method',
    'result_label': 'res',
    'other_label': 'other',
}



def read_txt_and_convert_to_dict(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    data_list = []
    for line in lines:
        # 改行文字の除去とPythonのリストに変換
        parsed_line = eval(line.strip())

        sentences = parsed_line[1]

        for sentence, label in sentences:
            entry = [sentence, label_dict[label]]
            data_list.append(entry)

    return data_list

def abst_label_pair_to_label_dict(abst_label_pair):
    label_dict = {
        'bg' : '',
        'obj': '',
        'method': '',
        'res': '',
        'other': '',
    }

    for sentence, label in abst_label_pair:
        label_dict[label] = sentence
        
    return label_dict

def classify(abstract):
    dir_path = './sequential_sentence_classification/'
    # dir_path = './'
    model_path = "tmp_output_dir/model.tar.gz"
    input_path = "data/input.jsonl"
    output_path = "data/output.txt"

    sentences = nltk.sent_tokenize(abstract)
    jsonl_data = {"abstract_id": 0, "id": 1, "sentences": sentences}
    with open(dir_path + input_path, "w") as f:
        f.write(json.dumps(jsonl_data))

    # subprocessでコマンドを実行
    cmd = [
        "allennlp", "predict",
        model_path,
        input_path,
        "--include-package", "sequential_sentence_classification",
        "--predictor", "SeqClassificationPredictor",
        "--output-file", output_path
    ]
    print(cmd)

    subprocess.run(cmd, cwd='/app/backend/sequential_sentence_classification')

    output = read_txt_and_convert_to_dict(dir_path + output_path)
    print(output)

    os.remove(dir_path + input_path)
    os.remove(dir_path + output_path)

    return output


# test
# classify("I like an apple. He is Tom.")
