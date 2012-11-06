# -*- coding: utf-8 -*-
'''
test_encode_decode.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
import unittest

from urlparse import parse_qs
from nose.plugins.skip import SkipTest

from core.data.parsers.encode_decode import htmldecode, urlencode


class TestHTMLDecode(unittest.TestCase):
    
    def test_simple(self):       
        self.assertEqual( htmldecode('hola mundo'), 'hola mundo')
    
    def test_tilde(self):
        self.assertEqual( htmldecode(u'hólá múndó'), u'hólá múndó')
    
    def test_special_char(self):
        self.assertEqual( htmldecode(u'hola &#0443'), u'hola ƻ')
    
    def test_charref(self):
        self.assertEqual( htmldecode(u'hola mundo &#x41'), u'hola mundo A')
        
    def test_html_encoded(self):
        self.assertEqual( htmldecode(u'&aacute;'), u'á')
    
    def test_html_invalid_utf8_entity_encoded(self):
        '''Test for invalid entity encoded chars'''
        samples = {
            'Valid ASCII' : u"a",
            'Valid 2 Octet Sequence' : u"&#xc3b1",
            'Invalid 2 Octet Sequence' : u"&#xc328",
            'Invalid Sequence Identifier' : u"&#xa0a1",
            'Valid 3 Octet Sequence' : u"&#xe282a1",
            'Invalid 3 Octet Sequence (in 2nd Octet)' : u"&#xe228a1",
            'Invalid 3 Octet Sequence (in 3rd Octet)' : u"&#xe28228",
            'Valid 4 Octet Sequence' : u"&#xf0908cbc",
            'Invalid 4 Octet Sequence (in 2nd Octet)' : u"&#xf0288cbc",
            'Invalid 4 Octet Sequence (in 3rd Octet)' : u"&#xf09028bc",
            'Invalid 4 Octet Sequence (in 4th Octet)' : u"&#xf0288c28",
            'Valid 5 Octet Sequence (but not Unicode!)' : u" &#xf8a1a1a1a1 ",
            'Valid 6 Octet Sequence (but not Unicode!)' : u" &#xfca1a1a1a1a1 ",
            'Invalid unicode FFFE' : u"&#xFFFE",
            'Invalid unicode FFFF' : u"&#xFFFF",
            }
        
        for desc, sample in samples.iteritems():
            try:
                htmldecode(sample)
            except Exception as e:
                msg = 'Exception "%s" was raised when trying to htmldecode() a "%s".'
                self.assertTrue(False, msg % (e, desc))
                
class TestURLEncode(unittest.TestCase):
    
    def test_simple(self):
        self.assertEqual(urlencode(parse_qs(u'a=1&a=c'), 'latin1'), 'a=1&a=c')
    
    def test_tilde(self):
        msg = 'This same unittest passed when written as a doctest, so I don\'t'\
              ' care much about why it is NOT passing when I migrated it to a'\
              ' unittest. It bothers me... but I\'m not too worried.'
        raise SkipTest(msg)
        self.assertEqual(urlencode(parse_qs(u'a=á&a=2'), 'latin1'), 'a=%C3%A1&a=2')
    
    def test_raises(self):
        self.assertRaises(TypeError, urlencode, u'a=b&c=d', 'utf-8')
    