import json

f = open('user.json')
data = json.load(f)

#wow = json.dumps(data, indent=4)
wow = json.dumps(data)

print(wow)

print("#")
print("##################################################################################")
print("#")

zap = json.loads(wow)
cut = zap['userinfo']
#slim = json.dumps(cut, indent=4)

print(cut)

print("#")
print("##################################################################################")
print("#")

sub = cut['sub']

print(sub)

print("#")
print("##################################################################################")
print("#")

#test = data['userinfo']['sub']

#print(test)
