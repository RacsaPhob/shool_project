from fnmatch import *

for n in range(2025,10**8,2025):
    if fnmatch(str(n),'12*34?5'):
        if n % 2025 ==0:
            print(n,n//2025)