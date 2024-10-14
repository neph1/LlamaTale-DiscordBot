


def format_text(html: str) -> str:
    """Format HTML text to discord markdown."""
    html = html.replace('<br>', '\n')
    html = html.replace('<p>', '')
    html = html.replace('</p>', '\n')
    html = html.replace('<b>', '**')
    html = html.replace('</b>', '**')
    html = html.replace('<i>', '*')
    html = html.replace('</i>', '*')
    html = html.replace('<u>', '__')
    html = html.replace('</u>', '__')
    html = html.replace('<s>', '~~')
    html = html.replace('</s>', '~~')
    html = html.replace('<code>', '`')
    html = html.replace('</code>', '`')
    html = html.replace('<pre>', '```')
    html = html.replace('</pre>', '```')
    return html