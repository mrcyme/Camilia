import ctags
from ctags import CTags, TagEntry
import sys

try:
    tagFile = CTags('tags')
except:
    sys.exit(1)

# Available file information keys:
#  opened -  was the tag file successfully opened?
#  error_number - errno value when 'opened' is false
#  format - format of tag file (1 = original, 2 = extended)
#  sort - how is the tag file sorted? 
#  author - name of author of generating program (may be empy string)
#  name - name of program (may be empy string)
#  url - URL of distribution (may be empy string)
#  version - program version (may be empty string)

print(tagFile["author"])

# Available sort type:
#  TAG_UNSORTED, TAG_SORTED, TAG_FOLDSORTED

# Note: use this only if you know how the tags file is sorted which is 
# specified when you generate the tag file
status = tagFile.setSortType(ctags.TAG_SORTED)