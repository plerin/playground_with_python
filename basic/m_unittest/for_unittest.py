import os


def add(a, b):
    return a + b


def substract(a, b):
    return a - b


def filelen(filename):
    f = open(filename, 'r')
    f.seek(0, os.SEEK_END)
    return f.tell()


def count_in_file(filename, char_to_find):
    count = 0
    f = open(filename, 'r')
    for word in f:
        for char in word:
            if char == char_to_find:
                count += 1
    return count
