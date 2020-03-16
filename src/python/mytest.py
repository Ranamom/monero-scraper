__author__ = 'teemu kanstren'

from monero import jsonapi, rpc
from db import sql, create_tables
from codeprofile import profiler

#
#rpc.init(_host="nodes.hashvault.pro")
rpc.init(_host="localhost")
daemon = jsonapi
info = daemon.info()
print(info)
mtx = daemon.get_transactions(["c6988cbd8eec02efdb6ce8e43e5c54c8af898dec8d331025248a066645a259dd"])
cnx = create_tables.get_cnx()
db_height = sql.get_max_block(cnx)
if db_height[0] is None:
    #this is the case when the table is empty
    db_height = (0,)

profiler.collect_raw = False
block = daemon.get_block(height=85341)
top_height = daemon.get_height()
for x in range(db_height[0] + 1, top_height):
    with profiler.profile("get block"):
        block = daemon.get_block(height=x)
    with profiler.profile("insert block"):
        sql.insert_block(cnx, block)
    if x%100 == 0:
        print(f"block height: {x}")
        profiler.print_run_stats()
print(block)
#coinbase_tx_hash = block["block_header"]["miner_tx_hash"]
#print(coinbase_tx_hash)
#cb_transactions = daemon.get_transactions([coinbase_tx_hash])
#print(cb_transactions)
print(block.txs)
print(daemon.get_height())
mempool = daemon.mempool()
print(mempool)
top_height = daemon.get_height() - 1
block = daemon.get_block(height=top_height)
pass
