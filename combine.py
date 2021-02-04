import os


files = list(os.scandir())

passlist = []


for file in files:
    if not file.name.startswith('combine'):
        passlist.extend(open(file.name ,'rb').read().split(b'\n'))
        
open('all.txt','wb').write(b'\n'.join(list(set(passlist))))