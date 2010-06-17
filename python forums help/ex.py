lines = {}

with open(sigs_file) as r:
    for line in r:
        if line and not line.startswith("#"):
            lines[line] = []
            previous = line
            # To model this on your code, you could then write this:
        elif line and line.startswith("#"):
            lines[previous].append(line)

expr = '|'.join(lines.keys())
# But like I said, that's not the optimal way for your purposes.
# Instead, I would do something like this:

for item in lines.keys():
    lines[item].append(re.compile(item))


with open(log_file) as fd:
    count = 0
    for line in fd:
        count = count + 1
        for expr in lines.keys():
            matches = lines[expr][1].search(line)
            if matches:
                lines[expr][1] = lines[expr][1] + 1
                lines[expr].append(count)
