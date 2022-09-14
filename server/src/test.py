import os

seen = set()
for i in range(1901,3501):
    seen.add(i)
path = r'D:\OutputFiles1\ProteinID'
for file in os.listdir(path):
    fileNum = os.path.basename(file)
    fileNum = fileNum.strip("File")
    fileNum = fileNum.strip(".fna")
    fileNum = int(fileNum.strip(".txt"))
    # print(fileNum)

    if fileNum in seen:
        seen.remove(fileNum)

print(seen)
    