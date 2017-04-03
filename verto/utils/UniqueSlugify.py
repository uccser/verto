from slugify import slugify
from math import log10, floor


class UniqueSlugify(object):
    ''' Wrapper for the python-slugify library enforcing unique slugs
    on each successive call.
    '''

    def __init__(self, uids=set(), occurance_separator='-', entities=True,
                 decimal=True, hexadecimal=True, max_length=0, word_boundary=False,
                 separator='-', save_order=False, stopwords=()):
                    '''
                    Args:
                        uids: A set of strings which are already taken as slugs.
                        Others: Passed directly to slugify.
                    '''
                    self.uids = set(uids)
                    self.occurance_separator = str(occurance_separator)
                    self.entities = bool(entities)
                    self.decimal = bool(decimal)
                    self.hexadecimal = bool(hexadecimal)
                    self.max_length = int(max_length)
                    self.word_boundary = bool(word_boundary)
                    self.separator = str(separator)
                    self.save_order = bool(save_order)
                    self.stopwords = tuple(stopwords)

    def __call__(self, text):
        '''
        Args:
            text: A string to be turned into a slug.
        Returns:
            A string which is a slug (as specified by slugify) that is unique.
        '''
        slug = slugify(text=text,
                       entities=self.entities,
                       decimal=self.decimal,
                       hexadecimal=self.hexadecimal,
                       max_length=self.max_length,
                       word_boundary=self.word_boundary,
                       separator=self.separator,
                       save_order=self.save_order,
                       stopwords=self.stopwords)
        count = 1
        new_slug = slug
        while new_slug in self.uids:
            count += 1
            end_index = len(slug)
            if self.max_length and (len(slug)
                                    + len(self.occurance_separator)
                                    + floor(log10(count))) >= self.max_length:
                end_index = self.max_length - floor(log10(count)) - len(self.occurance_separator) - 1
            new_slug = '{0}{1}{2}'.format(slug[:end_index], self.occurance_separator, count)
        self.uids.add(new_slug)
        return new_slug

    def add_uid(self, uid):
        '''
        Adds an externally used slug. (Useful to re-add a slug after a
        clear).
        Args:
            uid: A string which is already as a slug.
        '''
        self.uids.add(uid)

    def add_uids(self, uids):
        '''
        Adds externally used slugs. (Useful to re-add slugs after a
        clear).
        Args:
            uids: A set of strings which are already taken as slugs.
        '''
        self.uids.update(uids)

    def clear(self):
        '''
        Clears the known slugs used for uniqueness comparisons.
        '''
        self.uids = set()
