


def recursive_search(num,index):
    numbers = [1,2,3,4,5,6]
    
    if index < len(numbers):
        if numbers[index] != num:
            return recursive_search(num,index+1)
        else:
            return f"num {num} found at index {index}"
        
    return "Not found"


##
if __name__ == '__main__':
    users_num = input("type a number:")
    users_num = int(users_num.strip())
    result = recursive_search(users_num,0)
    print(result)