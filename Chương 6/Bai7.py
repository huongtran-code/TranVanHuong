# List đầu vào
_list = ['abc', 'xyz', 'abc', '12', 'ii', '12', '5a']

new1 = []

for i in _list:
    if _list.count(i) == 1:
        new1.append(i)

print("List chỉ chứa phần tử không trùng:")
print(new1)

new2 = []

for i in _list:
    if i not in new2:
        new2.append(i)

print("List loại bỏ phần tử trùng (giữ lại 1 phần tử):")
print(new2)