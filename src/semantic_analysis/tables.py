

scope = []

#类型种类定义
type_kind_int       = 'intTy'
type_kind_char      = 'charTy'
type_kind_array     = 'arrayTy'
type_kind_record    = 'recordTy'
type_kind_bool      = 'boolTy'

#符号表
ID_kind_type   = 'typeKind'
ID_kind_var    = 'varKind'
ID_kind_proc   = 'procKind'

#创建标识符表项
def new_id_item(name:str):
    return {
        'name':name,
        'attr':{}
    }

#创建标识符属性
def new_id_attr(type_ptr:int,kind: str):
    return {
        'type_ptr':0,
        'kind':'',
        'level':0,
        'var_attr':{
            'access':'',
            'off'   :0
        },
        'proc_attr':{
            'param':[],
            'code' :'',
            'size' :0
        }
    }

#创建类型项
def new_type():
    return {
        'size':0,
        'kind':'',
        'array_attr':{
            'index_type':'',
            'elem_type':''
        },
        'body':[]
    }

#创建记录域项
def new_field_item(name:str,unit_type:int,offset:int):
    return {
        'name'      :name,
        'unit_type' :unit_type,
        'offset'    :offset
    }

