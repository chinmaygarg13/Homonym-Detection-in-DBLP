import numpy

x = ['Computer graphics (images)', 'Exhibition', 'Multimedia']
y = ['Computer graphics (images)', 'Exhibition', 'Multimedia']

temp = list(set(x).intersection(y))
n= len(temp)
print(n)