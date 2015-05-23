import os
import subprocess


p = os.popen("curl -iH 'Accept: application/json' http://www.trola.si/zadruzni")
s = p.read()
p.close()

print s[100]
