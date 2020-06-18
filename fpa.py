#!/usr/bin/python

class File:
    lines = []
    numbers = []

    def validate_file(self, fd):
        for line in self.lines:
            if line[0] == " " or line [0] == "\t":
                return 0
            for i in range(len(line)-1):
                if line[i-1] == " " or line[i-1] == "\t":
                    if line[i] == "0":
                        return 0
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
                if q == " " or q == "\t":
                    sublist.append(int(num))
                    num=""
                else:
                    num+=q
            self.numbers.append(sublist)
#        return 1
        print (self.numbers)

#    def switch_lines(self, fd, l1, l2):
#    def switch_numbers(self, fd, l1, n1, l2, n2):
#    def save_file(self, fd, filename):
#    def insert_number(self, fd, line, index, number):
#    def read_number(self, fd, line, index):
#    def replace_number(self, fd, line, index, number):
#    def remove_number(self, fd, line, index):


filename = input ("Enter the full path to a file you would like to work with: ")

print ("a. validate the file contents\nb.switch two lines by line indexes\nc.switch two numbers by line and number indexes\nd.the result file be saved in the original after validations on the format and the given indexes\ne.1.insert at position\ne.2.read a number at a position\ne.3.modify a number at posigion\ne.4.remove a number at position")

option = input ("Select an option and input arguments: ")
print (option)

fd = open(filename,'r+')

myobject = File()
myobject.get_lines(fd)
print( myobject.validate_file(fd) )

fd.close()
