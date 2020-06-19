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
            if re.search(r'[ \t]0[0-9]+',line) or re.search(r'^0[0-9]+',line):
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

    def switch_lines(self, filename, l1, l2):
        if l1 <= 0 or l2 <= 0 or l1 > len(self.lines) or l2 > len(self.lines):
            print("Invalid indexes, range of file line indexes is [1;%d]"%len(self.lines))
            return 0
        l1-=1
        l2-=1
        self.lines[l1],self.lines[l2] = self.lines[l2],self.lines[l1]
        fd=open(filename,'w')
        for line in self.lines:
            fd.write(line)
        fd.close()
        
    def switch_numbers(self, filename, l1, n1, l2, n2):
        if l1 <= 0 or l1 > len(self.numbers):
            print("Line index %d is invalid. Range:[1;%d]"%(l1,len(self.numbers)))
            return 0
        if l2 <= 0 or l2 > len(self.numbers):
            print("Line index %d is invalid. Range:[1;%d]"%(l2,len(self.numbers)))
            return 0
        if n1 <= 0  or n1 > len(self.numbers[l1-1]):
            print("Inline index %d is invalid. Range:[1;%d]"%(n1,len(self.numbers[l1-1])))
            return 0
        if n2 <= 0  or n2 > len(self.numbers[l2-1]):
            print("Inline index %d is invalid. Range:[1;%d]"%(n2,len(self.numbers[l2-1])))
            return 0
        l1-=1
        l2-=1
        n1-=1
        n2-=1
        self.numbers[l1][n1], self.numbers[l2][n2] = self.numbers[l2][n2], self.numbers[l1][n1]
        fd=open(filename,'w')
        for line in self.numbers:
            check = 0 
            for num in line:
                if check == 0:
                    fd.write(str(num))
                    check = 1
                else:
                    fd.write(" " + str(num))
            fd.write("\n")
        fd.close()
#    def save_file(self, fd, filename):

    def insert_number(self, filename, line, index, number):
        if line <= 0 or line > len(self.numbers):
            if line == len(self.numbers)+1:
                self.numbers.insert(line-1,[])
            else:
                print("Line index is invalid. Range:[1;%d]"%len(self.numbers))
                return 0
        if index <= 0  or index > len(self.numbers[line-1])+1:
            print("Inline index is invalid. Range:[1;%d]"%len(self.numbers[line-1]))
            return 0
        if re.search(r'^0[0-9]+$',str(number)) or re.search(r'[^[0-9]]',str(number)):
            print("%d is not a valid number"%number)
            return 0
        self.numbers[line-1].insert(index-1,number)
        fd=open(filename,'w')
        for line in self.numbers:
            check = 0 
            for num in line:
                if check == 0:
                    fd.write(str(num))
                    check = 1
                else:
                    fd.write(" " + str(num))
            fd.write("\n")
        fd.close()
  
    def read_number(self, line, index):
        if line <= 0 or line > len(self.numbers):
            print("Line index is invalid. Range:[1;%d]"%len(self.numbers))
            return 0
        if index <= 0  or index > len(self.numbers[line-1]):
            print("Inline index is invalid. Range:[1;%d]"%len(self.numbers[line-1]))
            return 0
        print(self.numbers[line-1][index-1])
   
    def modify_number(self, filename, line, index, number):
        if line <= 0 or line > len(self.numbers):
            print("Line index is invalid. Range:[1;%d]"%len(self.numbers))
            return 0
        if index <= 0  or index > len(self.numbers[line-1]):
            print("Inline index is invalid. Range:[1;%d]"%len(self.numbers[line-1]))
            return 0
        if re.search(r'^0[0-9]+$',str(number)) or re.search(r'[^[0-9]]',str(number)):
            print("%d is not a valid number"%number)
            return 0
        self.numbers[line-1][index-1] = number
        fd=open(filename,'w')
        for line in self.numbers:
            check = 0 
            for num in line:
                if check == 0:
                    fd.write(str(num))
                    check = 1
                else:
                    fd.write(" " + str(num))
            fd.write("\n")
        fd.close()

        
    def remove_number(self, filename, line, index):
        if line <= 0 or line > len(self.numbers):
            print("Line index is invalid. Range:[1;%d]"%len(self.numbers))
            return 0
        if index <= 0  or index > len(self.numbers[line-1]):
            print("Inline index is invalid. Range:[1;%d]"%len(self.numbers[line-1]))
            return 0
        del self.numbers[line-1][index-1]
        fd=open(filename,'w')
        for line in self.numbers:
            check = 0 
            for num in line:
                if check == 0:
                    fd.write(str(num))
                    check = 1
                else:
                    fd.write(" " + str(num))
            fd.write("\n")
        fd.close()

#    def terminate_script(result):

filename = input ("Enter the full path to a file you would like to work with: ")

print ("a. validate the file contents\nb.switch two lines by line indexes\nc.switch two numbers by line and number indexes\nd.1.insert at position\nd.2.read a number at a position\nd.3.modify a number at posigion\nd.4.remove a number at position")

option = input ("Select an option and input arguments: ")

fd = open(filename,'r+')

myobject = File()
res=myobject.get_lines(fd)
if res == 0:
    sys.exit()

myobject.remove_number(filename,1,7)
fd.close()

