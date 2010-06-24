#!/usr/bin/env python

import csv
import re
import os
from manager import PluginManager

DIRECTIVE_MAP = {
                  '%h':  'remote_host',
                  '%l':  'remote_logname',
                  '%u':  'remote_user',
                  '%t':  'time_stamp',
                  '%r':  'request_line',
                  '%>s': 'status',
                  '%b':  'response_size',
                  '%{Referer}i':    'referer_url',
                  '%{User-Agent}i': 'user_agent',
                }


class LogLineGenerator:
    def __init__(self, log_format=None, log_dir='logs'):
        # LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
        if not log_format:
            self.format_string = '%h %l %u %t %r %>s %b %{Referer}i %{User-Agent}i'
        else:
            self.format_string = log_format
        self.log_dir = log_dir
        self.re_tsquote = re.compile(r'(\[|\])')
        self.field_list = []
        for directive in self.format_string.split(' '):
            self.field_list.append(DIRECTIVE_MAP[directive])
    
    def _quote_translator(self, file_name):
        for line in open(file_name):
            yield self.re_tsquote.sub('"', line)

    def _file_list(self):
        for file in os.listdir(self.log_dir):
            file_name = "%s/%s" % (self.log_dir, file)
            if os.path.isfile(file_name):
                yield file_name

    def get_loglines(self):
        for file in self._file_list():
            reader = csv.DictReader(self._quote_translator(file), fieldnames=self.field_list, delimiter=' ', quotechar='"')
            for line in reader:
                yield line

def main():
    plugin_manager = PluginManager()
    log_generator = LogLineGenerator()
    for log_line in log_generator.get_loglines():
        plugin_manager.call_method('process', args=log_line)
    plugin_manager.call_method('report')

if __name__ == '__main__':
    main()
