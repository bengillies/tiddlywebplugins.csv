"""
Setup some tiddlers to test with
"""
test_tiddlers = [
    ('foo', """{
        "text": "Hello There!",
        "modified": "20120202000000",
        "created": "20120202000000",
        "tags": ["foo", "bar", "baz"],
        "modifier": "bob",
        "fields": {
            "one": "1"
        }
    }"""),
    ('bar', """{
        "text": "Lorem Ipsum Dolor Sit \xe2\x99\xa5",
        "modified": "20120202000000",
        "created": "20120202000000",
        "tags": ["foo baz", "biz", "bix"],
        "modifier": "alice",
        "fields": {
            "two": "2"
        }
    }"""),
    ('baz', """{
        "text": "Goodbye",
        "modified": "20120202000000",
        "created": "20120202000000",
        "tags": [],
        "modifier": "Steve",
        "fields": {
            "one": "1",
            "three": "3"
        }
    }"""),
    ('biz', """{
        "text": "Some text, here",
        "modified": "20120202000000",
        "created": "20120202000000",
        "tags": ["foo", "biz", "bix"],
        "modifier": "Bill",
        "fields": {
            "one": "1"
        }
    }"""),
]
