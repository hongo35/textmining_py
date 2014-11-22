# -*- coding: utf-8 -*-
import MeCab

mecab = MeCab.Tagger()

node = mecab.parseToNode("今日もしないとね")
print node
