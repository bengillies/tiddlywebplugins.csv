"""
Tests serializing and deserializing with tiddlywebplugins.csv
"""
from fixtures import test_tiddlers
from tiddlyweb.serializer import Serializer
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.collections import Tiddlers
from tiddlyweb.config import config

from tiddlywebplugins.csv import Serialization as csv, init

def setup_module(module):
    init(config)
    module.environ = { 'tiddlyweb.config': config }
    serializer = Serializer('json')
    module.tiddlers = Tiddlers()
    for title, json in test_tiddlers:
        tiddler = Tiddler(title)
        serializer.object = tiddler
        serializer.from_string(json)
        module.tiddlers.add(tiddler)

def test_tiddler_to_csv():
    expected_string = 'title,text,modified,created,modifier,creator,revision,bag,tags,one\r\nfoo,Hello There!,20120202000000,20120202000000,bob,bob,0,,foo bar baz,1\r\n'
    serializer = Serializer('tiddlywebplugins.csv', environ=environ)
    tiddler = [t for t in tiddlers if t.title == 'foo'][0]
    serializer.object = tiddler
    string = serializer.to_string()

    assert string == expected_string

def test_unicode_tiddler_to_csv():
    expected_string = 'title,text,modified,created,modifier,creator,revision,bag,tags,two\r\nbar,Lorem Ipsum Dolor Sit \xe2\x99\xa5,20120202000000,20120202000000,alice,alice,0,,[[foo baz]] biz bix,2\r\n'
    serializer = Serializer('tiddlywebplugins.csv', environ=environ)
    tiddler = [t for t in tiddlers if t.title == 'bar'][0]
    serializer.object = tiddler
    string = serializer.to_string()

    assert string == expected_string

def test_tiddlers_to_csv():
    expected_string = 'title,text,modified,created,modifier,creator,revision,bag,tags,one,two,three\r\nfoo,Hello There!,20120202000000,20120202000000,bob,bob,0,,foo bar baz,1,,\r\nbar,Lorem Ipsum Dolor Sit \xe2\x99\xa5,20120202000000,20120202000000,alice,alice,0,,[[foo baz]] biz bix,,2,\r\nbaz,Goodbye,20120202000000,20120202000000,Steve,Steve,0,,,1,,3\r\nbiz,"Some text, here",20120202000000,20120202000000,Bill,Bill,0,,foo biz bix,1,,\r\n'
    serializer = Serializer('tiddlywebplugins.csv', environ=environ)
    string = serializer.list_tiddlers(tiddlers)

    output = string.split('\r\n')
    expected_output = expected_string.split('\r\n')
    for i in range(0,len(output)):
        assert output[i] == expected_output[i]
