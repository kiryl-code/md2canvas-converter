import re


def parse_blocks(end: str, blocks: list[str]) -> list[str]:
    """
    Parses a content inside a custom markdown-block.
    :param end: a regular expression which can be used to identify the end of the block.
    :param blocks: a part of the document that should be parsed.
    :return: list of lines inside the block
    """
    content_blocks = []
    found_end = False
    consumed_blocks = 0

    for block_idx, block in enumerate(blocks):
        block_lines = block.split('\n')

        start_line = 1 if block_idx == 0 else 0

        current_block_lines = []
        for line_idx in range(start_line, len(block_lines)):
            if re.search(end, block_lines[line_idx]):
                found_end = True
                consumed_blocks = block_idx + 1
                break
            current_block_lines.append(block_lines[line_idx])

        if current_block_lines:
            content_blocks.append("\n".join(current_block_lines))

        if found_end:
            break

    if not found_end:
        raise ValueError("No end found")

    for _ in range(consumed_blocks):
        blocks.pop(0)

    return content_blocks
