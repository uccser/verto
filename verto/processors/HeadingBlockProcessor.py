from markdown.blockprocessors import BlockProcessor
from verto.utils.HeadingNode import DynamicHeadingNode
from verto.utils.HtmlParser import HtmlParser
import re


class HeadingBlockProcessor(BlockProcessor):
    ''' Searches a Document for markdown headings (e.g. # HeadingTitle)
    these are then processed into html headings and generates level
    trails for each.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: The VertoExtension object.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'heading'
        self.max_levels = 6
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.template = ext.jinja_templates[self.processor]
        self.custom_slugify = ext.custom_slugify
        self.level_generator = LevelGenerator(self.max_levels)
        self.roots = []
        self.current_node = None
        self.update_ext_tree = ext._set_heading_tree
        self.get_ext_tree = ext.get_heading_tree

    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            block: The block to be tested.

        Returns:
            True if the block matches the pattern regex of a HeadingBlock.
        '''
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        ''' Processes the block matching the heading and adding to the
        html tree and the verto heading tree.

        Args:
            parent: The parent node of the element tree that children
            will reside in.
            blocks: A list of strings of the document, where the
            first block tests true.
        '''
        block = blocks.pop(0)
        match = self.pattern.search(block)

        before = block[:match.start()]
        after = block[match.end():]

        if before:
            self.parser.parseBlocks(parent, [before])
        if after:
            blocks.insert(0, after)

        level = len(match.group('level'))
        heading = match.group('header').strip()
        heading_slug = self.custom_slugify(heading)
        level_trail = self.level_generator.next(level)

        context = dict()
        context['heading_level'] = level
        context['heading_type'] = 'h{0}'.format(level)
        context['title'] = heading
        context['title_slug'] = heading_slug
        for i, level_val in enumerate(level_trail):
            context['level_{0}'.format(i + 1)] = level_val

        html_string = self.template.render(context)
        parser = HtmlParser()
        parser.feed(html_string).close()
        parent.append(parser.get_root())

        self.add_to_heading_tree(heading, heading_slug, level)

    def add_to_heading_tree(self, heading, heading_slug, level):
        ''' Adds a new heading to the heading tree.

        Args:
            heading: A string of the heading title
            heading_slug: A string of the heading title as a slug
            level: the level of the heading
        '''
        if self.get_ext_tree() is None:  # We are likely on a new file
            self.roots = []
            self.current_node = None

        # Who is our parent node
        parent = self.current_node
        while parent is not None and level <= parent.level:
            parent = parent.parent

        # if we have no parent we are a new tree
        if parent is None and self.current_node is not None:
            # old tree is finished compile up and save
            root_node = self.current_node
            while root_node.parent is not None:
                root_node = root_node.parent
            self.roots.append(root_node.to_immutable())

        # Make our new node
        new_node = DynamicHeadingNode(title=heading, title_slug=heading_slug, level=level, parent=parent, children=[])
        if parent is not None:
            parent.children.append(new_node)

        # Find the current root node
        self.current_node = new_node
        root_node = self.current_node
        while root_node.parent is not None:
            root_node = root_node.parent

        # Update the extension tree
        self.update_ext_tree(tuple(self.roots + [root_node.to_immutable(), ]))


class LevelGenerator:
    ''' Generates a level trail for example (1, 2, 3) which might be
    interpretted as chapter 1, section 2 and subsection 3.
    '''

    def __init__(self, max_levels):
        '''
        Args:
            max_levels: The max number of levels for the generator to
            handle.
        '''
        self.level_list = [0 for _ in range(max_levels)]

    def next(self, level_inc):
        ''' Increments the level trail at the given level. This also
        zeros any levels after the incremented level.

        Args:
            level_inc: the level to be incremented.

        Returns:
            A tuple of levels, where higher levels are first and the
            lowest level is last.
        '''
        assert level_inc-1 < len(self.level_list)
        self.level_list[level_inc-1] += 1
        for index in range(level_inc, len(self.level_list)):
            self.level_list[index] = 0
        return tuple(self.level_list)
