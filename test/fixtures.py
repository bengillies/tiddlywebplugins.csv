"""
Setup some tiddlers to test with
"""
test_tiddlers = [
    ('foo', """{
        "text": "Hello There!",
        "tags": ["foo", "bar", "baz"],
        "modifier": "bob",
        "fields": {
            "one": "1"
        }
    }"""),
    ('bar', """{
        "text": "Lorem Ipsum Dolor Sit \xe2\x99\xa5",
        "tags": ["foo baz", "biz", "bix"],
        "modifier": "alice",
        "fields": {
            "two": "2"
        }
    }"""),
    ('baz', """{
        "text": "Goodbye",
        "tags": [],
        "modifier": "Steve",
        "fields": {
            "one": "1",
            "three": "3"
        }
    }"""),
    ('biz', """{
        "text": "Some text, here",
        "tags": ["foo", "biz", "bix"],
        "modifier": "Bill",
        "fields": {
            "one": "1"
        }
    }"""),
]
