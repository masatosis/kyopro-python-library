class UnionFind:
    def __init__(self, N):
        self.N = N  # ノード数
        # 親ノードを示す。負は自身が親ということ。親だった場合は−(その集合のサイズ)
        self.parent = [-1] * N

    def root(self, A):
        # Aがどのグループに属しているか調べる
        # ノード番号を受けとって一番上の親ノードの番号を返す
        # print(A)
        if self.parent[A] < 0:
            return A
        self.parent[A] = self.root(self.parent[A])
        return self.parent[A]

    def size(self, A):
        # 自分のいるグループの頂点数を調べる
        return -self.parent[self.root(A)]

    def unite(self, A, B):
        # AとBをくっつける
        # AとBを直接つなぐのではなく、root(A)にroot(B)をくっつける
        A = self.root(A)
        B = self.root(B)

        if A == B:
            return False  # すでにくっついてるからくっつけない

        if self.size(A) < self.size(B):
            # 大きい方(A)に小さいほう(B)をくっ付けたい
            # 大小が逆だったらひっくり返しちゃう。
            A, B = B, A

        # Aのサイズを更新する
        self.parent[A] += self.parent[B]
        # Bの親をAに変更する
        self.parent[B] = A

        return True

    def same(self, A, B):
        return self.root(A) == self.root(B)

    def groups(self):
        # グラフを連結成分にわけ、その情報を返す。返り値: 1つの連結成分の頂点番号のリスト
        root_buf = [self.root(i) for i in range(self.N)]
        result = [[] for _ in range(self.N)]
        for i in range(self.N):
            result[root_buf[i]].append(i)
        return list(filter(lambda r: r, result))
