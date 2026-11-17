


def fibonacci(n):
    a,b =0,1
    total = 0
    
    for i in range(n):
        total+=a
        a,b = b, b+a
        
    return total
    
    
print(fibonacci(50))