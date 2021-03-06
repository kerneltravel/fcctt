#!/usr/bin/env python
#coding:utf-8

# by Li.Ci dyspneacn@gmail.com
# date	Sat, Mar 5, 2011 at 11:42 AM
# 自动分析sla文件有多少页，并把sla中的文本内容按页分割开

import HTMLParser
import sys

class SLAParser(HTMLParser.HTMLParser):
    
    data=[]
    flag=False
    handledtags=['pageobject','itext']
    taglevels=[] 
    atext = ''
    position = -1

    
    def __init__(self):        
        HTMLParser.HTMLParser.__init__(self)
    
    def handle_starttag(self,tag,attrs):
        if len(self.taglevels) and self.taglevels[-1]==tag :          
            self.handle_endtag(tag)
            
        
        self.taglevels.append(tag)  
        if tag== 'document' : 
            for key,value in attrs:
                if key == 'anzpages':
                    self.data=['']*int(value)
            
        if tag == 'pageobject':

            for key,value in attrs:
                if key=='ownpage':
                    self.position=int(value)

                    
        if tag == 'itext':
            for key,value in attrs:
                if key == 'ch':
                    self.atext=self.atext+value
                    
    def handle_endtag(self,tag):
        if not tag in self.taglevels:
            return 
        
        while len(self.taglevels):
            starttag=self.taglevels.pop()
            if tag == 'pageobject' and len(self.atext) and self.position>-1:               
                self.data[self.position]=self.data[self.position]+self.atext
                self.atext=''
            
            if starttag == tag:
                break

            
reload(sys)
sys.setdefaultencoding('utf-8')
slap = SLAParser()
fd = open(sys.argv[1])
#fd = open('/home/kofxx/test.sla')
slap.feed(fd.read())
fd.close()
print '共%s页' % len(slap.data)
pageno=0

for text in slap.data:
    pageno+=1
    print '第%s页' % pageno
    print text
    raw_input('敲回车键继续……')
