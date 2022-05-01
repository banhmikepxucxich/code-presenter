langlist = []
with open('Supported.txt', 'r') as supported:
    for line in supported:
        if line.startswith('#'):
            pass
        else:
            langlist.append(line)

print(langlist)