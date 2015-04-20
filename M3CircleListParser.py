#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
M3WebsiteParser.py

M3 webのサークルリストをcsvに変換するスクリプト
"""

from HTMLParser import HTMLParser
import urllib2
import sys
import codecs


class M3CircleListParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_a = False
        self.is_td = False
        self.is_tbl = False
        self.is_space = False
        self.is_circle_name = False
        self.is_circle_desc = False
        self.href = None
        self.val = None
        self.data = []
        self.circle_data = []
        self.cur_data = {}
        
    def handle_starttag(self, tag, attr):
        if tag.lower() == 'table':
            for i in attr:
                if i[0].lower() == 'class' and i[1] == 'tblCircleList':
                    self.is_tbl = True
                    
        if self.is_tbl is True:
            if tag.lower() == 'td':
                self.is_td = True
                self.td_data = ''
                for i in attr:
                    if i[0].lower() == 'class' and i[1] == 'left':
                        self.is_space = True
                    if i[0].lower() == 'class' and i[1] == 'center':
                        self.is_circle_name = True
                    if i[0].lower() == 'class' and i[1] == 'right':
                        self.is_circle_desc = True
                        
        if self.is_circle_name is True:
            if tag.lower() == 'a':
                for i in attr:
                    if i[0].lower() == 'href':
                        self.href = i[1]
                    
    def handle_endtag(self, tag):
        if tag.lower() == 'a':
            self.is_a = False
            
        if tag.lower() == 'td':
            if self.is_space is True:
                self.td_data = self.td_data.strip()
                splitted = self.td_data.split('\t')
                self.floor = splitted[0]
                self.space = splitted[1]+splitted[2]
                self.is_space = False
                
            if self.is_circle_name is True:
                self.name = self.circle_data[0]
                self.circle_data = []
                self.is_circle_name = False
                
            if self.is_circle_desc is True:
                self.is_circle_desc = False
                self.cur_data['floor'] = self.floor
                self.cur_data['space'] = self.space
                self.cur_data['name'] = self.name
                self.cur_data['url'] = self.href
                self.cur_data['desc'] = self.desc
                
                self.data.append(self.cur_data)
                self.cur_data = {}
                self.href = None

            self.is_td = False
            self.td_data = ''
                
        if tag.lower() == 'table':
            if self.is_tbl == True:
                self.is_tbl = False
            
    def handle_data(self, data):
        if self.is_a is True:
            self.urldata = data
            
        if self.is_tbl is True:
            pass

        if self.is_td is True:
            self.td_data += '\t{}'.format( data.strip() )
            
        if self.is_circle_name is True:
            self.circle_data.append(data.strip())
            
        if self.is_circle_desc is True:
            self.desc = data.strip()
            
            
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python M3CircleListParser.py <output csv filename>')
        exit(-1)
        
    m3_url = 'http://www.m3net.jp/attendance/circle2015s.html'
    fid = urllib2.urlopen(m3_url)
    html = fid.read().decode('utf-8')
    
    parser = M3WebCircleListParser()
    parser.feed(html)
    
    fname_out = sys.argv[1]
    with codecs.open(fname_out, 'w', encoding='utf-8') as fo:
        for item in parser.data:
            out_str = '{0}\t{1}\t{2}\t{3}\n'.format(
                item['floor'],
                item['space'],
                item['name'],
                item['url']
            )
            fo.write(out_str)
