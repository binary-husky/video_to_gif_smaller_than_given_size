
def bi_search(fn, range):    
    # 输入 fn 是一个递增过零点的函数
    # 输入 range 是一个fn的list
    # 返回 range 中的零点或零点左侧的值
    L, R = 0, len(range)
    while (R-L>1):
        M = (L + R)//2
        y = fn(range[M])
        if y > 0: 
            R = M
        elif y == 0: 
            return M
        else:
            L = M
        print(L, R)
    return range[L]

def q(a):
    print(a)
    return a - 77.8

res = bi_search(q, list(range(100)))
print(res)
