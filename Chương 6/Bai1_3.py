_tuple = ('ab', 'b', 'e', 'c', 'd', 'e', 'ab')

_new_list = []

for phan_tu in _tuple:
    if _new_list.count(phan_tu) == 0:
        _new_list.append(phan_tu)

_new_tuple = tuple(_new_list)

print(f"Tuple ban đầu: {_tuple}")
print(f"Tuple sau khi loại bỏ trùng lặp: {_new_tuple}")