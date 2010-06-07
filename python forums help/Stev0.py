import sys 
import re 

def logparse(): 
    while True: 

        log_file = input("Enter the path to the log file: ") 
        sigs_file = input("Enter the path to the signature file: ") 

        lines = [] 
        with open(sigs_file) as r: 
            for line in r: 
                if line and not line.startswith("#"): 
                    lines.append(line) 
        expr = '|'.join(lines)

        rr = re.compile(expr) 

        with open(log_file, 'r') as fd:
            count = 0 
            for i in fd: 
                if rr.search(i): 
                    print(i); 
                    count+=1 
            if count == 0: 
                fail_to_find() 
            else: 
                print("Found %s suspicious entries." %count) 
                print(); 
                logparse() 

def fail_to_find(): 
    print() 
    print("No suspicious entries found.") 
    print() 
    logparse();

print("A simple command line log parser.")
print()
logparse()