if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    # Parse n and m
    first_line = input().split()
    if not first_line:
        exit()
    n = int(first_line[0])
    m = int(first_line[1])
    
    items = []
    for _ in range(m):
        line = input().split()
        name = line[0]
        weight = int(line[1])
        cost = int(line[2])
        if weight > 0:
            ratio = cost / weight
            items.append({'name': name, 'weight': weight, 'cost': cost, 'ratio': ratio})
        else:
             # Handle 0 weight? value infinite? usually not in test cases or just take it all. 
             # Assuming positive weight.
             pass

    # Sort by ratio descending
    items.sort(key=lambda x: x['ratio'], reverse=True)
    
    taken_items = []
    remaining_cap = n
    
    for item in items:
        if remaining_cap <= 0:
            break
            
        if item['weight'] <= remaining_cap:
            taken_items.append({
                'name': item['name'],
                'weight': float(item['weight']),
                'cost': float(item['cost'])
            })
            remaining_cap -= item['weight']
        else:
            fraction = remaining_cap / item['weight']
            taken_cost = item['cost'] * fraction
            taken_items.append({
                'name': item['name'],
                'weight': float(remaining_cap),
                'cost': float(taken_cost)
            })
            remaining_cap = 0
            
    # Output: Sort by cost descending
    taken_items.sort(key=lambda x: x['cost'], reverse=True)
    
    for item in taken_items:
        # Format weight and cost to 2 decimals
        print(f"{item['name']} {item['weight']:.2f} {item['cost']:.2f}")
