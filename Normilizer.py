import json
import os
import sys
from spacy.lang.ru import Russian
from spacy_russian_tokenizer import RussianTokenizer, MERGE_PATTERNS
import nltk

ARTICLES_JSON_PATH = 'data/articles.json'


def eprint(msg):
    sys.stderr(msg)


def join_nonempty(dir):
    nonempty_articles = {}
    articles_count = 0
    for filename in os.listdir(dir):
        print(filename)
    # for filename in ['0.json']:
        lines = []
        with open(os.path.join(dir, filename), 'r', encoding='utf8') as f:
            lines = f.readlines()
        assert len(lines) == 1
        articles = json.loads(lines[0])
        articles_count += len(articles)
        for title in articles:
            assert len(articles[title]) == 1
            if len(articles[title]) != 0 and len(articles[title][0]) != 0:
                nonempty_articles[title] = [*articles[title]]

    print(len(nonempty_articles))
    print(articles_count)

    json_str = json.dumps(nonempty_articles, ensure_ascii=False)
    with open(ARTICLES_JSON_PATH, 'w+', encoding='utf8') as f:
        f.write(json_str)


def count_simple_stats():
    with open('data/articles.json', 'r', encoding='utf8') as f:
        json_str = f.readlines()[0]
    articles = json.loads(json_str)
    nlp = Russian()
    russian_tokenizer = RussianTokenizer(nlp, MERGE_PATTERNS)
    nlp.add_pipe(russian_tokenizer, name='russian_tokenizer')
    texts_count = 0
    sent_count = 0
    words_count = 0
    symbols_count = 0
    for title in articles:
        text = articles[title][0].strip()
        texts_count += 1
        sents = nltk.sent_tokenize(text, language="russian")
        sent_count += len(sents)
        tokens = nlp(text)
        words_count += len(tokens)
        symbols = [symb for symb in text if symb != ' ' and symb != '\n']
        symbols_count += len(symbols)
        # print([token.txt for token in tokens])
    print("Texts count:", texts_count)
    print("Sentences count:", sent_count)
    print("Words count:", words_count)
    print("Symbols count:", symbols_count)


if __name__ == '__main__':
    backup_path = 'parsing_backup'
    # join_nonempty(backup_path)
    count_simple_stats()
