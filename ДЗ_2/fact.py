import time

def fact_rec(n):
    if n == 0 or n == 1:
        return 1
    return n * fact_rec(n - 1)

def fact_it(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

if __name__ == '__main__':
    n = 900 # Ниже лимита рекурсии (обычно 1000)
    
    start_rec = time.time()
    fact_rec(n)
    end_rec = time.time()
    
    start_it = time.time()
    fact_it(n)
    end_it = time.time()
    
    print(f"Recursive time: {end_rec - start_rec:.10f}")
    print(f"Iterative time: {end_it - start_it:.10f}")
    # Итеративный способ обычно быстрее и безопаснее, так как не вызывает переполнение стека рекурсии при больших n.
