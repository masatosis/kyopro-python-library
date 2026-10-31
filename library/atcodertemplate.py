# atcodertemplate
import numpy as np


def get_nearest_value(arr, num):
    """
    概要: リストからある値に最も近い値を返却する関数
    @param arr: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """

    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(arr) - num).argmin()

    return arr[idx]


def cmb(n, r, p):
    if n < r:
        return 0
    r = min(n - r, r)
    if r == 0:
        return 1
    over = 1
    for i in range(n, n - r, -1):
        over = over * i % p
    under = 1
    for i in range(1, r + 1):
        under = under * i % p
    inv = pow(under, p - 2, p)
    return over * inv % p


def cmb(n, r):
    if n < r:
        return 0
    if n - r < r:
        r = n - r
    if r == 0:
        return 1
    if r == 1:
        return n

    numerator = [n - r + k + 1 for k in range(r)]
    denominator = [k + 1 for k in range(r)]

    for p in range(2, r + 1):
        pivot = denominator[p - 1]
        if pivot > 1:
            offset = (n - r) % p
            for k in range(p - 1, r, p):
                numerator[k - offset] /= pivot
                denominator[k] /= pivot

    result = 1
    for k in range(r):
        if numerator[k] > 1:
            result *= int(numerator[k])

    return result


# 二項係数
class Combination:
    """MOD上の
    計算量：階乗・逆元テーブルの作成O(N)
    nCkを求めるO(1)"""

    def __init__(self, n, MOD):
        self.fact = [1] * (n + 1)
        for i in range(1, n + 1):
            # self.fact.append(self.fact[-1] * i % MOD)
            self.fact[i] = (self.fact[i - 1] * i) % MOD
        self.inv_fact = [pow(self.fact[i], MOD - 2, MOD) for i in range(n + 1)]
        self.MOD = MOD

    def factorial(self, k):
        """k!を求める O(1)"""
        return self.fact[k]

    def inverse_factorial(self, k):
        """k!の逆元を求める O(1)"""
        return self.inv_fact[k]

    def permutation(self, k, r):
        """kPrを求める O(1)"""
        if k < r:
            return 0
        return (self.fact[k] * self.inv_fact[r]) % self.MOD

    def combination(self, k, r):
        """kCrを求める O(1)"""
        if k < r:
            return 0
        return (self.fact[k] * self.inv_fact[k - r] * self.inv_fact[r]) % self.MOD


# 使用例
# N = int(input())
# MOD = 10**9 + 7
# comb = Combination(N, MOD) # インスタンス化
# comb.combination(n,k) # nCk

"""nを素因数分解"""
"""2以上の整数n => [[素因数, 指数], ...]の2次元リスト"""
"""計算量O(√N)"""


def factorization(n):
    arr = []
    temp = n
    for i in range(2, int(-(-(n**0.5) // 1)) + 1):
        if temp % i == 0:
            cnt = 0
            while temp % i == 0:
                cnt += 1
                temp //= i
            arr.append([i, cnt])

    if temp != 1:
        arr.append([temp, 1])

    # if arr==[]:  # n=1のとき、[1,1]を返す
    #     arr.append([n, 1])

    return arr


factorization(24)

## [[2, 3], [3, 1]]
##  24 = 2^3 * 3^1


"""
約数全列挙
"""


def make_divisors(n):
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)

    # divisors.sort()
    return divisors


# 最大公倍数、最小公倍数
from functools import reduce


def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x


def gcdd(l):
    return reduce(gcd, l)


def gcd(x, y):
    if y == 0:
        return x
    return gcd(y, x % y)


def lcm(x, y):
    return x * y // gcd(x, y)


def lcmm(l):
    return reduce(lcm, l)


def isprime(x):
    # 素数判定
    if x == 2:
        return True
    if x < 2 or x % 2 == 0:
        return False
    i = 3
    while i <= x**0.5:
        if x % i == 0:
            return False
        i += 2
    return True


"""
エラトステネスの篩
MAXまでの整数について素数かどうかをテーブルで持っておく
"""
MAX = 10**5 + 1
isprime = [True] * (MAX)
isprime[0] = False
isprime[1] = False
for i in range(2, MAX):
    if isprime[i]:
        for j in range(i + i, MAX, i):
            isprime[j] = False


def get_primes(n):
    """nまでの素数リスト"""
    candidates = [0, 1] * (n // 2 + 1)
    if n % 2 == 0:
        candidates.pop()
    candidates[1] = 0
    candidates[2] = 1
    for p in range(3, int(n**0.5) + 1, 2):
        if candidates[p]:
            for m in range(p * p, n + 1, 2 * p):
                candidates[m] = 0
    return [p for p, b in enumerate(candidates) if b]


# n進数変換関連
def base_n_to_10(num: str, b: int) -> int:
    """
    b進数表記のnumを10進数に変換する
    (
    2進数、8進数、16進数であれば、組み込み関数 int()でできる
    ex.
    print(int('10'))
    print(int('10', 2))
    # 10
    # 2
    )
    """
    n = 0
    numlist = list(num)
    while numlist:
        n *= b
        n += int(numlist.pop(0))
    return n


def base_10_to_n(n: int, b: int) -> str:
    """
    10進数nを、b進数に変換し、結果を文字列で返す
    """
    if n == 0:
        return "0"
    res = ""
    while n > 0:
        res = str(n % b) + res
        n //= b
    return res


# def base_10_to_n(n, b):
#     """
#     10進数nを、b進数に変換し、結果を文字列で返す
#     """
#     if n // b:
#         return base_10_to_n(n // b, b) + str(n % b)
#     return str(n % b)


def kousa_check(a, b, c, d):
    # 2つの区間, 共通部分, 重なるか, 交差判定
    # 2 ​つの閉区間 ​[a,b],[c,d]​が共通部分を持つかの判定は ​max(a,c)≤min(b,d) ​と書くことができます。
    return max(a, c) <= min(b, d)


# ランレングス圧縮, run length encoding
from itertools import groupby


# RUN LENGTH ENCODING str -> tuple
def run_length_encode(S: str):
    """
    'AAAABBBCCDAABBB' -> [('A', 4), ('B', 3), ('C', 2), ('D', 1), ('A', 2), ('B', 3)]
    """
    grouped = groupby(S)
    res = []
    for k, v in grouped:
        res.append((k, len(list(v))))
    return res


# N以下の高度合成数を列挙したリストを返す
def hcn_heapq(N):
    from heapq import heappop, heappush
    from math import log

    prime = [
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
        101,
        103,
        107,
        109,
        113,
        127,
        131,
        137,
        139,
        149,
        151,
        157,
        163,
        167,
        173,
        179,
        181,
        191,
        193,
        197,
        199,
        211,
        223,
        227,
        229,
        233,
        239,
        241,
        251,
        257,
        263,
    ]
    lim = [[2 * int(log(p, q)) for q in prime] for p in prime]  # 枝刈り用配列
    # 初期状態
    q = [(2, 2, [1])]  # (n,nの約数の個数、nの指数表記)を保存する heapq
    res = [(1, 1, [])]

    while q and q[0][0] <= N:
        n, val, lst = heappop(q)
        if val > res[-1][1]:  # 条件をみたすなら答に追加
            res.append((n, val, lst[:]))
        L = len(lst)
        e0 = lst[0]
        # 全部１なら新しい素数で横に伸ばせる
        if e0 == 1:
            heappush(q, (n * prime[L], val * 2, [1] * (L + 1)))
        # 最上段の上を横方向に積む
        for i in range(L):
            if e0 > lst[i]:
                break  # 段差があると、もう伸ばせない
            if e0 >= lim[L][i]:
                break  # 枝刈り（重要）
            n *= prime[i]
            if n <= N:
                lst[i] += 1
                val = val // (e0 + 1) * (e0 + 2)
                heappush(q, (n, val, lst[:]))
    return res


N = 10**100
res = hcn_heapq(N)
print(len(res))  # N以下の高度合成数の個数
# 1381
print(res[-1])  # N以下の最大の高度合成数


def myceil(n, x):
    """
    切り上げ
    [N/X] [ ]ガウス記号 N,Xは正整数
    (N+X-1)/X
    """
    return (n + x - 1) // x


from functools import lru_cache


@lru_cache(maxsize=None)
def popcount(x):
    return bin(x).count("1")


def next_permutation(P):
    """
    https://twitter.com/u2dayo/status/1589271826626072578?s=20&t=TlSm1CUNSgu-Yy8WD-98kA
    """
    A = list(P)
    N = len(A)
    for i in reversed(range(N - 1)):
        if A[i] < A[i + 1]:
            j = N - 1
            while A[i] >= A[j]:
                j -= 1
            A[i], A[j] = A[j], A[i]
            A[i + 1 :] = A[i + 1 :][::-1]
            return A
    else:
        return None


def prev_permutation(P):
    """
    https://twitter.com/u2dayo/status/1589271826626072578?s=20&t=TlSm1CUNSgu-Yy8WD-98kA
    """
    A = list(P)
    N = len(A)
    for i in reversed(range(N - 1)):
        if A[i] > A[i + 1]:
            j = N - 1
            while A[i] <= A[j]:
                j -= 1
            A[i], A[j] = A[j], A[i]
            A[i + 1 :] = A[i + 1 :][::-1]
            return A
    else:
        return None


def graph_show(G):
    # グラフ一覧表示,　デバッグ用
    for i in range(len(G)):
        print(f"{i}: {G[i]}")


# n! は p で何回割り切れるか（ルジャンドルの定理）
def legendre(n, p):
    res = 0
    p2 = p
    while True:
        tmp = n // p2
        if tmp == 0:
            break
        res += tmp
        p2 *= p
    return res


# 比較関数
class Compare:
    def __init__(self, x) -> None:
        self.x = x

    def __lt__(self, other):
        return self.x > other.x  # 降順
        # return self.x < other.x # 昇順

    def __repr__(self) -> str:
        return str(self.x)


A = list(map(int, input().split()))
B = [Compare(a) for a in A]
B.sort()
print(B)

# in
# 1 2 3 4 5
# out
# [5, 4, 3, 2, 1]

from typing import Union


def is_palindrome(s: Union[str, list]) -> bool:
    """
    sが回文か判定
    sは文字列またはリスト
    """
    for i in range(len(s) // 2):
        if s[i] != s[-i - 1]:
            return False
    return True


def z_algorithm(S: str) -> list:
    """
    Zアルゴリズムを用いて、文字列 S の Z-array を計算します。

    Z-array の各要素 Z[i] は、文字列 S の i 番目以降で、
    S の接頭辞と一致する最長部分文字列の長さを表します。

    パラメータ:
        S (str): 入力文字列

    戻り値:
        list: Z-array（整数のリスト）

    使用例:
        入力: "abracadabra"
        出力: [11, 0, 0, 1, 0, 1, 0, 4, 0, 0, 1]
    """
    N = len(S)  # 文字列 S の長さを取得
    Z = [0] * N  # Z-arrayを初期化（すべての要素を 0 で初期化）
    Z[0] = N  # Z[0] は文字列全体と一致するため、文字列の長さに設定
    i = 1  # 現在の探索開始位置（1文字目以降）
    j = 0  # 現在の一致文字数

    # 文字列全体を走査して Z-array を計算する
    while i < N:
        # 文字列 S の i 番目から始まる部分文字列と S の接頭辞を比較し、
        # 一致する文字数を j にカウントする
        while i + j < N and S[j] == S[i + j]:
            j += 1
        Z[i] = j  # 一致した文字数を Z[i] に格納

        # 一致がなかった場合は次の位置に移動
        if j == 0:
            i += 1
            continue

        # 一致した部分を利用して、Z-arrayの値を効率的に設定する
        k = 1
        while k < j and k + Z[k] < j:
            Z[i + k] = Z[k]
            k += 1

        # 次の探索位置に移動し、一致文字数を調整する
        i += k
        j -= k

    return Z


# 3次元配列 (D x H x W) を1次元配列に変換するユーティリティ
# D: 奥行き, H: 高さ(行数), W: 幅(列数)


# (z, x, y) -> 1次元インデックス
def to_idx(z, x, y):
    return z * H * W + x * W + y


# 1次元インデックス -> (z, x, y)
def to_z_x_y(idx):
    z = idx // (H * W)
    x = (idx % (H * W)) // W
    y = idx % W
    return z, x, y


# --- 2次元配列 (H x W) ---
def to_xy(x, y):
    return x * W + y


def to_x_y(pos):
    return pos // W, pos % W
