from redirects.models import LiveRedirect

import random

VALID_WORDS = [
    'ant',
    'apple',
    'awesome',
    'badger',
    'ball',
    'bank',
    'bat',
    'bear',
    'bee',
    'beer',
    'bird',
    'black',
    'blue',
    'book',
    'bus',
    'butter',
    'car',
    'cat',
    'charlie',
    'claw',
    'cow',
    'dad',
    'dave',
    'day',
    'dog',
    'duck',
    'easy',
    'egg',
    'empty',
    'essex',
    'fish',
    'fox',
    'frog',
    'full',
    'go',
    'goat',
    'gold',
    'green',
    'happy',
    'hat',
    'ink',
    'item',
    'jig',
    'judge',
    'king',
    'lake',
    'lava',
    'leaf',
    'lion',
    'london',
    'love',
    'map',
    'massive',
    'monkey',
    'moon',
    'nest',
    'nuts',
    'orange',
    'pie',
    'pig',
    'pip',
    'pudding',
    'purple',
    'queen',
    'red',
    'robot',
    'sad',
    'seal',
    'ship',
    'sky',
    'slow',
    'snake',
    'star',
    'stop',
    'sugar',
    'sun',
    'tank',
    'time',
    'tiny',
    'tree',
    'truck',
    'uncle',
    'union',
    'van',
    'vine',
    'whip',
    'white',
    'world',
    'worm ',
    'yellow',
    'york',
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