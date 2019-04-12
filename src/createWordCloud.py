# coding:utf-8
# 実行例
# python createWordCloud.py \
#     /path/to/a6s-cloud-batch/test_data/tweet1.txt \
#     /path/to/RictyDiminished/RictyDiminished-Bold.ttf \
#     /path/to/a6s-cloud-batch/output/wordcloud_sample1.png

import csv
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from wordcloud import WordCloud
import sys

args = sys.argv

# 形態素解析
def MorphologicalAnalysis(texts):
    a = Analyzer(token_filters=[CompoundNounFilter()])
    words_count = defaultdict(int)
    words = []

    for text in texts:
        tokens = a.analyze(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos in ['名詞','形容詞']:
                words_count[token.base_form] += 1
                words.append(token.base_form.strip("@").strip("#").strip(":").strip("\""))
    return words_count, words

def main():
    if(len(args) != 4):
        print("引数が不正です")
        exit()

    with open(args[1], 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        texts = []
        for row in reader:
            if(len(row) > 0):
                text = row[0].split('http')
                texts.append(text[0])

    words_count, words = MorphologicalAnalysis(texts)
    text = ' '.join(words)

    # pathは環境に合わせる必要がある
    fpath = args[2]
    
    #ストップワードを設定
    stop_words = [u"こと", u"よう", u"そう", u"これ", u"それ",u"みたい",u"ため",u"やつ",u"さん",u"RT",u"ない",u"ほど",]
    
    # WordCloud処理
    wordcloud = WordCloud(min_font_size=5, collocations=False, background_color="white",
                        font_path=fpath, width=900, height=500,stopwords=set(stop_words),max_words=300).generate(text)

    # 画像出力
    wordcloud.to_file(args[3])

main()
