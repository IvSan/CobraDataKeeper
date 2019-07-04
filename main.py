from blockchain.chain import Chain
from blockchain.note import Note

chain = Chain()
chain.add_block()
chain.store_data(Note('ab'))
chain.add_block()
chain.store_data(Note(45))
chain.add_block()
chain.store_data(Note([]))
print('Done')
print(chain)
