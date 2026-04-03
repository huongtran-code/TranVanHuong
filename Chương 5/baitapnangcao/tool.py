import os
import re
import math
import sys
from collections import Counter

def doc_file(duong_dan: str) -> str:
    """Đọc nội dung file, trả về chuỗi rỗng nếu không tìm thấy."""
    if not os.path.exists(duong_dan):
        print(f"  [!] Không tìm thấy file: {duong_dan}")
        return ""
    with open(duong_dan, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def tach_token(code: str) -> list:
    """Tách token từ code Python (bỏ comment và chuỗi docstring)."""
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)          
    code = re.sub(r'"""[\s\S]*?"""', '', code)                     
    code = re.sub(r"'''[\s\S]*?'''", '', code)                     
    return [t for t in code.lower().split() if t]


def lay_dong_code(code: str) -> list:
    """Lấy danh sách dòng code có nghĩa (bỏ comment, dòng trắng)."""
    lines = []
    for line in code.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            lines.append(line)
    return lines


def lay_ten_ham(code: str) -> list:
    """Trích xuất tên các hàm được định nghĩa bằng def."""
    return re.findall(r'def\s+(\w+)\s*\(', code)


def lay_ten_bien(code: str) -> list:
    """Trích xuất tên biến từ các phép gán."""
    return re.findall(r'^(\w+)\s*=', code, flags=re.MULTILINE)


def phan_tich_logic(code: str) -> dict:
    """Đếm số lần xuất hiện của các cấu trúc logic."""
    patterns = {
        'if/elif/else': r'\b(if|elif|else)\b',
        'for loop':     r'\bfor\b',
        'while loop':   r'\bwhile\b',
        'try/except':   r'\b(try|except)\b',
        'return':       r'\breturn\b',
        'import':       r'\b(import|from)\b',
        'class':        r'\bclass\b',
        'lambda':       r'\blambda\b',
        'with':         r'\bwith\b',
        'list comp':    r'\[.+\s+for\s+.+\s+in\s+.+\]',
    }
    result = {}
    for name, pat in patterns.items():
        count = len(re.findall(pat, code))
        if count > 0:
            result[name] = count
    return result


def cosine_similarity(list_a: list, list_b: list) -> float:
    """Tính độ tương đồng cosine giữa 2 danh sách token."""
    if not list_a or not list_b:
        return 0.0
    freq_a = Counter(list_a)
    freq_b = Counter(list_b)
    all_keys = set(freq_a.keys()) | set(freq_b.keys())
    dot = sum(freq_a.get(k, 0) * freq_b.get(k, 0) for k in all_keys)
    norm_a = math.sqrt(sum(v ** 2 for v in freq_a.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in freq_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def jaccard_similarity(list_a: list, list_b: list) -> float:
    """Tính độ tương đồng Jaccard giữa 2 tập hợp."""
    set_a = set(list_a)
    set_b = set(list_b)
    if not set_a and not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


def overlap_coefficient(list_a: list, list_b: list) -> float:
    """Tỉ lệ phần tử chung so với tập nhỏ hơn."""
    set_a = set(list_a)
    set_b = set(list_b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / min(len(set_a), len(set_b))


def tim_dong_chung(lines_a: list, lines_b: list, min_len: int = 10) -> list:
    """Tìm các dòng code xuất hiện ở cả 2 file (dài hơn min_len ký tự)."""
    set_b = set(lines_b)
    return [l for l in lines_a if len(l) >= min_len and l in set_b]


def bigram(words: list) -> list:
    """Tạo danh sách bigram (cụm 2 từ liên tiếp)."""
    return [words[i] + ' ' + words[i+1] for i in range(len(words)-1)]


def phan_tich_code(code1: str, code2: str) -> dict:
    """Phân tích toàn diện mức độ trùng lặp giữa 2 đoạn code Python."""
    # Tách dữ liệu
    tokens1 = tach_token(code1)
    tokens2 = tach_token(code2)
    lines1  = lay_dong_code(code1)
    lines2  = lay_dong_code(code2)
    funcs1  = lay_ten_ham(code1)
    funcs2  = lay_ten_ham(code2)
    vars1   = lay_ten_bien(code1)
    vars2   = lay_ten_bien(code2)
    logic1  = phan_tich_logic(code1)
    logic2  = phan_tich_logic(code2)

    # Tính điểm tương đồng
    token_sim  = cosine_similarity(tokens1, tokens2)
    line_sim   = jaccard_similarity(lines1, lines2)
    func_sim   = overlap_coefficient(funcs1, funcs2) if (funcs1 or funcs2) else 0
    var_sim    = jaccard_similarity(vars1, vars2)

    # Logic similarity: so sánh phân phối cấu trúc
    all_keys   = set(logic1) | set(logic2)
    logic_sim  = 0.0
    if all_keys:
        matches = sum(1 for k in all_keys if (k in logic1) == (k in logic2))
        logic_sim = matches / len(all_keys)

    # Điểm tổng hợp (trọng số)
    overall = (token_sim * 0.30 + line_sim * 0.30 +
               func_sim  * 0.15 + var_sim  * 0.10 +
               logic_sim * 0.15)

    common_lines = tim_dong_chung(lines1, lines2)
    func_chung   = [f for f in funcs1 if f in funcs2]
    var_chung    = list(set(vars1) & set(vars2))

    return {
        'overall':      round(overall * 100, 1),
        'token_sim':    round(token_sim * 100, 1),
        'line_sim':     round(line_sim * 100, 1),
        'func_sim':     round(func_sim * 100, 1),
        'var_sim':      round(var_sim * 100, 1),
        'logic_sim':    round(logic_sim * 100, 1),
        'so_dong_1':    len(lines1),
        'so_dong_2':    len(lines2),
        'ham_1':        funcs1,
        'ham_2':        funcs2,
        'ham_chung':    func_chung,
        'var_chung':    var_chung[:10],
        'dong_chung':   common_lines[:10],
        'logic_1':      logic1,
        'logic_2':      logic2,
    }


def phan_tich_bao_cao(text1: str, text2: str) -> dict:
    """Phân tích mức độ trùng lặp văn bản báo cáo / tiểu luận."""
    words1 = [w for w in text1.lower().split() if len(w) > 3]
    words2 = [w for w in text2.lower().split() if len(w) > 3]

    sents1 = [s.strip() for s in re.split(r'[.!?\n]+', text1) if len(s.strip()) > 20]
    sents2 = [s.strip() for s in re.split(r'[.!?\n]+', text2) if len(s.strip()) > 20]
    sents1_lower = [s.lower() for s in sents1]
    sents2_lower = [s.lower() for s in sents2]

    bg1 = bigram(words1)
    bg2 = bigram(words2)

    word_sim   = cosine_similarity(words1, words2)
    sent_sim   = jaccard_similarity(sents1_lower, sents2_lower)
    bigram_sim = jaccard_similarity(bg1, bg2)

    overall = (word_sim * 0.30 + sent_sim * 0.40 + bigram_sim * 0.30)

    cau_chung = [s for s in sents1 if s.lower() in sents2_lower]

    return {
        'overall':    round(overall * 100, 1),
        'word_sim':   round(word_sim * 100, 1),
        'sent_sim':   round(sent_sim * 100, 1),
        'bigram_sim': round(bigram_sim * 100, 1),
        'so_tu_1':    len(words1),
        'so_tu_2':    len(words2),
        'so_cau_1':   len(sents1),
        'so_cau_2':   len(sents2),
        'cau_chung':  cau_chung[:5],
    }



def xep_loai(pct: float) -> str:
    if pct < 31:
        return "THẤP (bình thường)"
    elif pct < 61:
        return "TRUNG BÌNH (cần xem xét)"
    else:
        return "CAO (nghi vấn sao chép)"


def thanh_tien_trinh(pct: float, width: int = 30) -> str:
    filled = int(pct / 100 * width)
    bar = '█' * filled + '░' * (width - filled)
    return f"[{bar}] {pct:5.1f}%"


def in_ket_qua_code(r: dict, ten1: str, ten2: str):
    sep = "=" * 60
    print(f"\n{sep}")
    print("  KẾT QUẢ PHÂN TÍCH TRÙNG LẶP CODE")
    print(sep)
    print(f"  Sản phẩm 1 : {ten1}  ({r['so_dong_1']} dòng code)")
    print(f"  Sản phẩm 2 : {ten2}  ({r['so_dong_2']} dòng code)")
    print(sep)

    print(f"\n  ► ĐIỂM TỔNG HỢP  : {thanh_tien_trinh(r['overall'])}")
    print(f"    Xếp loại        : {xep_loai(r['overall'])}\n")

    print("  Chi tiết:")
    print(f"    Token / từ khoá : {thanh_tien_trinh(r['token_sim'])}")
    print(f"    Dòng code       : {thanh_tien_trinh(r['line_sim'])}")
    print(f"    Tên hàm (def)   : {thanh_tien_trinh(r['func_sim'])}")
    print(f"    Tên biến        : {thanh_tien_trinh(r['var_sim'])}")
    print(f"    Cấu trúc logic  : {thanh_tien_trinh(r['logic_sim'])}")

    print(f"\n  Hàm sản phẩm 1 : {r['ham_1'] or ['(không có)']}")
    print(f"  Hàm sản phẩm 2 : {r['ham_2'] or ['(không có)']}")
    if r['ham_chung']:
        print(f"  Hàm TRÙNG NHAU : {r['ham_chung']}")
    if r['var_chung']:
        print(f"  Biến trùng nhau: {r['var_chung']}")

    if r['dong_chung']:
        print(f"\n  Các dòng code GIỐNG NHAU ({len(r['dong_chung'])} dòng):")
        for i, line in enumerate(r['dong_chung'], 1):
            print(f"    {i:2}. {line}")

    print(f"\n  Cấu trúc logic sản phẩm 1: {r['logic_1']}")
    print(f"  Cấu trúc logic sản phẩm 2: {r['logic_2']}")
    print(sep)


def in_ket_qua_bao_cao(r: dict, ten1: str, ten2: str):
    sep = "=" * 60
    print(f"\n{sep}")
    print("  KẾT QUẢ PHÂN TÍCH TRÙNG LẶP BÁO CÁO")
    print(sep)
    print(f"  Báo cáo 1 : {ten1}  ({r['so_tu_1']} từ, {r['so_cau_1']} câu)")
    print(f"  Báo cáo 2 : {ten2}  ({r['so_tu_2']} từ, {r['so_cau_2']} câu)")
    print(sep)

    print(f"\n  ► ĐIỂM TỔNG HỢP  : {thanh_tien_trinh(r['overall'])}")
    print(f"    Xếp loại        : {xep_loai(r['overall'])}\n")

    print("  Chi tiết:")
    print(f"    Từ vựng         : {thanh_tien_trinh(r['word_sim'])}")
    print(f"    Câu văn         : {thanh_tien_trinh(r['sent_sim'])}")
    print(f"    Cụm từ 2-gram   : {thanh_tien_trinh(r['bigram_sim'])}")

    if r['cau_chung']:
        print(f"\n  Câu văn GIỐNG NHAU ({len(r['cau_chung'])} câu):")
        for i, s in enumerate(r['cau_chung'], 1):
            print(f"    {i}. {s[:100]}{'...' if len(s) > 100 else ''}")
    print(sep)


def menu_nhap_tay():
    """Chế độ nhập nội dung trực tiếp từ bàn phím."""
    print("\nNhập code / văn bản (gõ 'END' trên một dòng riêng để kết thúc):")

    def nhap_nhieu_dong(ten):
        print(f"\n--- {ten} ---")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip() == 'END':
                break
            lines.append(line)
        return '\n'.join(lines)

    return nhap_nhieu_dong("Sản phẩm 1"), nhap_nhieu_dong("Sản phẩm 2")


def chay_voi_file(f1: str, f2: str, che_do: str):
    """Chạy phân tích với 2 file đầu vào."""
    noi_dung_1 = doc_file(f1)
    noi_dung_2 = doc_file(f2)
    if not noi_dung_1 or not noi_dung_2:
        print("Không thể đọc file. Thoát.")
        return

    if che_do == 'code':
        ket_qua = phan_tich_code(noi_dung_1, noi_dung_2)
        in_ket_qua_code(ket_qua, f1, f2)
    else:
        ket_qua = phan_tich_bao_cao(noi_dung_1, noi_dung_2)
        in_ket_qua_bao_cao(ket_qua, f1, f2)


def main():
    print("=" * 60)
    print("  CÔNG CỤ KIỂM TRA TRÙNG LẶP CODE & BÁO CÁO PYTHON")
    print("=" * 60)

    if len(sys.argv) == 4:
        che_do = sys.argv[1].lower()
        chay_voi_file(sys.argv[2], sys.argv[3], che_do)
        return

    print("\nChọn chế độ phân tích:")
    print("  1. Phân tích CODE Python")
    print("  2. Phân tích BÁO CÁO / tiểu luận")
    print("  3. Thoát")

    lua_chon = input("\nNhập lựa chọn (1/2/3): ").strip()

    if lua_chon == '3':
        print("Tạm biệt!")
        return

    if lua_chon not in ('1', '2'):
        print("Lựa chọn không hợp lệ!")
        return

    che_do = 'code' if lua_chon == '1' else 'report'

    print("\nNguồn dữ liệu:")
    print("  1. Nhập đường dẫn file")
    print("  2. Nhập trực tiếp nội dung")
    nguon = input("Chọn (1/2): ").strip()

    if nguon == '1':
        f1 = input("Đường dẫn file sản phẩm 1: ").strip()
        f2 = input("Đường dẫn file sản phẩm 2: ").strip()
        chay_voi_file(f1, f2, che_do)

    elif nguon == '2':
        nd1, nd2 = menu_nhap_tay()
        if che_do == 'code':
            kq = phan_tich_code(nd1, nd2)
            in_ket_qua_code(kq, "Sản phẩm 1 (nhập tay)", "Sản phẩm 2 (nhập tay)")
        else:
            kq = phan_tich_bao_cao(nd1, nd2)
            in_ket_qua_bao_cao(kq, "Báo cáo 1 (nhập tay)", "Báo cáo 2 (nhập tay)")
    else:
        print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()