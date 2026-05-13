if __name__ == '__main__':
    n = int(input())
    arr = []
    for _ in range(n):
        command = input().split()
        cmd_type = command[0]
        
        if cmd_type == 'insert':
            arr.insert(int(command[1]), int(command[2]))
        elif cmd_type == 'print':
            print(arr)
        elif cmd_type == 'remove':
            arr.remove(int(command[1]))
        elif cmd_type == 'append':
            arr.append(int(command[1]))
        elif cmd_type == 'sort':
            arr.sort()
        elif cmd_type == 'pop':
            arr.pop()
        elif cmd_type == 'reverse':
            arr.reverse()
