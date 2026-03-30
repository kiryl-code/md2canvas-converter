from markdown import Extension

from custom_processors import CodeblockPostProcessor, CollapsibleProcessor, LinkTreeProcessor


class ExtensionsRegister(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(CollapsibleProcessor(md.parser), 'collapsible', 175)
        md.treeprocessors.register(LinkTreeProcessor(md), 'links', 15)
        md.postprocessors.register(CodeblockPostProcessor(md), 'remove_code_tag', 5)
