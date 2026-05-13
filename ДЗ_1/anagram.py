if __name__ == '__main__':
    s1 = input()
    s2 = input()
    
    if sorted(s1) == sorted(s2):
        print("YES")
    else:
        print("NO")
