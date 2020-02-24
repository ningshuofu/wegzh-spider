def f(a, b):
    a += '.0'
    b += '.0'
    a_l = len(a)
    b_l = len(b)
    min_l = min(a_l, b_l)
    a_index = -1
    b_index = -1
    while True:
        a_index += 1
        b_index += 1
        a_meta = 0
        b_meta = 0
        while a_index < min_l:
            if a[a_index] != '.':
                a_meta = a_meta * 10 + int(a[a_index])
                a_index += 1
            else:
                break
        else:
            if a_meta != 0:
                return 1
            break
        while b_index < min_l:
            if b[b_index] != '.':
                b_meta = b_meta * 10 + int(b[b_index])
                b_index += 1
            else:
                break
        else:
            if b_meta != 0:
                return -1
            break
        if a_meta > b_meta:
            return 1
        elif a_meta < b_meta:
            return -1
    for i in range(b_index, b_l):
        if b[i] != '.' and b[i] != '0':
            return -1
    for i in range(a_index, a_l):
        if a[i] != '.' and a[i] != '0':
            return 1
    return 0


if __name__ == '__main__':
    print(f("0.1", "1.1"))
    print(f("1.0.1", "1"))
    print(f("7.5.2.4", "7.5.3"))
    print(f("1.01", "1.001"))
    print(f("1.0", "1.0.0"))
