
import json

    
program_path = '/Users/bytedance/codes/jlu-2119-compiler-design/outputs/cache/2022-03-04_16:18:19_TQDLJUWZVI'

# 获取语法树
def getTree(path) :
    tson_file_path = path + '/tson'
    tson_file = open(tson_file_path,encoding='utf-8')
    lines = tson_file.readlines()
    buff = [i for i in range(500)]
    for line in lines:
        level = line.find('{')
        content = line[level:]
        node = json.loads(content)
        node['children'] = []
        buff[level] = node
        if level > 0:
            node['father'] = buff[level-1]
            buff[level-1]['children'].append(node)
    return buff[0]

# 打印语法树
def printTree(level,node):
    children = node['children']
    node['children'] = []
    print(level,node,end='\n')
    for child in children:
        printTree(level+1,child)


tree = getTree(program_path)
printTree(0,tree)