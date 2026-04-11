def cong_phan_so(tu1, mau1, tu2, mau2):
    tu_moi = tu1 * mau2 + tu2 * mau1
    mau_moi = mau1 * mau2
    return f"{tu_moi}/{mau_moi}"

def tru_phan_so(tu1, mau1, tu2, mau2):
    tu_moi = tu1 * mau2 - tu2 * mau1
    mau_moi = mau1 * mau2
    return f"{tu_moi}/{mau_moi}"

def nhan_phan_so(tu1, mau1, tu2, mau2):
    return f"{tu1 * tu2}/{mau1 * mau2}"

def chia_phan_so(tu1, mau1, tu2, mau2):
    return f"{tu1 * mau2}/{mau1 * tu2}"