"""
testbench code to verify regex filter
"""


import re


def testbench(key):

    key = key.upper()
    key = re.sub(r'[^a-zA-Z0-9\s]+', '', key) #rmv all non alphanumeric
    key = re.sub(r'\s+',' ', key) #trim all \s+ to just \s
    key = re.sub(r'\bAND\b', '&', key) #convert all word AND to &
    key = re.sub(r'\bOR\b', '@', key) #convert all word OR to @
    key = re.sub(r'(?<![@&])\s+(?![@&])', '&', key) #convert all space that is not beside &/@ into &
    key = re.sub(r'\s+','', key) #remove all \s
    key = re.sub(r'^[@&]+|[@&]+$', '', key) #remove all leading/trailing @&
    key = re.sub(r'[\s@]*&[\s@&]*', '&', key) #replace all series of any @@&&&@&@&@ to & as long as 1 & present
    key = re.sub(r'[@]*@[@]*', '@', key) #replace all series of @@@@@ to just @

    key_groups_intermediate = re.split(r'@', key) #split into sum of products
    key_groups = []

    for group in key_groups_intermediate:
        groups_intermediate = re.split(r'&', group) #split each product into individual element
        key_groups.append(groups_intermediate)

    print(key_groups)

#Should output (Foo and Bar and Baz) or (Qux and Quux)
testbench("$>  foo and    bar baz or qux   quux   or") #leading/trailing symbols or operators ignored, multiple /s resolved
testbench(" $$^&@# f&oo* aNd BAR&&&@@@@ bAZ ||| or qux >>q>>uux   ") #leading/trailing /s ignored, symbols within keyword ignored
testbench("$^and FOo ..BaR + Baz or    quX      and or and and or quux     ") #multiple and/or conflicting logic resolved

#Should not misintepret ORange or ANDes as operator
testbench("  AnDes AND ORange Or foo ") #correctly displays (Andes and Orange) or (Foo)