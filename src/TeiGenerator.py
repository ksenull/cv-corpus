import json

from lxml import etree
from lxml.builder import ElementMaker

if __name__ == '__main__':
    with open('../data/articles.json', 'r', encoding='utf8') as f:
        json_str = f.readlines()[0]
    articles = json.loads(json_str)

    E = ElementMaker()

    root = E.teiCorpus(xmlns="http://www.tei-c.org/ns/1.0")

    for title in articles:
        TEI = E.TEI(
            E.teiHeader(
                E.fileDesc(
                    E.titleStmt(
                        E.title(
                            title
                        )
                    )
                )
            ),
            E.text(
                E.body(
                    articles[title][0]
                )
            )
        )
        root.append(TEI)

    # print(etree.tostring(root, pretty_print=True, encoding='utf8').decode())
    etree.ElementTree(root).write('../data/tei.xml', pretty_print=True, encoding='utf8')