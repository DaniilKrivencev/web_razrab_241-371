def matrix_multiply(A, B, n):
    # Initialize result matrix C with zeros
    C = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                
    return C

if __name__ == '__main__':
    try:
        line = input()
        if not line:
            exit()
        n = int(line)
        
        matrix_a = []
        for _ in range(n):
            matrix_a.append(list(map(int, input().split())))
            
        matrix_b = []
        for _ in range(n):
            matrix_b.append(list(map(int, input().split())))
            
        result = matrix_multiply(matrix_a, matrix_b, n)
        
        for row in result:
            print(*(row))
    except ValueError:
        pass
