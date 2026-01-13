import re

key = " anders or and or tim and and     bob or or cute   "

key = key.upper()
key = re.sub(r'\s+',' ', key)
key = re.sub(r'\bAND\b', '&', key)
key = re.sub(r'\bOR\b', '@', key)
key = re.sub(r'(?<![@&])\s+(?![@&])', '&', key)
key = re.sub(r'\s+','', key)
key = re.sub(r'^[@&]+|[@&]+$', '', key)
key = re.sub(r'[\s@]*&[\s@&]*', '&', key)
key = re.sub(r'[@]*@[@]*', '@', key)

print(key)