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

import re
import os.path
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta

def extend(l):
    if len(l) < 2: return [l[0], None]
    return l

def expand_packed(k):
    kvpairs = [kv for kv in k.split(";") if kv]
    return [extend(k.split("=",2)) for k in kvpairs ]

def packed_to_dict(packed):
    return dict(expand_packed(packed))

def packed_to_list(packed):
    return [l[0] for l in expand_packed(packed)]

def vcard_line_to_kvs(line):
    #print "line:", line
    kpacked, vpacked = line.split(":",1)
    #print "kp:"
    #print kpacked
    #print vpacked
    k = packed_to_dict(kpacked)
    v = packed_to_list(vpacked)
    #print "kv:", k, v
    return KV(k,v)

class KV(object):
    def __init__(self, k,v):
        encoding = "ISO-8859-1"
        if k.has_key("CHARSET"):
            encoding = k["CHARSET"]
        for kkey, kvalue in k.items():
            if kvalue is None:
                self.name = kkey
        self.k = k
        v = [item.decode(encoding) for item in v]
        self.v = v

class VCard(object):
    def __init__(self, lines):
        self.dict = {}
        for line in lines:
            if not line:
                continue
            try:
                kv = vcard_line_to_kvs(line)
                self.dict[kv.name] = kv
            except ValueError:
                print "oops",
                for char in line: print ord(char),
                print ""
    def __getitem__(self, key):
        if not attr in self.dict: return None
        return self.dict[key].v
    def __getattr__(self,attr):
        if not attr in self.dict: return None
        result = self.dict[attr].v
        if len(result) == 1: return result[0]
        return result

def load(vcf):
    raw_data = open(vcf, "r").read() 
    data = raw_data.replace("\r","")
    data = data.replace("BEGIN:VCARD\n","")
    data = data.replace("END:VCARD\n","")
    data = re.sub("VERSION:.*","",data)
    vcs = [VCard(vc.split("\n")) for vc in data.split("\n\n") if vc]
    return vcs

def make_kv_string(kname, kvalues, vvalues):
    return "%s:%s" % ( 
            [ [kname] + kvalues].join(";"),
            vvalues.join(";")
            )

def birthday_data_from_vcard_info(vcard_info):
    if (vcard_info is None) or (vcard_info == "0000-00-00"): return
    year, month, day = vcard_info.split("-")
    date_obj =  date_parser.parse(vcard_info)
    start_date = year+month+day
    end_date_obj = date_obj + relativedelta(days=1)
    end_date = "%s-%s-%s" % (end_date_obj.year, end_date_obj.month, end_date_obj.day)
    slot_string = ("DTSTART;VALUE=DATE:%s\r\n"
    + "DTEND;VALUE=DATE:%s\r\n"
    + "RRULE:FREQ=YEARLY;INTERVAL=1;BYMONTH=%i\r\n") % (
            start_date, end_date_obj, date_obj.month
            )

    return slot_string


if __name__ == "__main__":
    vcffile = "sample.vcf"
    for vc in load(vcffile):
        if vc.BDAY:
            print "%s: %s" % (vc.FN, vc.BDAY)
