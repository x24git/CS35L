
#!/usr/bin/python

"""
Extends functionality of POSIX comm command with option to handle
unsorted files

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: comm.py,v 1.7 2018/01/29 11:30:43 makarem Exp $
"""

import  argparse, sys

class comm:
    def __init__(self, args):
        if args.FILE1 == "-":
            self.lines1 = sys.stdin.readlines()
        else:
            file1 = open(args.FILE1, 'r')
            self.lines1 = file1.readlines()
            file1.close()
            
        if args.FILE2 == "-":
            self.lines2 = sys.stdin.readline()
        else:
            file2 = open(args.FILE2, 'r')
            self.lines2 = file2.readlines()
            file2.close()
        self.lines1[-1] += "\n"
        self.lines2[-1] += "\n"
        self.suppress1 = args.noone
        self.suppress2 = args.notwo
        self.suppress3 = args.nothree
        self.sort = args.unsorted
        
    def compare_unsorted(self):
        i=j=0
        while i < len(self.lines1):
            try:
                self.lines2.remove(self.lines1[i])
            except ValueError:
                self.print_comm(self.lines1[i],int(1))
            else:
                self.print_comm(self.lines1[i],int(3))
            finally:
                i+=1
        while j < len(self.lines2):
            self.print_comm(self.lines2[j],int(2))
            j+=1
                                
    def compare(self):
        i = j = 0
        while i < len(self.lines1) or j < len(self.lines2):
            if i >= len(self.lines1):
                self.print_comm(self.lines2[j],int(2))
                j+=1
            elif j >= len(self.lines2):
                self.print_comm(self.lines1[i],int(1))
                i+=1
            elif self.lines1[i] == self.lines2[j]:
                self.print_comm(self.lines1[i],int(3))
                i+=1
                j+=1
            elif self.lines1[i]>self.lines2[j]:
                self.print_comm(self.lines2[j],int(2))
                j+=1
            elif self.lines1[i]<self.lines2[j]:
                self.print_comm(self.lines1[i],int(1))
                i+=1  
        
    def print_comm(self,word,column):
        spacer ="\t"
        line = ''
        if not self.suppress1:
            if column == 1:
                line = word
            elif column > 1:
                line += spacer
        if not self.suppress2:
            if column == 2:
                line += word
            elif column > 2:
                line += spacer
        if not self.suppress3:
            if column == 3:
                line += word
        if not line.isspace() or "\n" in line:                
            sys.stdout.write(str(line))
        return


def main():

    parser = argparse.ArgumentParser(description="""Compare files File1
    and FILE2 line by line""", usage='comm [OPTION]... FILE1 FILE2')
    parser.add_argument("FILE1",type=str, help="""Compare this file with FILE2
    When is -, read standard input (FILE2 cannot also be -)""")
    parser.add_argument("FILE2",type=str, help="""Compare this file with
    FILE1. When is -, read stanard input (FILE1 cannot also bev-)""")
    parser.add_argument("-1","--noone",action='store_true',default=False,
    help="suppress column 1 (lines unique to FILE1)")
    parser.add_argument("-2","--notwo",action='store_true',default=False,
    help="suppress column 2 (lines unique to FILE2)")    
    parser.add_argument("-3","--nothree",action='store_true',default=False,
    help="suppress column 3 (lines that appear in both files)")
    parser.add_argument("-u","--unsorted",action='store_true',default=False,
    help="""display results from unsorted files (uses FILE1 for primary
    sorting)""")

    args = parser.parse_args()

    if args.FILE1 == '-' and args.FILE2 == '-':
        parser.error("Cannot read both inputs from stdin")
    try:
        comparator = comm(args)
    except OSError as e:
        print("comm: {2}: {1} ".
                     format (e.errno, e.strerror, e.filename))
        return
    try:
        if not args.unsorted:
            comparator.compare()
        else:
            comparator.compare_unsorted()
    except OSError as e:
        print("comm:{0}: {1} ".
                     format (e.errno, e.strerror))
        return
    
if __name__ == "__main__":
    main()
    
