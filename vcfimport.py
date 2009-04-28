#!/usr/bin/env python
#
# Copyright (C) 2009 Anatol Ulrich, hypnocode
# au@hypnocode.net
# www.hypnocode.net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
sys.path.insert(0, './gdata-1.3.1/src')
sys.path.insert(0, './gdata-1.3.1/samples/calendar')

import os,vcard,calendarExample
from sys import argv
from ConfigParser import ConfigParser


class Adder(object):
    def __init__(self, user=None, pw=None, title=None):
        try:
            self.client = calendarExample.CalendarExample(user, pw) 
        except Exception, e:
            print e
            raise SystemExit
        self.title = title
    def add(self, vc):
        if self.client:
            event = self.client._InsertRecurringEvent(
            title=self.title % (vc.FN, vc.BDAY),
            content = '', 
            where = '',
            recurrence_data=birthday_data_from_vcard_info(vc.BDAY)
            )
        return

def argvconfig():
    return dict(vcffile = argv[1], username=argv[2], password=argv[3], event_text=argv[4])

def fileconfig(filename):
    config = ConfigParser()
    config.read("vcfimport.conf")
    config = dict(config.items(config.sections()[0]))
    return config


if len(argv) == 5:
    config = argvconfig()
else:
    if len(argv) == 2:
        configfile = argv[1]
    else:
        configfile = "vcfimport.conf"
    config = fileconfig(configfile)


vcffile = config.pop('vcffile')
adder = Adder(*config)
evils = []
for vc in vcard.load(vcffile):
    if vc.BDAY:
        print "%s: %s" % (vc.FN, vc.BDAY)
        #adder.add(vc)
    else:
        evils.append(vc)
#for evil in evils:
#    if hasattr(evil, 'FN'):
#        print "evil: " + evil.FN
#    else:
#        print "MEGA EVIL", evil
