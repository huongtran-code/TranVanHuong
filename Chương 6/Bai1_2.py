_tuple = ('ab', 'b', 'e', 'c', 'd', 'e', 'ab')

_new_list = [phan_tu for phan_tu in _tuple if _tuple.count(phan_tu) == 1]

_new_tuple = tuple(_new_list)

print(f"Tuple ban đầu: {_tuple}")
print(f"Tuple sau khi loại bỏ các phần tử trùng nhau: {_new_tuple}")
print("-" * 50)