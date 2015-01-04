# -*- coding: utf8 -*-
from __future__ import unicode_literals
import unicodedata
from unidecode import unidecode
import re

import math


TAGS = 'adj adp adv conj det noun num pdt pos pron prt punct verb'.upper().split()


# Binary string features
def is_alpha(string):
    return string.isalpha()


def is_digit(string):
    return string.isdigit()


def is_punct(string):
    for c in string:
        if not unicodedata.category(c).startswith('P'):
            return False
    else:
        return True


def is_space(string):
    return string.isspace()


def is_ascii(string):
    for c in string:
        if ord(c) >= 128:
            return False
    else:
        return True


def is_title(string):
    return string.istitle()


def is_lower(string):
    return string.islower()


def is_upper(string):
    return string.isupper()


TLDs = set("com|org|edu|gov|net|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|"
        "name|pro|tel|travel|xxx|"
        "ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|"
        "bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|"
        "co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|"
        "fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|"
        "hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|"
        "km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|"
        "mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|"
        "nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|"
        "sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|ss|st|su|sv|sy|sz|tc|td|tf|tg|th|"
        "tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|"
        "wf|ws|ye|yt|za|zm|zw".split('|'))


def like_url(string):
    # We're looking for things that function in text like URLs. So, valid URL
    # or not, anything they say http:// is going to be good.
    if string.startswith('http://'):
        return True
    elif string.startswith('www.') and len(string) >= 5:
        return True
    # No dots? Not URLish enough
    if string[0] == '.' or string[-1] == '.' or '.' not in string:
        return False
    tld = string.rsplit('.', 1)[1].split(':', 1)[0]
    if tld.endswith('/'):
        return True

    if tld.isalpha() and tld in TLDs:
        return True
    return False


NUM_WORDS = set('zero one two three four five six seven eight nine ten'
                'eleven twelve thirteen fourteen fifteen sixteen seventeen'
                'eighteen nineteen twenty thirty forty fifty sixty seventy'
                'eighty ninety hundred thousand million billion trillion'
                'quadrillion gajillion bazillion'.split())
def like_number(string):
    string = string.replace(',', '')
    string = string.replace('.', '')
    if string.isdigit():
        return True
    if string.count('/') == 1:
        num, denom = string.split('/')
        if like_number(num) and like_number(denom):
            return True
    if string in NUM_WORDS:
        return True
    return False

# Statistics features
def oft_case(name, thresh):
    def wrapped(string, prob, case_stats, tag_stats):
        return string
    return wrapped


def can_tag(name, thresh=0.5):
    def wrapped(string, prob, case_stats, tag_stats):
        return string
    return wrapped


# String features
def canon_case(string, upper_pc=0.0, title_pc=0.0, lower_pc=0.0):
    if upper_pc >= lower_pc and upper_pc >= title_pc:
        return string.upper()
    elif title_pc >= lower_pc:
        return string.title()
    else:
        return string.lower()


def word_shape(string):
    length = len(string)
    shape = []
    last = ""
    shape_char = ""
    seq = 0
    for c in string:
        if c.isalpha():
            if c.isupper():
                shape_char = "X"
            else:
                shape_char = "x"
        elif c.isdigit():
            shape_char = "d"
        else:
            shape_char = c
        if shape_char == last:
            seq += 1
        else:
            seq = 0
            last = shape_char
        if seq < 4:
            shape.append(shape_char)
    return ''.join(shape)


def asciied(string):
    ascii_string = unidecode(string)
    if not ascii_string:
        return b'???'
    return ascii_string
