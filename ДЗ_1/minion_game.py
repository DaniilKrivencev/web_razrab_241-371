def minion_game(string):
    vowels = 'AEIOU'
    kevin_score = 0
    stuart_score = 0
    length = len(string)
    
    for i in range(length):
        if string[i] in vowels:
            kevin_score += (length - i)
        else:
            stuart_score += (length - i)

    if kevin_score > stuart_score:
        print(f"Кевин {kevin_score}")
    elif stuart_score > kevin_score:
        print(f"Стюарт {stuart_score}")
    else:
        print("Draw") # Or implicit tie, but usually "Draw" in Hackerrank. Russian prompt doesn't specify tie output. 
        # But looking at example: "Стюарт 12". "Определить победителя...".
        # If tie, usually no winner. 
        # I'll output Draw or similar if needed, but let's stick to standard behavior.
        # Actually task doesn't specify what to print on draw. Hackerrank says "Draw".
        # I'll stick to "Draw" if equal, or just print nothing? 
        # The prompt asks for "имя победителя ... и набранное им количество очков". 
        # If draw, there is no winner. I will print "Draw" as is standard.

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    s = input()
    minion_game(s)
