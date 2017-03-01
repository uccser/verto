from slugify import slugify
from math import log10, floor

class UniqueSlugify(object):
    def __init__(self, uids=set(), entities=True, decimal=True, hexadecimal=True, max_length=0, word_boundary=False, separator='-', save_order=False, stopwords=()):
        self.uids = set(uids)
        self.entities = bool(entities)
        self.decimal = bool(decimal)
        self.hexadecimal = bool(hexadecimal)
        self.max_length = int(max_length)
        self.word_boundary = bool(word_boundary)
        self.separator = str(separator)
        self.save_order = bool(save_order)
        self.stopwords = tuple(stopwords)

    def __call__(self, text):
        slug = slugify(text = text,
                        entities = self.entities,
                        decimal = self.decimal,
                        hexadecimal = self.hexadecimal,
                        max_length = self.max_length,
                        word_boundary = self.word_boundary,
                        separator = self.separator,
                        save_order = self.save_order,
                        stopwords = self.stopwords)
        count = 0
        new_slug = slug
        while new_slug in self.uids:
            count += 1
            end_index = len(slug)
            if self.max_length and (len(slug) + floor(log10(count))) >= self.max_length:
                end_index = len(slug) - floor(log10(count)) - 1
            new_slug = "{0}{1}".format(slug[:end_index], count)
        self.uids.add(new_slug)
        return new_slug

    def clear(self):
        uids = set()
