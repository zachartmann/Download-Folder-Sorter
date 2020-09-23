# CREDIT Ben Samuel
# https://github.com/scooby/osx-tags/blob/master/osx_tags/__init__.py
# Adapted (made worse) for my personal taste. Check out the link for the real deal

from xattr import xattr
from biplist import writePlistToString, readPlistFromString

def tag_split(tag):
    parts = tag.rsplit('\n', 1)
    if len(parts) == 1:
        return parts[0], 0
    elif len(parts[1]) != 1 or parts[1] not in '0123456': # Not a color number
        return tag, 0
    else:
        return parts[0], int(parts[1])

def tag_nocolor(tag):
    return tag.rsplit('\n', 1)[0]

def tag_colored(tag, color):
    return '{}\n{}'.format(tag_nocolor(tag), color)

def tag_normalize(tag):
    tag, color = tag_split(tag)
    return tag_colored(tag, color)

class Tags(object):
    def __init__(self, fileish):
        self.xa = xattr(fileish)

    TAG_XATTRS = ('com.apple.metadata:_kMDItemUserTags', 'com.apple.metadata:kMDItemOMUserTags')

    def add(self, *tags):
        new_tags = self.read() | set(map(tag_normalize, tags))
        self.write(*tags)

    def read(self):
        tags = set()
        for key in self.TAG_XATTRS:
            try:
                plist = self.xa.get(key)
            except (OSError, IOError):
                pass
            else:
                tags.update(map(tag_normalize, readPlistFromString(plist)))
        return tags

    def write(self, *tags):
        tag_plist = writePlistToString(list(map(tag_normalize, tags)))
        for key in self.TAG_XATTRS:
            self.xa.set(key, tag_plist)
