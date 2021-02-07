#-*- coding: utf-8 -*-


def quotify(comment, username):
    """
    Converts 'Foo\nbar' to:
    @username
    > Foo
    > bar
    \n\n
    """
    header = "@%s" % username
    lines = comment.splitlines()
    quote = "\n> ".join(lines)
    quote = "%(header)s\n> %(quote)s\n\n" % ({'header': header, 'quote': quote})
    return quote