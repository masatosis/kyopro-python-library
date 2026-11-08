"""
複数の整数フィールドを、辞書順を保ったまま 1 つの int に畳むキー。

なぜ int に畳むか:
    PyPy では tuple の比較が int の比較より何倍も遅く、
    SortedSet / heapq のような比較を大量に行うデータ構造で効いてくるため。

使い方:
    K = CompositeKey((M, "max"), (N, "min"))   # 票数は大きいほど上、番号は小さいほど上
    key = K.pack(cnt, idx)                     # (票数, 番号) -> int
    cnt, idx = K.unpack(key)                   # int -> (票数, 番号)
"""


class CompositeKey:
    def __init__(self, *fields):
        """
        fields: (最大値, 向き) のタプルの並び。先頭ほど優先度が高い。
            向きが "max" ならその値が大きいほどキーが大きい
            向きが "min" ならその値が小さいほどキーが大きい
        各フィールドの値は 0 以上 最大値 以下であること。
        """
        for m, d in fields:
            assert m >= 0, "最大値は 0 以上"
            assert d in ("max", "min"), "向きは 'max' か 'min'"
        self.maxes = [m for m, _ in fields]
        self.dirs = [d for _, d in fields]
        # 桁が溢れないよう、各フィールドの桁幅は「最大値 + 1」にする
        self.bases = [m + 1 for m in self.maxes]

    def pack(self, *values):
        key = 0
        for v, m, d, b in zip(values, self.maxes, self.dirs, self.bases):
            # "min" は値を反転して「小さいほど大きい」に揃える
            digit = v if d == "max" else m - v
            key = key * b + digit
        return key

    def unpack(self, key):
        out = []
        # 下位桁から順に取り出すので、最後に反転して元の順序に戻す
        for m, d, b in zip(reversed(self.maxes), reversed(self.dirs), reversed(self.bases)):
            key, digit = divmod(key, b)
            out.append(digit if d == "max" else m - digit)
        return tuple(reversed(out))


if __name__ == "__main__":
    # 動作確認: タプルの辞書順と int の大小が一致することを検証
    import itertools
    import random

    N, M = 7, 5
    K = CompositeKey((M, "max"), (N, "min"))

    # 全組み合わせで pack/unpack が往復できること
    for v in range(M + 1):
        for k in range(1, N + 1):
            assert K.unpack(K.pack(v, k)) == (v, k)

    # 順序の一致: (v, -k) のタプル順と pack した int の順が等しいこと
    pairs = [(v, k) for v in range(M + 1) for k in range(1, N + 1)]
    for (v1, k1), (v2, k2) in itertools.product(pairs, repeat=2):
        tuple_cmp = (v1, -k1) < (v2, -k2)
        int_cmp = K.pack(v1, k1) < K.pack(v2, k2)
        assert tuple_cmp == int_cmp, ((v1, k1), (v2, k2))

    # 3 フィールドでもランダムに検証
    K3 = CompositeKey((9, "max"), (4, "min"), (6, "max"))
    for _ in range(2000):
        a = (random.randint(0, 9), random.randint(0, 4), random.randint(0, 6))
        b = (random.randint(0, 9), random.randint(0, 4), random.randint(0, 6))
        ta = (a[0], -a[1], a[2])
        tb = (b[0], -b[1], b[2])
        assert (ta < tb) == (K3.pack(*a) < K3.pack(*b)), (a, b)
        assert K3.unpack(K3.pack(*a)) == a

    print("ok")
