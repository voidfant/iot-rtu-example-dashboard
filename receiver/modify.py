with open('receiver/test_data.csv') as f:
    f = [x.strip() for x in f.read().split('\n')]
    f.pop()

res = ''

for k, v in enumerate(f):
    res += str(k + 1) + ';' + v + '\n'

with open('receiver/new_data.csv', 'w') as f:
    f.write(res)

