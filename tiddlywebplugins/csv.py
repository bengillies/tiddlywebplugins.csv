"""
A csv serialization for TiddlyWeb
"""
from __future__ import absolute_import
from tiddlyweb.serializations import SerializationInterface
from tiddlyweb.manage import make_command
from tiddlywebplugins.utils import get_store
from tiddlyweb.util import binary_tiddler
from tiddlyweb.store import StoreError
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler, string_to_tags_list
from uuid import uuid4

import sys
from csv import writer, DictReader

# XXX combine with header some?
CORE_TIDDLER_ATTRS = ['text', 'tags', 'type', 'modified', 'modifier']

class TiddlerWriter(object):
    """
    an object suitable for passing in to the csv writer
    """

    def __init__(self):
        self.output = ''

    def write(self, output):
        self.output += output


class Serialization(SerializationInterface):
    """
    turn a tiddler or a list of tiddlers into csv format
    """
    header = [
        'title',
        'text',
        'modified',
        'created',
        'modifier',
        'creator',
        'revision',
        'bag',
        'tags'
    ]

    def tiddler_as(self, tiddler):
        """
        turn a tiddler into a csv file
        """
        out = TiddlerWriter()
        csv_writer = writer(out)
        tiddler_header = self.header[:]
        fields = [f for f in tiddler.fields.iterkeys()]
        tiddler_body = self._tiddler_list(tiddler, fields)
        tiddler_header.extend(fields)
        tiddler_header = [h.encode('utf-8') for h in tiddler_header]

        csv_writer.writerow(tiddler_header)
        csv_writer.writerow(tiddler_body)

        return out.output

    def list_tiddlers(self, tiddlers):
        """
        Turn a list of tiddlers into csv format
        """
        out = TiddlerWriter()
        csv_writer = writer(out)
        tiddler_header = self.header[:]
        fields = []
        for t in tiddlers:
            fields.extend([f for f in t.fields.iterkeys() if fields.count(f) == 0])

        tiddler_rows = []
        for tiddler in tiddlers:
            tiddler_rows.append(self._tiddler_list(tiddler, fields))

        tiddler_header.extend(fields)
        tiddler_header = [h.encode('utf-8') for h in tiddler_header]
        csv_writer.writerow(tiddler_header)
        [csv_writer.writerow(tiddler) for tiddler in tiddler_rows]

        return out.output


    def _tiddler_list(self, tiddler, fields):
        """
        turn a tiddler into a list
        given the tiddler and a list of fields to include
        """
        def _handle_unicode(val):
            if isinstance(val, unicode):
                return val.encode('utf-8')
            else:
                return val

        tiddler_body = []
        for name in self.header:
            value = getattr(tiddler, name, '')
            if name == 'tags':
                value = self.tags_as(value)
            tiddler_body.append(_handle_unicode(value))

        for name in fields:
            value = tiddler.fields.get(name, '')
            tiddler_body.append(_handle_unicode(value))

        return tiddler_body



def init(config):
    config['serializers']['text/csv'] = ['tiddlywebplugins.csv', 'text/csv; charset=UTF-8']
    config['extension_types']['csv'] = 'text/csv'

    @make_command()
    def csvimport(args):
        """Import a csv file as tiddlers."""
        store = get_store(config)
        try:
            bag_name = args[0]
            bag = store.get(Bag(bag_name))
        except IndexError:
            usage('you must include a bag name')
        except StoreError:
            usage('bag %s does not exist' % bag_name)
        tiddler_reader = DictReader(sys.stdin)
        for tiddler_data in tiddler_reader:
            try:
                title = tiddler_data['title']
                del tiddler_data['title']
            except KeyError:
                title = str(uuid4())
            tiddler = Tiddler(title, bag_name)

            for key, value in tiddler_data.iteritems():
                if key is None:
                    continue
                if key == 'tags':
                    value = string_to_tags_list(value)
                if key in CORE_TIDDLER_ATTRS:
                    setattr(tiddler, key, value)
                else:
                    tiddler.fields[key] = value
                if binary_tiddler(tiddler):
                    try:
                        tiddler.text = b64decode(tiddler.text)
                    except TypeError, exc:
                        raise TiddlerFormatError(
                                'unable to decode b64 tiddler: %s: %s'
                                % (tiddler.title, exc))
            store.put(tiddler)
