import random

ANSI_LOOKUP = dict(R=101, B=104, Y=103, G=42,
                   O=43, C=106, M=105, m=41,
                   P=45, A=100, W=107, g=102,
                   T=47, b=44, c=46, p=35)

colors = ['R', 'B', 'Y']

def gen():
    to_gen = 5000
    min = 4
    max = 15

    for i in range (1, 5000):
        size = random.randint(4, 15)
        
if __name__ == '__main__':
    gen()



