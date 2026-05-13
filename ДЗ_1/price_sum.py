import csv

if __name__ == '__main__':
    adult_sum = 0.0
    pensioner_sum = 0.0
    child_sum = 0.0
    
    with open('products.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            next(reader) # Skip header
        except StopIteration:
            pass
            
        for row in reader:
            if not row:
                continue
            try:
                # Handle possible empty strings or bad format if necessary, 
                # but assuming clean data based on file view
                if len(row) >= 4:
                    adult_sum += float(row[1]) if row[1] else 0.0
                    pensioner_sum += float(row[2]) if row[2] else 0.0
                    child_sum += float(row[3]) if row[3] else 0.0
            except ValueError:
                continue
                
    print(f"{adult_sum:.2f} {pensioner_sum:.2f} {child_sum:.2f}")
