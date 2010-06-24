#!/usr/bin/env python

from manager import Plugin

class CountHTTP200(Plugin):

    def __init__(self, **kwargs):
        self.keywords = ['counter']
        self.counter_200 = 0
        self.counter_total = 0

    def process(self, **kwargs):
        if 'status' in kwargs:
            self.counter_total += 1
            if kwargs['status'] == '200':
                self.counter_200 += 1

    def report(self, **kwargs):
        print '== HTTP code 200 counter =='
        print "HTTP 200 responses: %d" % self.counter_200
        print "All responses: %d" % self.counter_total
