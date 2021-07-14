import json
dic = dict(json.load(open('./static/json/dictnsdc.json','r')))
dist_name = sorted(dic['TC District'].keys())
unique_dist_name = list(set(dist_name))

for dist in (dist_name):
    print(dist)