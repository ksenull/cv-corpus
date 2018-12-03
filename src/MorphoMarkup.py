import json
import os
from spacy.lang.ru import Russian
from spacy_russian_tokenizer import RussianTokenizer, MERGE_PATTERNS
import nltk

ARTICLES_JSON_PATH = 'data/articles.json'


def tokenize():
    with open('data/articles.json', 'r', encoding='utf8') as f:
        json_str = f.readlines()[0]
    articles = json.loads(json_str)
    nlp = Russian()
    russian_tokenizer = RussianTokenizer(nlp, MERGE_PATTERNS)
    nlp.add_pipe(russian_tokenizer, name='russian_tokenizer')
    for title in articles:
        text = articles[title][0].strip()
        texts_count += 1
        sents = nltk.sent_tokenize(text, language="russian")
        sent_count += len(sents)
        tokens = nlp(text)
        words_count += len(tokens)
        symbols = [symb for symb in text if symb != ' ' and symb != '\n']
        symbols_count += len(symbols)