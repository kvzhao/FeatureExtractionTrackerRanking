import sys
import struct
import matplotlib.pyplot as plt

filename = sys.argv[1]
fd = open(filename, 'rb')
n = struct.unpack('i', fd.read(4))[0]
c = struct.unpack('i', fd.read(4))[0]
l = struct.unpack('i', fd.read(4))[0]
h = struct.unpack('i', fd.read(4))[0]
w = struct.unpack('i', fd.read(4))[0]
print 'Dim', n, c, l, h, w

fc = []
for i in range(n * c):
    feat = struct.unpack('f', fd.read(4))[0]
    print feat
    fc.append(feat)
plt.plot(fc)
plt.show()
