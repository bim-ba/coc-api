def toCamel(string: str, *, lower_first: bool = True):  # pylint: disable=invalid-name
    first, *others = string.split("_")
    if lower_first:
        return "".join([first.lower(), *map(str.title, others)])
    return "".join(word.capitalize() for word in [first, *others])


def shape_tag(tag: str):
    true_tag = tag.upper()
    return true_tag.replace("#", "%23")
