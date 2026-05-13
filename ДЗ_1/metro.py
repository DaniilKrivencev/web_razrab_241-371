if __name__ == '__main__':
    n = int(input())
    passengers = []
    for _ in range(n):
        passengers.append(list(map(int, input().split())))
    
    t = int(input())
    
    count = 0
    for p in passengers:
        if p[0] <= t <= p[1]:
            count += 1
            
    print(count)
