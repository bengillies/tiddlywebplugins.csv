"""
A csv serialization for TiddlyWeb
"""
from __future__ import absolute_import
from tiddlyweb.serializations import SerializationInterface

from csv import writer

class TiddlerWriter(object):
    """
    an object suitable for passing in to the csv writer
    """
    output = ''

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
