
import sys, os, shutil
from StringIO import StringIO

from tiddlyweb.config import config
from tiddlyweb.manage import handle
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler

from tiddlywebplugins.csv import init
from tiddlywebplugins.utils import get_store

def setup_module(module):
    if os.path.exists('store'):
        shutil.rmtree('store')
    init(config)
    module.savedin = sys.stdin
    module.store = get_store(config)
    module.store.put(Bag('bag1'))

def teardown_module(module):
    sys.stdin = module.savedin

def set_stdin(content):
    f = StringIO(content)
    sys.stdin = f

def test_one_simple_tiddler():
    set_stdin('title,text,modifier,tags,one\r\nfoo,Hello There!,bob,foo bar baz,1\r\n')
    handle(['', u'csvimport', u'bag1'])


    tiddler = Tiddler('foo', 'bag1')
    tiddler = store.get(tiddler)

    assert tiddler.title == 'foo'
    assert tiddler.text == 'Hello There!'
    assert sorted(tiddler.tags) == sorted(['foo', 'bar', 'baz'])
    assert tiddler.fields['one'] == '1'
    store.delete(tiddler)

def test_two_untitled_tiddlers():
    set_stdin("""alpha,beta,gamma,hotel
one,two,three,four
cat,dog,hamster,mouse""")
    handle(['', u'csvimport', u'bag1'])

    tiddlers = [store.get(tiddler) for tiddler
            in store.list_bag_tiddlers(Bag('bag1'))]

    assert len(tiddlers) == 2
    assert tiddlers[0].text == ''
    assert tiddlers[1].text == ''

    assert 'alpha' in tiddlers[0].fields
    assert 'beta' in tiddlers[1].fields
    
    assert (tiddlers[0].fields['alpha'] == 'one' or
        tiddlers[0].fields['alpha'] == 'cat')

