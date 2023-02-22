# 源数据
s = [{'name':'leader-1','belong_to':None},{'name':'jack','belong_to':'leader-2'},{'name':'lili','belong_to':'leader-1'},{'name':'leader-2','belong_to':None},{'name':'Tom', 'belong_to':'leader-1'}]

# 目标数据
d = [
    {'name':'leader-1', 'team':[{'name':'lili'},{'name':'Tom'}]},
    {'name':'leader-2', 'team':[{'name':'jack'}]}
]

leader_all=[]
# 之后会查询team,所以需要使用{}
teamer_all={}   # {'leader-1':[{'name':'lili'}]}
for index in s:
    if index['belong_to']:
        # 队员
        teamer_all.setdefault(index['belong_to'],[])
        teamer_all[index['belong_to']].append({'name':index['name']})
    else:
        # 队长
        leader_all.append({'name':index['name'],'team':[]})
for i in leader_all:
    if i['name'] in teamer_all.keys():
        i['team']=teamer_all[i['name']]
print('leader_all:'%s,leader_all)
# leader_all: [{'name': 'leader-1', 'team': [{'name': 'lili'}, {'name': 'Tom'}]}, {'name': 'leader-2', 'team': [{'name': 'jack'}]}]


# print('leader_all:'%s,leader_all)
# print('teamer_all:'%s,teamer_all)
# leader_all: [{'name': 'leader-1', 'team': []}, {'name': 'leader-2', 'team': []}]
# teamer_all: {'leader-2': [{'name': 'jack'}], 'leader-1': [{'name': 'lili'}, {'name': 'Tom'}]}


