# Tạo file với nội dung yêu cầu
with open("demo_file1.txt", "w", encoding="utf-8") as f:
    f.write("Thuc \n hanh \n voi \n file\n IO\n")

# In nội dung trên một dòng
with open("demo_file1.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("a) Nội dung trên một dòng:")
    print(content.replace("\n", " "))

# In nội dung theo từng dòng
with open("demo_file1.txt", "r", encoding="utf-8") as f:
    print("\nb) Nội dung theo từng dòng:")
    for line in f:
        print(line, end="")