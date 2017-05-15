"""
This is python code I wrote to use as reference to translate to our machine's architecture txhu
"""

def bubbleSort(alist):
    #increment down the length of the size of the arrays
    for passnum in range(len(alist)-1,0,-1):
        #only does bubble sort within that length
        for i in range(passnum):
            if alist[i]>alist[i+1]:
                temp = alist[i]
                alist[i] = alist[i+1]
                alist[i+1] = temp

alist = [54,26,93,17,77,31,44,55,20]
bubbleSort(alist)
print(alist)
