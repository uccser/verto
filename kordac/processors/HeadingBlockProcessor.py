from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re

class HeadingBlockProcessor(BlockProcessor):
    ''' Searches a Document for markdown headings (e.g. # HeadingTitle) these are then processed into html headings and generates level trails for each.
    '''

    def __init__(self, ext, *args, **kwargs):
        '''
        Args:
            ext: The parent node of the element tree that children will reside in.
            args: Arguments handed to the super class.
            kwargs: Arguments handed to the super class.
        '''
        super().__init__(*args, **kwargs)
        self.processor = 'heading'
        self.max_levels = 6
        self.pattern = re.compile(ext.processor_info[self.processor]['pattern'])
        self.template = ext.jinja_templates[self.processor]
        self.custom_slugify = ext.custom_slugify
        self.level_generator = LevelGenerator(self.max_levels)
        
    def test(self, parent, block):
        ''' Tests a block to see if the run method should be applied.

        Args:
            parent: The parent node of the element tree that children will reside in.
            block: The block to be tested.

        Returns:
            True if the block matches the pattern regex of a HeadingBlock.
        '''
        return self.pattern.search(block) is not None

    def run(self, parent, blocks):
        ''' Increments the level trail at the given level. This also
        zeros any levels after the incremented level.

        Args:
            level_inc: the level to be incremented.

        Returns:
            A tuple of levels, where higher levels are first and the lowest
            level is last.
        '''
        block = blocks.pop(0)
        match = self.pattern.search(block)
        assert match is not None # If this is true how did we test successfully

        before = block[:match.start()]
        after = block[match.end():]

        if before:
            self.parser.parseBlocks(parent, [before])
        if after:
            blocks.insert(0, after)

        level = len(match.group('level'))
        heading = match.group('header').strip()
        level_trail = self.level_generator.next(level)

        context = dict()
        context['heading_level'] = level
        context['heading_type'] = "h{0}".format(level)
        context['title'] = heading
        context['title_slug'] = self.custom_slugify(heading)
        context.update(
            zip(("level_{0}".format(level) for level in range(1, self.max_levels + 1))
                , level_trail))

        html_string = self.template.render(context)
        node = etree.fromstring(html_string)
        parent.append(node)

class LevelGenerator:
    ''' Generates a level trail for example (1, 2, 3) which might be
    interpretted as chapter 1, section 2 and subsection 3.
    '''

    def __init__(self, max_levels):
        '''
        Args:
            max_levels: The max number of levels for the generator to handle.
        '''
        self.level_list = [0 for _ in range(max_levels)]

    def next(self, level_inc):
        ''' Increments the level trail at the given level. This also
        zeros any levels after the incremented level.

        Args:
            level_inc: the level to be incremented.

        Returns:
            A tuple of levels, where higher levels are first and the lowest
            level is last.
        '''
        assert level_inc-1 < len(self.level_list)
        self.level_list[level_inc-1] += 1
        for index in range(level_inc, len(self.level_list)):
            self.level_list[index] = 0
        return tuple(self.level_list)
