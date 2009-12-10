inputstring = """g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."""
outputstring = ''
import string
for letter in inputstring:
    if 97 < ord(letter) < 120:
        outputstring = outputstring + chr(ord(letter)+2)
    elif ord(letter) == 121:
        outputstring = outputstring + chr(97)
    elif ord(letter) == 122:
        outputstring = outputstring + chr(98)
    else:
        outputstring = outputstring + letter


print outputstring    