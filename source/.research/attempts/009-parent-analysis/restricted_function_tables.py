"""Restrict finite function domains by explicit injective parent-index maps."""


def restrict_tables(tables,indices):
    assert len(tables)==len(indices)
    for table,rows in zip(tables,indices):
        assert rows and len(rows)==len(set(rows))
        assert all(type(i)is int and 0<=i<len(table)for i in rows)
    return [table[rows]for table,rows in zip(tables,indices)]
