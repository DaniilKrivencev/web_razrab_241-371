if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    n = int(input())
    students = []
    for _ in range(n):
        name = input()
        score = float(input())
        students.append([name, score])
    
    # Extract unique scores and sort them
    scores = sorted(list(set([s[1] for s in students])))
    second_lowest_score = scores[1]
    
    # Find students with second lowest score
    second_best_students = [s[0] for s in students if s[1] == second_lowest_score]
    
    # Print sorted names
    for name in sorted(second_best_students):
        print(name)
