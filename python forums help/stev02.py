import sys 
import re 

def logparse():   

    log_file = raw_input("Enter the path to the log file: ") 
    sigs_file = raw_input("Enter the path to the signature file: ") 

    lines = {}
    with open(sigs_file) as r:
        for item in r:
            if item[-1] == "\n":
                item = item[:-1]
            if item and not item.startswith("#"):
                lines[item] = []
                lines[item].append(re.compile(item))
                lines[item].append(0)
                prev = item
            elif item and item.startswith("#"):
                lines[prev].insert(0, item)

    with open(log_file) as fd:
        count = 0
        for line in fd:
            count = count + 1

            for expr in lines.keys():
                found = lines[expr] [1].search(line)
                if found:
                    lines[expr] [2] = lines[expr] [2] + 1
                    lines[expr].append(count)

    print("Checked %d lines in the log file." % (count))
    print("--Signatures Found--     --Occurences--")
    for val in lines.values():
        print(val[0], val[2])

            
def fail_to_find(): 
    print() 
    print("No suspicious entries found.") 
    print() 
    logparse();

print("A simple command line log parser.")
print()
logparse()