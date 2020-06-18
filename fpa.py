#!/usr/bin/python

import re
import sys
import os
import tempfile

class File:
    lines = []
    numbers = []
    
    def validate_file(self, fd):
        count=1
        for line in self.lines:
            if re.search(r'^[ \t]',line):
                print("Line %d starts with a space.Invalid syntax" %count)
                return 0
            if re.search(r'[ \t]0',line) or re.search(r'^0',line):
                print("Number at line %d starts with 0" %count)
                return 0
            if re.search(r'[^[0-9]]',line,re.IGNORECASE):
                print("Line %d contains non-digit characters" %count)
                return 0
            count+=1
        return 1

    def get_lines(self,fd):
        self.lines=fd.readlines()
        check=self.validate_file(fd)
        if check == 0:
            return 0
        num=""
        for j in self.lines:
            sublist = []
            for q in j:
                if q == " " or q == "\t" or q == "\n":
                    sublist.append(int(num))
                    num=""
                else:
                    num+=q
            self.numbers.append(sublist)
        return 1

    def switch_lines(self, l1, l2):
        first=0
        second=0
        if l1 <= 0 or l2 <= 0 or l1 > len(self.lines) or l2 > len(self.lines):
            if l1<l2:
                first=l1
                second=l2
            else:
                first=l2
                second=l1
        tfd, path = tempfile.mkstemp()
        try:
            with os.fdopen(tfd,'w') as tmp:
                count=1
                for line in self.lines:
                    if count == first:
                        tmp.write(self.lines[second] + '\n')
                    elif count == second:
                        tmp.write(self.lines[first] + '\n')
                    else:
                        tmp.write(line + '\n')
                    count+=1
        finally:
            os.remove(path)
        
#    def switch_numbers(self, fd, l1, n1, l2, n2):
#    def save_file(self, fd, filename):
#    def insert_number(self, fd, line, index, number):
#    def read_number(self, fd, line, index):
#    def replace_number(self, fd, line, index, number):
#    def remove_number(self, fd, line, index):


filename = input ("Enter the full path to a file you would like to work with: ")

print ("a. validate the file contents\nb.switch two lines by line indexes\nc.switch two numbers by line and number indexes\nd.the result file be saved in the original after validations on the format and the given indexes\ne.1.insert at position\ne.2.read a number at a position\ne.3.modify a number at posigion\ne.4.remove a number at position")

option = input ("Select an option and input arguments: ")

fd = open(filename,'r+')

myobject = File()
res=myobject.get_lines(fd)
if res == 0:
    sys.exit()
myobject.switch_lines(2,5)
fd.close()
