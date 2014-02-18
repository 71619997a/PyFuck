'''
Created on Feb 9, 2014

@author: gbeharmarks
'''

import sys    
import re

breakOnError=False
ascii=False
DEBUG=False

def error(message):
    if(breakOnError):
        sys.exit(message)
    else:
        print message

def fatalError(message):
    sys.exit(message)

def findOpenBracket(bfuck,location,depth):
    bf=(bfuck[:location])[::-1]
    for i in range(len(bf)):
        if(bf[i]=='['):
            depth-=1
        if(depth==0):
            if (DEBUG):
                print "closed at ",location,", next at ",len(bf)-i-1 
            return len(bf)-i-1
    if (DEBUG):
        print "closed at ", location,", couldn't find matching open" 
    return -1
        
def findClosedBracket(bfuck,location):
    bf=bfuck[location:]
    if (DEBUG):
        print "open at ",location, ", next at ",bf.find(']')+1
    return bf.find(']')

def readSubroutines(subroutines):
    dicti={}
    begin=0
    while(subroutines.find("::",begin)!=-1):
        funcBegin=subroutines.find("::",begin)+2
        begin=funcBegin
        funcEnd=subroutines.find("::",begin)
        funcName=subroutines[funcBegin:funcEnd]
        bodyBegin=funcEnd+2
        begin=bodyBegin
        bodyEnd=subroutines.find("[::]",begin)
        body=subroutines[bodyBegin:bodyEnd]
        dicti[":"+funcName+":"]=body
        begin=bodyEnd+4
    return dicti

def findAndReplace(strn,rdict):
 
    pattern = re.compile('|'.join(re.escape(key) for key in rdict.keys()))
    return pattern.sub(lambda x: rdict[x.group()], strn)


brainChars=".,+-[]><:_"
brainfuck=""
depth=0
mem=[0 for i in range(30000)]
ptr=0
loc=0
ptrArea=7
recursion=21

#routineFile=open("/Users/gbeharmarks/Desktop/subroutines.pbf",'r'
routineFile=open("/tmp/guest-lqfSOm/subroutines.pbf",'r')
routines=routineFile.read()
routineFile.close()
#routines="::.,::.++.[::]::--::-.-.+ [::]"

routines=filter(lambda x: x in brainChars,routines)

srdict=readSubroutines(routines)

switch=input("0: Read from input\n1: Read from file")

if(switch):
    path=raw_input("Enter filepath: ")
    brainfile=open(path)
    brainfuck=brainfile.read()
    brainfile.close()
    
else:
    brainfuck=raw_input("Type your code: \n\n")
    
brainfuck=filter(lambda x: x in brainChars,brainfuck)
for i in range(recursion):
    if(':' in brainfuck):
        brainfuck=findAndReplace(brainfuck,srdict)
    else:
        break
if(':' in brainfuck):
    start=brainfuck.find(':')
    end=brainfuck.find(':',start+1)
    
    fatalError("Max recursion depth (" + str(recursion)+") reached: func "+brainfuck[start:end+1])
print brainfuck
while (loc<len(brainfuck)):
    if(brainfuck[loc]=='.'):
        if(ascii):
            print str(unichr(mem[ptr]))
        else:
            print mem[ptr]
    elif(brainfuck[loc]==','):
        inp = input("Input: ")
        
        if(ascii):
            mem[ptr]=ord(inp)
        else:
            mem[ptr]=int(inp)
    elif(brainfuck[loc]=='+'):
        mem[ptr]+=1
        if(DEBUG):
            print "add 1 to "+str(ptr)
    elif(brainfuck[loc]=='-'):
        if(mem[ptr]>0 or ascii):
            mem[ptr]-=1
        else:
            error("At ",loc,": Negative numbers only permitted out of ASCII mode.")
    elif(brainfuck[loc]=='>'):
        
        ptr+=1
        if (DEBUG):
            print "after mov ptr is "+str(ptr)
        if(ptr>29999):
            ptr=0
    elif(brainfuck[loc]=='<'):
        ptr-=1
        if(DEBUG):
            print "after mov ptr is "+str( ptr)
        #if(ptr<0):
           # error("At ",loc,": Pointer is less than 0.")
            
    elif(brainfuck[loc]=='['):
        depth+=1
        if(mem[ptr]==0):
            depth-=1
            loc=findClosedBracket(brainfuck,loc)
    elif(brainfuck[loc]==']'):
        if(mem[ptr]!=0):
            loc=findOpenBracket(brainfuck,loc,depth)-1
            depth-=1
    elif(brainfuck[loc]=='_'):
        strel=" "
        for i in range(3*ptrArea):
            strel+=" "
        print strel+"v"
        bnd=ptr-ptrArea
        if(bnd<0):
            print mem[bnd:]+mem[:2*ptrArea+bnd+1]
        else:
            print mem[bnd:ptr+ptrArea+1]
        if(DEBUG):
            print mem[-1],mem[0],mem[1]
            
       
    loc+=1
    
