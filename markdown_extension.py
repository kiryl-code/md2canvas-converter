import re
import xml.etree.ElementTree as eTree

from markdown.blockprocessors import BlockProcessor
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor

from markdown import Extension


class CollapsibleProcessor(BlockProcessor):
    """
    Processes custom expandable block syntax.
    """

    RE_START = r'^ *\^{4,}(.*)'
    RE_END = r'\^{4,}\s*$'

    def test(self, parent, block):
        return re.match(self.RE_START, block)

    def run(self, parent, blocks) -> bool | None:
        lines = blocks[0].split('\n')
        match = re.match(self.RE_START, lines[0])
        title_text = match.group(1).strip() if match else ""

        content_blocks = []
        found_end = False
        consumed_blocks = 0

        for block_idx, block in enumerate(blocks):
            block_lines = block.split('\n')

            start_line = 1 if block_idx == 0 else 0

            current_block_lines = []
            for line_idx in range(start_line, len(block_lines)):
                if re.search(self.RE_END, block_lines[line_idx]):
                    found_end = True
                    consumed_blocks = block_idx + 1
                    break
                current_block_lines.append(block_lines[line_idx])

            if current_block_lines:
                content_blocks.append("\n".join(current_block_lines))

            if found_end:
                break

        if not found_end:
            return False

        for _ in range(consumed_blocks):
            blocks.pop(0)

        details = eTree.SubElement(parent, 'details')
        summary = eTree.SubElement(details, 'summary')
        summary.text = title_text
        div = eTree.SubElement(details, 'div')
        div.set('class', 'collapsible-content')

        self.parser.parseBlocks(div, content_blocks)
        return True


class CodeblockPostProcessor(Postprocessor):
    """
    Modify codeblock HTML structure to match Canvas
    representation to avoid visual issues and enable proper
    styling.
    """

    def run(self, text: str) -> str:
        text = re.sub(r'<pre><span></span><code[^>]*>', '<pre>', text)
        text = text.replace('</code></pre>', '</pre>')
        return text


class LinkTreeProcessor(Treeprocessor):
    """
    Modify link processor to add ``inline_disabled`` class,
    which prevets Canvas from adding preview for e.g. YouTube videos.
    For the non-anchor links sets ``target`` attribute to ``_blank`` to
    open external links in a new tab.
    """

    def run(self, root):
        for a in root.iter('a'):
            classes = a.get('class')
            a.set('class', (classes + "inline_disabled").strip() if classes else "inline_disabled")
            link = a.get('href')
            if link and not link.startswith('#'):
                a.set('target', '_blank')
        return root


class ExtensionsRegister(Extension):
    """
    Register all custom extensions and overrides for Markdown package.
    """
    def extendMarkdown(self, md) -> None:
        """
        Register extensions and processors.
        :param md: Markdown instance
        """
        md.parser.blockprocessors.register(CollapsibleProcessor(md.parser), 'collapsible', 175)
        md.treeprocessors.register(LinkTreeProcessor(md), 'links', 15)
        md.postprocessors.register(CodeblockPostProcessor(md), 'remove_code_tag', 5)
