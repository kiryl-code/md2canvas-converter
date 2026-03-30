import re
import xml.etree.ElementTree as etree
from markdown.blockprocessors import BlockProcessor
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor


class CollapsibleProcessor(BlockProcessor):
    RE_START = r'^ *\^{4,}(.*)'
    RE_END = r'\^{4,}\s*$'

    def test(self, parent, block):
        return re.match(self.RE_START, block)

    def run(self, parent, blocks):
        lines = blocks[0].split('\n')
        match = re.match(self.RE_START, lines[0])
        title_text = match.group(1).strip() if match else ""

        content_lines = []
        found_end = False
        consumed_blocks = 0

        for block_idx, block in enumerate(blocks):
            block_lines = block.split('\n')

            start_line = 1 if block_idx == 0 else 0

            for line_idx in range(start_line, len(block_lines)):
                if re.search(self.RE_END, block_lines[line_idx]):
                    content_lines.extend(block_lines[start_line:line_idx])
                    found_end = True
                    consumed_blocks = block_idx + 1
                    break

            if found_end:
                break

            content_lines.extend(block_lines[start_line:])
            content_lines.append("")

        if not found_end:
            return False

        for _ in range(consumed_blocks):
            blocks.pop(0)

        details = etree.SubElement(parent, 'details')
        summary = etree.SubElement(details, 'summary')
        summary.text = title_text
        div = etree.SubElement(details, 'div')
        div.set('class', 'collapsible-content')

        self.parser.parseBlocks(div, ["\n".join(content_lines)])

        return True

class CodeblockPostProcessor(Postprocessor):
    def run(self, text):
        text = re.sub(r'<pre><span></span><code[^>]*>', '<pre>', text)
        text = text.replace('</code></pre>', '</pre>')
        return text

class LinkTreeProcessor(Treeprocessor):
    def run(self, root):
        for a in root.iter('a'):
            classes = a.get('class')
            a.set('class', (classes + "inline_disabled").strip() if classes else "inline_disabled")
            link = a.get('href')
            if not link.startswith('#'):
                a.set('target', '_blank')
        return root