import math

# Hình tròn
def chu_vi_tron(ban_kinh):
    return 2 * math.pi * ban_kinh

def dien_tich_tron(ban_kinh):
    return math.pi * (ban_kinh ** 2)

# Hình chữ nhật
def chu_vi_hcn(dai, rong):
    return (dai + rong) * 2

def dien_tich_hcn(dai, rong):
    return dai * rong