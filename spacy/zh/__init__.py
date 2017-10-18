from ..language import Language
from ..tokens import Doc


class Chinese(Language):
    lang = u'zh'

    def make_doc(self, text):
        import jieba
        words = list(jieba.cut(text, cut_all=False))
        words=[x for x in words if x]
        return Doc(self.vocab, words=words, spaces=[False]*len(words))
