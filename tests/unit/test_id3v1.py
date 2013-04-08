#-*- coding: utf-8 -*-

from StringIO import StringIO

from hamcrest import *

from mp3hash import TaggedFile


MP3_ID3v1_NOT_TAGGED = '\n' * 128
MP3_ID3v1_TAGGED = 'TAG' + '\n' * (128 - 3)
MP3_ID3v1_TAGGED_AND_FILLED = '\n' * 512 + MP3_ID3v1_TAGGED


class TestID3v1(object):
    def test_detects_id3v1_tags(self):
        file = StringIO(MP3_ID3v1_TAGGED)

        tagged = TaggedFile(file)

        assert_that(tagged.has_id3v1)

    def test_detects_id3v1_tags_even_with_content(self):
        file = StringIO(MP3_ID3v1_TAGGED_AND_FILLED)

        tagged = TaggedFile(file)

        assert_that(tagged.has_id3v1)

    def test_detects_when_there_is_no_id3v1_tag(self):
        file = StringIO(MP3_ID3v1_NOT_TAGGED)

        tagged = TaggedFile(file)

        assert_that(not tagged.has_id3v1)

    def test_says_there_is_no_tag_when_file_is_too_small(self):
        file = StringIO()

        tagged = TaggedFile(file)

        assert_that(not tagged.has_id3v1)
