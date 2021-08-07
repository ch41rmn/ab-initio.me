import os
import typing
import sys
import re


def get_content() -> typing.List[str]:
    """Read body from stdin"""
    return sys.stdin.readlines()

def split_ref_section(lines: str) -> typing.Tuple[str, str]:
    """
    Extract references section (the last section) from a list of lines

    Returns (before, after)
    """
    # find the last line which starts with '#':
    ref_section = []
    for line in lines[::-1]:
        if not line.startswith('# '):
            ref_section.append(line)
        else:
            # this is the reference section heading. we can stop now
            break
    else:
        # we never found a title line?
        raise ValueError('Could not find Reference section')

    after = ref_section[::-1]
    before = lines[:-len(after)]

    return before, after


def make_references(references: typing.List[str]) -> typing.Tuple[typing.List[str], dict]:
    """
    Returns (lines, dict)
    - lines is re-created to render a list with proper hyperlinks
    - dict is a mapping of key "[i]": "([i])[#ref-x]"
    """
    out_lines = []
    out_dict = {}

    for line in references:
        pat = r'(\[[0-9]+\]) ([a-zA-Z0-9-_ ]+): (.*)'
        matched = re.match(pat, line)

        if not matched:
            out_lines.append(line)
            continue

        key, name, url = matched.group(1, 2, 3)
        tag = "ref-" + re.sub('[ _]', '-', name).lower()

        if key in out_dict:
            raise ValueError(f"Duplicate key found in reference: {key}")

        new_line = f'1. {name}: <a name="{tag}" href="{url}">{url}</a>'
        out_lines.append(new_line)
        out_dict[key] = f'[{key}](#{tag})'

    return out_lines, out_dict


def fix_body(lines: typing.List[str], ref_dict: dict) -> typing.List[str]:
    """Replaces unlinked references in text with actual references"""
    def sub_ref(matchobj):
        pre, matched, post = matchobj.group(1, 2, 3)
        if matched in ref_dict:
            return pre + ref_dict[matched] + post
        else:
            return matchobj.group(0)

    for line in lines:
        pat = r'([\. ])(\[[0-9]+\])([,;\. \n\)])'
        yield re.sub(pat, sub_ref, line)



def main():
    lines = get_content()
    before, after = split_ref_section(lines)
    new_after, new_tags = make_references(after)

    for line in fix_body(before, new_tags):
        print(line.rstrip())
    for line in new_after:
        print(line.rstrip())

    # print('\n'.join(new_after))
    # print(new_tags)


if __name__ == '__main__':
    main()

