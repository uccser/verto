from collections import namedtuple


class HeadingNode(namedtuple('HeadingNode', 'title, title_slug, level, children')):
    ''' Represents a heading in the heading tree.

    Keyword arguments:
        title: the title of the current node.
        title_slug: the slug of the current node.
        level: the level of the current node.
        children: a tuple of HeadingNodes the level directly below the current node.
    '''


class DynamicHeadingNode(object):
    ''' Represents a heading in the heading tree.

    Keyword arguments:
        title: the title of the current node.
        title_slug: the slug of the current node.
        level: the level of the current node.
        parent: parent node of the current node.
        children: a list of DynamicHeadingNodes the level directly below the current node.
    '''

    def __init__(self, title, title_slug, level, parent, children):
        self.title = title
        self.title_slug = title_slug
        self.level = level
        self.parent = parent
        self.children = list(children)
        for child in self.children:
            child.parent = self

    def to_immutable(self):
        immutable_children = tuple(child.to_immutable() for child in self.children)
        return HeadingNode(title=self.title, title_slug=self.title_slug, level=self.level, children=immutable_children)
