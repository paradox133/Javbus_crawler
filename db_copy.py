import sqlite3
import sys

# NOT WORKING YET
def open_db(nam):
    conn = sqlite3.connect(nam)
    # Let rows returned be of dict/tuple type
    conn.row_factory = sqlite3.Row
    print ("Openned database %s as %r" % (nam, conn))
    return conn

def copy_table(table, src, dest):
    print ("Copying %s %s => %s" % (table, src, dest))
    sc = src.execute('SELECT * FROM %s' % table)
    ins = None
    dc = dest.cursor()
    for row in sc.fetchall():
        if not ins:
            cols = tuple([k for k in row.keys() if k != 'id'])
            ins = 'INSERT OR REPLACE INTO %s %s VALUES (%s)' % (table, cols,
                                                     ','.join(['?'] * len(cols)))
            print ('INSERT stmt = ' + ins)
        c = [row[c] for c in cols]
        dc.execute(ins, c)

    dest.commit()

src_conn  = open_db("E:\VS Projects\Vscode\javsdt\TestDB.db")
dest_conn = open_db("javbus1.sqlite3 copy.db")

copy_table('DISTINCTID', src_conn, dest_conn)