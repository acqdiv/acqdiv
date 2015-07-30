import json

with open('test.json', 'r') as f:
    data = json.load(f)
    print(data['CHAT']['u'])
#    print(json.dumps(data['CHAT']['u']))
