file1 = open("spelling.txt", "r")
#print(file1.read())
for i in file1.readlines():
    i=i.rstrip("\n")
    #print i
    spelling_data=i.split(",")
    print(spelling_data)
