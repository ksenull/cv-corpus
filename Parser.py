from lxml import etree
import dewiki
import os
import json

BACKUP_FREQUENCY = 200


def backup(dict):
    def remove_json_ext(filename):
        assert filename[-5:] == '.json'
        return filename[:-5]
    backup_dir = 'parsing_backup'
    files = [int(remove_json_ext(x)) for x in os.listdir(backup_dir)]
    filename = str(len(files)) + '.json'

    json_str = json.dumps(dict, ensure_ascii=False)
    print(json_str)
    with open(os.path.join(backup_dir, filename), 'w+', encoding='utf8') as f:
        f.write(json_str)


def clear_tables(text, start_symbol='{', end_symbol='}'):
    isTable = False
    res = []
    for i, c in enumerate(text):
        if c == start_symbol:
            isTable = True
        elif isTable:
            if c == end_symbol and (i == len(text) - 1 or text[i+1] != end_symbol):
                isTable = False
        else:
            res.append(c)
    return ''.join(res)


def clear_refs(text, start_ref='<ref>', end_ref='</ref>'):
    res = []
    tokens = text.split(start_ref)
    for i, token in enumerate(tokens):
        if i == 0:
            res.extend([*token])
        else:
            end = token.find(end_ref)
            res.extend([*token[end + len(end_ref):]])
    return ''.join(res)


def clear_bottom_links(text, keyword='Каçăсем'):
    tokens = text.split(keyword)
    tokens = tokens[:-1]
    return keyword.join(tokens)


def parseXML(xmlFile):
    """
    Парсинг XML
    """
    with open(xmlFile, encoding='utf8') as fobj:
        xml = fobj.read()
    print("Start to parse")
    root = etree.fromstring(xml)
    articles = {}
    for i, page in enumerate(root.getchildren()):
        print(i)
        title = None
        for elem in page.getchildren():
            if elem.tag.endswith('title') and elem.text:
                title = elem.text
                print(title)
            if elem.tag.endswith('revision'):
                for child in elem.getchildren():
                    if child.tag.endswith('text') and child.text:
                        text = dewiki.from_string(child.text)
                        # text = unwiki.loads(child.text)
                        text = clear_tables(text)
                        text = clear_refs(text)
                        text = clear_bottom_links(text)
                        text = clear_bottom_links(text, keyword='Вуламалли')
                        text = clear_bottom_links(text, keyword='Асăрхавсем')
                        # print(text)
                        if title in articles:
                            articles[title].append(text)
                        else:
                            articles[title] = [text]
        if i != 0 and i % BACKUP_FREQUENCY == 0:
            backup(articles)
            articles = {}
    # print(articles)
    backup(articles)


if __name__ == "__main__":
    parseXML("cvwiki-20181120-pages.xml")
