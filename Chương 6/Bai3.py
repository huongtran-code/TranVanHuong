_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Tạo hai list mới
even_list = []
odd_list = []

for num in _list:
    if num % 2 == 0:
        even_list.append(num)
    else:
        odd_list.append(num)

# In ra hai list
print("List số chẵn:", even_list)
print("List số lẻ:", odd_list)