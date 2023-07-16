f = open("Mehlandroads07.txt","r")
lines = sorted(f.readlines())
f.close()

f = open("out.txt","w")
for line in lines:
    f.write(line)
f.close