def compress(X):
    """
    数列 X をソートした結果を vals とする (setに入れるので重複は削除される)
    X のそれぞれの要素について、vals の中の何番目に出現するか 辞書b に格納
    """
    vals = sorted(set(X))
    b = {a: i for i, a in enumerate(vals)}
    return b

def compress2d(X1, X2):
    """
    X1,X2 と Y1,Y2 で分けて、一次元での座標圧縮を行う(以下 X1,X2 について考える)
    X1,X2 の要素と、その一つ隣の要素を全てまとめて、ソートした結果を vals とする(setに入れるので重複は削除される)
    X1,X2 のそれぞれの要素について、vals の中の何番目に出現するか 辞書b に格納
    返り値:
        b: X1,X2 のそれぞれの要素について、vals の中の何番目に出現するか  
        vals: ソートされ重複要素を除いた値
    """
    tmp = set()
    for li in (X1, X2):
        for x in li:
            tmp.add(x)
            # tmp.add(x + 1)
    vals = sorted(tmp)
    b = {a: i for i, a in enumerate(vals)}
    return b, vals
  
