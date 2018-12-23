import hashlib
import json


class Block:

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index

        self.timestamp = timestamp

        self.data = data

        self.previous_hash = previous_hash

        self.hash = self.hash_block()

    def hash_block(self):
        return hashlib.sha256(str(str(self.index) +

                   str(self.timestamp) +

                   str(self.data) +

                   str(self.previous_hash)).encode('utf-8')).hexdigest()






import datetime as date

def SetListBlockchain(blocklist):
    db = json.load(open('database.json', encoding='utf8'))
    for i in range(1, len(blocklist)):
        hdict={"Номер СНИЛСа:" : blocklist[i].data[0], "Статус утверждения возраста:" : blocklist[i].data[1]}
        db['Data'].append(hdict)

    with open('database.json', 'w', encoding='utf-8') as output:
        output.write(json.dumps(db, ensure_ascii=False, indent=4))
        output.close()
def create_genesis_block():#Генерация начального блока
    return Block(0, date.datetime.now(), "Genesis Block", "0")

def next_block(index,hash, data):
    this_index = index + 1
    this_timestamp = date.datetime.now()

    this_data = data

    this_hash = hash

    return Block(this_index, this_timestamp, this_data, this_hash)

genesis_block = create_genesis_block()
blocks_list = []
blocks_list.append(genesis_block)
for i in range(2):#Количество пользователей системы
    snils = input("Enter snils value: ")#Я решил взять снилс, так как данные паспорта проще узнать
    data = [snils, "Moderation..."]
    previous_block = next_block(genesis_block.index, genesis_block.hash, data)
    blocks_list.append(previous_block)
    genesis_block = previous_block
    print("Block #{} has been added to the blockchain!".format(previous_block.index))
    print("Hash: {}\n".format(previous_block.hash))
    print("Data: " + str(previous_block.data))
SetListBlockchain(blocks_list)