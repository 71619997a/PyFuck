'''
Created on Feb 9, 2014
@author: gbeharmarks
'''
import sys    
import re
breakOnError=False
ascii=False
outAscii=False
DEBUG=True
dir="/Users/gbeharmarks/Desktop/PyFuck/"
saved=""
askSave=False
inputs=""
#print c.get("bob", "british") # To access the "british" attribute for bob directly
def error(message):
    if(breakOnError):
        sys.exit(message)
    else:
        print message
def fatalError(message):
    sys.exit(message)
def getDepth(bfuck,location):
    bf=bfuck[:location]
    depth=0
    for i in range(len(bf)):
        if(bf[i]=='['):
            depth+=1
        if(bf[i]==']'):
            depth-=1
    return depth
def findOpenBracket(bfuck,location):
    bf=(bfuck[:location])[::-1]
    depth=getDepth(bfuck,location)
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
    depth=getDepth(bfuck,location)
    start=location

    if(getDepth(bfuck,bfuck.find("]",start+1))-1!=depth):
        start=bfuck.find("]",start+1)
        if (DEBUG):
            print "non-closing bracket at "+str(start-1)
    else:
        return bfuck.find("]",start+1)
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
def save():
    if(input("Would you like to save your code? 1 - yes, 0 - no: ")):
        outFile=open(dir+"scripts/"+raw_input("Enter a filename: "),"w")
        outFile.write(saved)
        print "Wrote file into "+dir+"scripts."
        outFile.close()
    return
def onExit(message):
    if(askSave):
        save()
    sys.exit(message)
    
brainChars=".,+-[]><:_@$%^v"
brainfuck=""
mem=[0 for i in range(30000)]
ptr=0
loc=0
stored=0
ptrArea=7
recursion=21
routineFile=open(dir+"subroutines.pbf",'r')
#routineFile=open("/tmp/guest-lqfSOm/subroutines.pbf",'r')
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
    askSave=True
    brainfuck=raw_input("Type your code: \n\n")
saved=brainfuck    
brainfuck=filter(lambda x: x in brainChars,brainfuck)
for i in range(recursion):
    if(':' in brainfuck):
        newBF=findAndReplace(brainfuck,srdict)
        if(newBF==brainfuck):
            start=brainfuck.find(':')
            end=brainfuck.find(':',start+1)
            fatalError("Function not found: "+brainfuck[start:end+1])
    else:
        break
if(':' in brainfuck):
    start=brainfuck.find(':')
    end=brainfuck.find(':',start+1)
    
    fatalError("Max recursion depth (" + str(recursion)+") reached: func "+brainfuck[start:end+1])
print brainfuck
while (loc<len(brainfuck)):
    if(brainfuck[loc]=='.'): #print mem at ptr
        if(outAscii):
            print str(unichr(mem[ptr]))
        else:
            print mem[ptr]
    elif(brainfuck[loc]==','): #input mem at ptr
        if(inputs=="" and ascii):
            inputs = raw_input("Input: ")
        
            
        if(ascii):
            mem[ptr]=ord(inputs[0])
            inputs=inputs[1:]
        else:
            mem[ptr]=int(raw_input("Input: "))
    elif(brainfuck[loc]=='+'): #
        mem[ptr]+=1
        if(DEBUG):
            print "add 1 to "+str(ptr)
    elif(brainfuck[loc]=='-'):
        if(mem[ptr]>0 or not ascii):
            mem[ptr]-=1
        else:
            error("At "+str(loc)+": Negative numbers only permitted out of ASCII mode.")
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
            #error("At ",loc,": Pointer is less than 0.")
            
    elif(brainfuck[loc]=='['):
        
        if(mem[ptr]==0):
            
            loc=findClosedBracket(brainfuck,loc)
    elif(brainfuck[loc]==']'):
        if(mem[ptr]!=0):
            loc=findOpenBracket(brainfuck,loc)-1
            
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
    elif (brainfuck[loc]=='@'):
        onExit("Exited from reaching @")
    elif (brainfuck[loc]=='$'):
        stored=mem[ptr]
    elif (brainfuck[loc]=='%'):
        mem[ptr]=stored
    elif (brainfuck[loc]=='v'):
        loc=brainfuck.find('v',loc+1)
    elif (brainfuck[loc]=='^'):
        end=brainfuck.find('^',loc+1)
        loc=brainfuck.find('v'+brainfuck[loc+1:end]+'v')+end-loc
    loc+=1
onExit("Exited from reaching EOF")

