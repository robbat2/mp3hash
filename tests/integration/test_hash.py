#-*- coding: utf-8 -*-

import os
import zlib
import shutil
import hashlib

import mutagen

from hamcrest import *
from nose.tools import raises

from mp3hash import mp3hash

from tests.integration import SONG1_PATH, SONG2_PATH


SONG_SIZE = os.path.getsize(SONG1_PATH)

ALGORITHMS = ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')


class IdenticalFiles(object):
    @classmethod
    def setup_class(cls):
        shutil.copy(SONG1_PATH, SONG2_PATH)


class TestSameDataButNoTags(IdenticalFiles):
    @classmethod
    def setup_class(cls):
        shutil.copy(SONG1_PATH, SONG2_PATH)
        f = mutagen.File(SONG2_PATH)
        f.clear()
        f.save()


class HashOperations(object):
    def test_mp3hash(self):
        hash1 = mp3hash(SONG1_PATH)
        hash2 = mp3hash(SONG2_PATH)
        assert_that(hash1, is_(equal_to(hash2)))

    def test_algs(self):
        "Test generator for every algorithm"
        for alg in ALGORITHMS:
            yield self.check_algs, alg

    def check_algs(self, alg):
        hash1 = mp3hash(SONG1_PATH, hasher=hashlib.new(alg))
        hash2 = mp3hash(SONG2_PATH, hasher=hashlib.new(alg))
        assert_that(hash1, is_(equal_to(hash2)))

    def test_maxbytes_all(self):
        "Test generator for multiple sizes"
        for num in range(1, SONG_SIZE, 250 * 1024):
            yield self.check_num, num

    def check_num(self, maxbytes):
        hash1 = mp3hash(SONG1_PATH, maxbytes=maxbytes)
        hash2 = mp3hash(SONG2_PATH, maxbytes=maxbytes)

        assert_that(hash1, is_(equal_to(hash2)))

    @raises(ValueError)
    def test_maxbytes_negative(self):
        mp3hash(SONG1_PATH, maxbytes=-15)

    @raises(ValueError)
    def test_maxbytes_0(self):
        mp3hash(SONG1_PATH, maxbytes=-15)

    def test_hasher_protocol(self):
        class Adler32Hasher(object):
            def __init__(self):
                self.value = None

            def update(self, data):
                self.value = zlib.adler32(
                    data, *([self.value] if self.value is not None else [])
                ) & 0xffffffff

            def hexdigest(self):
                return hex(self.value)

        hasher = Adler32Hasher
        hash1 = mp3hash(SONG1_PATH, hasher=hasher())
        hash2 = mp3hash(SONG2_PATH, hasher=hasher())

        assert_that(hash1, is_(equal_to(hash2)))


class TestHashIdenticFile(IdenticalFiles, HashOperations):
    pass


class TestHashSameDataButNoTags(TestSameDataButNoTags, HashOperations):
    pass
