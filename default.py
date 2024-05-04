def undef(row, cursor):
    return row, cursor, undef

def true(row, cursor):
    print('End')
    sts.destroy()
    while True:
        res.update()
    return row, cursor, true
