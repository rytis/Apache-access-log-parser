#!/usr/bin/env python

from manager import Plugin
from operator import itemgetter
import GeoIP

class GeoIPStats(Plugin):

    def __init__(self, **kwargs):
        self.gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
        self.countries = {}

    def process(self, **kwargs):
        if 'remote_host' in kwargs:
            country = self.gi.country_name_by_addr(kwargs['remote_host'])
            if country in self.countries:
                self.countries[country] += 1
            else:
                self.countries[country] = 1

    def report(self, **kwargs):
        print "== Requests by country =="
        for (country, count) in sorted(self.countries.iteritems(), key=itemgetter(1), reverse=True):
            print " %10d: %s" % (count, country)
        

