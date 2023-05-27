import random
import string
import numpy as np
import helper

def gen(size, grid):
    alphabet = string.ascii_uppercase + string.ascii_lowercase
    colors = list(alphabet)

    to_gen = 5000

    for i in range (1, to_gen):
        code = ''
        color_amount = generate_color_amount(size)
        
        added = 0
        while added < color_amount:
            char = colors[random.randint(0,len(colors)-1)]
            if char not in code:
                code = code + char
                added += 1
            else:
                continue
        
        code = code + code
        _sum = size*size - len(code)
        n = random.randint(len(code)/2, len(code))
        nums = np.random.multinomial(_sum, np.ones(n)/n, size=1)[0]
        nums = [x for x in nums if x != 0]

    print(format_code(code, nums))
    print (helper.to_string(helper.code_to_grid(format_code(code, nums), size),size))
        

def format_code(str, nums):
    generated = []
    
    code = []
    code[:] = str
    random.shuffle(code)
    lastwaspoint = False

    while(len(code) > 0 or len(nums) > 0):

        if (len(code) > 0 and not len(nums) > 0):
            generated = generated + code
            code = []
        elif(len(nums) > 0 and not len(code) > 0):
            num = sum(nums)
            generated.append('{}'.format(num))
            nums = []


        if (len(code) > 0 and len(nums) > 0):
            ispoint = random.choice([True, False])
            if not lastwaspoint:
                last, code = code[-1], code[:-1]
                generated.append(last)
                lastwaspoint = True

            else:
                if(ispoint):
                    last, code = code[-1], code[:-1]
                    generated.append(last)
                    lastwaspoint = True
                else:
                    last, nums = nums[-1], nums[:-1]
                    generated.append('{}'.format(last))
                    lastwaspoint = False

    return ''.join(generated)

def generate_color_amount(size):
    if size <= 5:
        return random.randint(2, size-1)

    elif(size < 10):
        return random.randint(size, size + 3)

    else:
        return random.randint(size, size + 8)


if __name__ == '__main__':
    gen(8)



