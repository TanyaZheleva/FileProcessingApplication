#!/usr/bin/python
import re
import sys
import os.path
import mysql.connector
#import subprocess

class File:
    lines = []
    numbers = []
    
    def check_file(self,filename):
        if os.path.isfile(filename):
            print("file exists")
            return 1
        print("file doesnt exist")
        return 0

    def save_file(self, filename):
        fd=open(filename,'w+')
        for line in self.numbers:
            check = 0 
            for num in line:
                if check == 0:
                    fd.write(str(num))
                    check = 1
                else:
                    fd.write(" " + str(num))
            fd.write("\n")
        self.update_lines(fd)
        fd.close()

    def update_lines(self,fd):
        if self.lines:
            del self.lines
        fd.seek(0)
        self.lines=fd.readlines()
        if not self.validate_file(fd):
            return 0
        return 1

    def update_numbers(self):
        if self.numbers:
            self.numbers.clear()
        num=""
        for j in self.lines:
            sublist = []
            for q in j:
                if q == " " or q == "\t" or q == "\n" and num != "":
                    sublist.append(int(num))
                    num=""
                else:
                    num+=q
            self.numbers.append(sublist)
        return 1
    
    def validate_line_index(self,line):
        if line <= 0 or line > len(self.numbers):
            print("Invalid index, range of file line indexes is [1;%d]"%len(self.numbers))
            return 0
    
    def validate_inline_index(self,line,index):
        if index <= 0  or index > len(self.numbers[line-1]):
            print("Inline index is invalid. Range:[1;%d]"%len(self.numbers[line-1]))
            return 0
   
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
            if re.search(r'[ \t]{2,}',line):
                print("Line %d contains sequence of spaces and/or tabs. Invalid syntax." %count)
                return 0
            count+=1
        return 1

    def get_lines(self,fd):
        if not self.update_lines(fd):
            print("Failed reading lines from file")
            return 0
        if not self.update_numbers():
            print("Failed to read literals as numbers")
            return 0
        return 1

    def switch_lines(self, filename, l1, l2):
        self.validate_line_index(l1)
        self.validate_line_index(l2)
        l1,l2=l1-1,l2-1
        self.lines[l1],self.lines[l2] = self.lines[l2],self.lines[l1]
        self.update_numbers()
        self.save_file(filename)
        
    def switch_numbers(self, filename, l1, n1, l2, n2):
        self.validate_line_index(l1)
        self.validate_line_index(l2)
        self.validate_inline_index(l1,n1)
        self.validate_inline_index(l2,n2)
        l1,l2,n1,n2=l1-1,l2-1,n1-1,n2-1
        self.numbers[l1][n1], self.numbers[l2][n2] = self.numbers[l2][n2], self.numbers[l1][n1]
        self.update_lines(fd)
        self.save_file(filename)

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
        self.save_file(filename)
  
    def read_number(self, line, index):
        self.validate_line_index(line)
        self.validate_inline_index(line,index)
        print(self.numbers[line-1][index-1])
   
    def modify_number(self, filename, line, index, number):
        self.validate_line_index(line)
        self.validate_inline_index(line,index)
        if re.search(r'^0[0-9]+$',str(number)) or re.search(r'[^[0-9]]',str(number)):
            print("%d is not a valid number"%number)
            return 0
        self.numbers[line-1][index-1] = number
        self.save_file(filename)
        
    def remove_number(self, filename, line, index):
        self.validate_line_index(line)
        self.validate_inline_index(line,index)
        del self.numbers[line-1][index-1]
        self.save_file(filename)

    def create_db(sef):
       mydb = mysql.connector.connect(
            host="localhost",
            user="myuser",
            password="mypassword"
        )
       
       mycursor = mydb.cursor()
       mycursor.execute("CREATE DATABASE myfiledb")

    def insert_table(self):
#        subprocess.call("./createdb.sh")
#        self.create_db()
        mydb = mysql.connector.connect(
            host="localhost",
            user="myuser",
            password="mypassword",
            database="myfiledb"
        )
        
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE IF NOT EXISTS fileContents (id INT NOT NULL PRIMARY KEY, line_index INT NOT NULL, data TEXT)")
        index=1
        _id=1000
        for line in self.lines:
            sql = "INSERT INTO fileContents (id, line_index, data) values(%s, %s, %s);"
            val = (int(_id), int(index), line)
            mycursor.execute(sql, val)
            index+=1
            _id+=1
            mydb.commit()

def print_options():
    print("\n")
    print("Enter only letter(and .<number>) of desired option")
    print ("a. validate the file contents\nb.switch two lines by line indexes\nc.switch two numbers by line and number indexes\nd.1.insert at position\nd.2.read a number at a position\nd.3.modify a number at posigion\nd.4.remove a number at position\ne.insert content of file into a database table\nq.exit program" )



filename = input ("Enter the full path to a file you would like to work with: ")

myobject = File()
while not myobject.check_file(filename):
    filename = input ("Enter the full path to a file you would like to work with: ")

#file is fine; selecting options
print_options()
option = input ("Select an option and input arguments: ")

#initially open file
fd = open(filename,'r+')
myobject.get_lines(fd)

#menu loop
while option != "q": 
    if option == "a":
        myobject.validate_file(fd)
    elif option == "b":
        line1, line2 = map(int, input ("specity line indexes: ").split())
        myobject.switch_lines(filename, line1, line2)
    elif option == "c":
        line1, num1, line2, num2 = map(int,input ("specity two pairs of line index, inline index: ").split())
        myobject.switch_numbers(filename, line1, num1, line2, num2)
    elif option == "d.1":
        line, num, number = map(int, input ("specity line index, inline index and new number: ").split())
        myobject.insert_number(filename, line, num, number)
    elif option == "d.2":
        line, num = map(int, input ("specity line index, inline index: ").split())
        myobject.read_number(line, num)
    elif option == "d.3":
        line, num, number = map(int, input ("specity line index, inline index and new number: ").split()) 
        myobject.modify_number(filename,line,num, number)
    elif option == "d.4":
        line, num = map(int, input ("specity line index, inline index: ").split())
        myobject.remove_number(filename,line, num)
    elif option == "e":
        myobject.insert_table()
    else:
        print("Invalid option.")
    print_options()
    option = input ("Select an option and input arguments: ")

fd.close()
