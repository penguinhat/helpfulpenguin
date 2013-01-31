from redirects.models import LiveRedirect

import random

VALID_WORDS = [
    'apple',
    'butter',
    'charlie',
    'ink',
    'king',
    'london',
    'monkey',
    'nuts',
    'orange',
    'pudding',
    'sugar',
    'uncle',
    'beer',
    'emma',
    'oranges',
    'pip',
    'queen',
    'robert',
    'essex',
    'york',
    'dog',
    'cat',
    'badger',
    'easy',
    'slow',
    'fox',
    'love',
    'item',
    'jig',
    'red',
    'yellow',
    'green',
    'blue',
    'white',
    'black',
    'purple',
    'bird',
    'judge',
    'pig',
    'bank',
    'book',
    'world',
    'time',
    'union',
    'snake',
]

MAX_TRIES = 20

TRIES_BEFORE_LENGTHEN = 5

class TooManyAttempts(Exception):
    pass

def get_unused_slug(length):
    """
    Returns a tuple of slug,list of words of at least <length> words (but possibly more)

    length must be < len(VALID_WORDS)

    Might throw TooManyAttempts Exception
    """

    if length > len(VALID_WORDS):
        raise ValueError('Length > Number of valid words!')

    attempts = 0

    while attempts < MAX_TRIES:

        words = random.sample(VALID_WORDS,length)
        slug = ''.join(words)

        queryset = LiveRedirect.objects.filter(slug=slug)

        if queryset.exists():
            attempts += 1

            if attempts % TRIES_BEFORE_LENGTHEN == 0:
                length = min(length+1,len(VALID_WORDS))
        else:
            return slug,words

    raise TooManyAttempts()