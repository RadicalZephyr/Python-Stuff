import sys 
import re 

def logparse():   

    log_file = input("Enter the path to the log file: ") 
    sigs_file = input("Enter the path to the signature file: ") 

    lines = {}
    with open(sigs_file) as r:
        for item in r:
            item = item.replace('\n', '')

            if item and not item.startswith("#"):
                lines[item] = {}
                lines[item]['re'] = re.compile(item)
                lines[item]['count'] = 0
                lines[item]['linenums'] = []
                prev = item
            elif item and item.startswith("#"):
                lines[prev]['description'] = item

    with open(log_file) as fd:
        count = 0
        for line in fd:
            count = count + 1
            for expr in lines.keys():
                found = lines[expr]['re'].search(line)
                if found:
                    lines[expr]['count'] = lines[expr]['count'] + 1
                    lines[expr]['linenums'].append(count)

    print("--Signatures Found--     --Occurences--")
    for val in lines.values():
        print(val['description'], val['count'])

print("A simple command line log parser.")
print()
logparse()