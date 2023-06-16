import json
import csv
import sys

from easy.file import *

#####################################
# 全局配置
LUA_BOOL = 1
LUA_NUM = 2
LUA_STRING = 3
LUA_ARRAY = 4
LUA_MAP = 5
LUA_CSV = 6
LUA_NIL = 7

# 即使配表ID重复，也不重新生成配表
IGNORE_REPEAT_ID = False
# IGNORE_REPEAT_ID = True

LUA_TRUE_VALUE = 'true'
LUA_FALSE_VALUE = 'false'
LUA_NIL_VALUE = 'nil'

#####################################
# 运行时全局变量
g_luaTableMap = {}
g_luaFileTableCache = {}  # {txt: [uuid, src, cnt, replace_cnt]}
g_luaFileTableUUIDMap = {}  # {uuid: txt}
g_UUID = 0
g_makeDeep = 0
g_luaTypeString = ["", "LUA_BOOL", "LUA_NUM", "LUA_STRING", "LUA_ARRAY", "LUA_MAP", "LUA_CSV", "LUA_NIL"]
g_space = 0
g_spaceIndent = 4
g_spaceStr = ' '*g_spaceIndent
g_notes_tag = "__note"

space = 0

#####################################

def dump(data):
    if type(data) != list and type(data) != dict : return data

    def buildStr(typ,k,v = ''):
        if typ == list:
            return "[{0}] = {1}".format(k,v)
        elif typ == dict:
            return "{0} : {1}".format(k,v)
        return k

    def pairs(typ,ret):
        if typ == list:
            return range(len(ret))
        return ret

    def _dump(_data,indent,isValue = False):
        space = indent * g_spaceStr
        typ = type(_data)
        str = ''
        if typ == list or typ == dict:
            if not isValue:
                str += space
            str += ('[' if typ == list else '{')
            for k in pairs(typ,_data):
                str += '\n{0}{1}'.format((indent + 1)*g_spaceStr,buildStr(typ,k,_dump(_data[k],indent + 1, True)))
            str += '\n{0}{1}'.format(space,(']' if typ == list else '}'))
        else:
            return _data
        return str

    return _dump(data,0)

def isMap(s):
    s = strSys2User(s)
    return s[0] == '{' and s[-1] == '}'


def isCsv(s):
    return s.endswith(".csv") or s.endswith(".xls") or s.endswith(".xlsx")


def isNil(s):
    if len(s) == 0:
        return True
def isCompatibility(t, castType):
    # LUA_BOOL = 1
    # LUA_NUM = 2
    # -> ok
    # LUA_STRING = 3
    # -> no
    # LUA_ARRAY = 4
    # LUA_MAP = 5
    # LUA_CSV = 6
    # LUA_NIL = 7
    if t == castType:
        return True
    if t <= LUA_STRING and castType == LUA_STRING:
        return True
    if t == LUA_STRING and castType == LUA_CSV:
        return True
    return False


def isBool(s):
    return s in ('true', 'false', 'True', 'False', 'TRUE', 'FALSE')


def isInt(s):
    try:
        int(s)
        return True
    except Exception as e:
        # print e
        return False


def isFloat(s):
    try:
        float(s)
        return True
    except Exception as e:
        # print e
        return False


def isNumber(s):
    return isInt(s) or isFloat(s)


def isArray(s):
    s = strSys2User(s)
    return s[0] == '<' and s[-1] == '>'


def isString(s):
    if len(s) == 0:
        return False
    # 用户强制设定字符串
    if s[:3] == '"""' and s.count('"') % 2 == 0 and s[-3:] == '"""':
        return True
    if s[:2] == '""' and s.count('"') % 2 == 0 and s[-2:] == '""':
        return True
    if s[0] == "'" and s.count("'") == 2 and s[-1] == "'":
        return True
    # 系统字符串标示，还需要后续检查
    return False


def whatType(s):
    s = s.strip()
    if isNil(s):
        return LUA_NIL
    elif isCsv(s):
        return LUA_CSV
    elif isString(s):
        return LUA_STRING
    elif isBool(s):
        return LUA_BOOL
    elif isNumber(s):
        return LUA_NUM
    elif isMap(s):
        return LUA_MAP
    elif isArray(s):
        return LUA_ARRAY
    return LUA_STRING


def autoMake(s):
    # print 'autoMake',repr(s)
    luaType = whatType(s)
    return makeElem(luaType, s)

def exportStr(s):
    global g_space
    g_space = 0

    # data = dump(autoMake(s))
    # return ','.join(autoMake(s))
    return dump(autoMake(s))

DELIM_MATCH = {'"': '"', "'": "'", '<': '>', '{': '}'}
ESCAP_MATCH = ('"', "'")
RECUR_MATCH = ('<', '{')


def makeString(s):
    s = s.strip()
    # remove system "
    if s[0] == s[-1] == '"':
        s = s[1:-1]
    # system escape "" -> "
    s = s.replace('""', '"')
    if len(s) == 0:
        return "''"
    # remove user " and '
    if s[0] == s[-1] == '"':
        s = s[1:-1]
    elif len(s) > 1 and s[0] == s[-1] == "'":
        s = s[1:-1]
    return '%s' % (s.replace("'", "\\'"))


# def makeCsvVar(fileName, isRel = False):
# 	fileName = fileName.replace('\\', '/')
# 	fileName = os.path.normpath(fileName)
# 	if not isRel:
# 		fileName = os.path.relpath(fileName, SRC_PATH)
# 	dirList, fileName = splitFilePath(fileName)
# 	if fileName.endswith('.xlsx'):
# 		fileName = fileName[:-5]
# 	else:
# 		fileName = fileName[:-4] # delete .csv
#
# 	if len(dirList) == 0:
# 		g_luaTableMap[LUA_MODULE_NAME + "." + fileName] = True
# 		return '', LUA_DIR_FUNC(LUA_MODULE_NAME, fileName), LUA_MODULE_NAME + "." + fileName
#
# 	varPerList = []
# 	dirList.append(fileName)
# 	varName = LUA_MODULE_NAME
# 	luaVarPath = LUA_MODULE_NAME
# 	for i in xrange(0, len(dirList)):
# 		if luaVarPath not in g_luaTableMap:
# 			varPerList.append("%s = {}\r\n" % varName)
# 			if not isRel:
# 				g_luaTableMap[luaVarPath] = True
# 		varName = LUA_DIR_FUNC(varName, dirList[i])
# 		# varName = varName + "['%s']" % dirList[i]
# 		luaVarPath = luaVarPath + '.' + dirList[i]
# 	return "".join(varPerList), varName, LUA_CSV_FUNC([LUA_MODULE_NAME] + dirList)



def strSys2User(s):
    s = s.strip()
    # remove system "
    if s[0] == s[-1] == '"':
        s = s[1:-1]
    # system escape "" -> "
    return s.replace('""', '"')


def splitToArrayByDelim(s):
    s = strSys2User(s)[1:-1]
    delim, part, array = [], '', []
    for i in s:
        part += i
        # print i, delim, part
        if len(delim) > 0:
            if i == delim[-1]:
                del delim[-1]
            elif delim[-1] in ESCAP_MATCH:
                # 字符串中会有<和{的可能，配置了公式应当做字符串处理
                pass
            elif i in RECUR_MATCH:
                delim.append(DELIM_MATCH[i])
        elif i in DELIM_MATCH:
            delim.append(DELIM_MATCH[i])
        elif i == ';':
            array.append(part[:-1])
            part = ''
    if len(part) > 0:
        array.append(part)
    return array


def strUser2Sys(s):
    s = s.replace('"', '""')
    return '"%s"' % s


def autoUser2Sys(s):
    if len(s) > 1 and s[0] == s[-1] == "'":
        return strUser2Sys(s)
    elif len(s) > 0 and s[0] == s[-1] == '"':
        return strUser2Sys(s)
    return s


def uuidname():
    global g_UUID
    g_UUID += 1
    return '__predefine_t__[%d]' % g_UUID


def makeArray(s):
    # print 'makeArray', s
    global g_space
    g_space = g_space + 1
    array = splitToArrayByDelim(s)
    array = [autoMake(autoUser2Sys(x)) for x in array]
    # array中间为空的需要保留nil
    array = [LUA_NIL_VALUE if x is None else x for x in array]
    return array

def makeMap(s):
    # print 'makeMap', s
    global g_space
    g_space = g_space + 1

    array = splitToArrayByDelim(s)
    mapp = {}
    cnt = 0
    for i in array:
        if len(i.strip()) == 0:
            continue
        pos = i.find('=')
        if pos == -1:
            raise Exception('map k-v must be split by "="!')
        k, v = i[:pos], i[pos + 1:]
        kType = whatType(k)
        if (kType != LUA_NUM) and (kType != LUA_STRING):
            raise Exception('key must be integer or string!')
        if len(v.strip()) == 0:
            raise Exception('value was empty!')
        k, v = autoMake(autoUser2Sys(k)), autoMake(autoUser2Sys(v))
        if v is None:
            continue
        if k in mapp:
            raise Exception('map key %s deuplicated!' % k)
        mapp[k] = v
        cnt += 1

    # if 0 == len(mapp):
    # 	return None

    if cnt != len(mapp):
        raise Exception('map key deuplicated!')

    return mapp


def showTypeString(luaType):
    return '%d(%s)' % (luaType, g_luaTypeString[luaType])


def makeElem(luaType, strValue):
    strValue = strValue.strip()
    # print 'makeElem', luaType, strValue
    ret = None
    if luaType == LUA_NIL:
        return None
    elif luaType == LUA_BOOL:
        if strValue in ('true', 'True', 'TRUE'):
            ret = LUA_TRUE_VALUE
        else:
            ret = LUA_FALSE_VALUE
    elif luaType == LUA_NUM:
        ret = int(strValue)
    elif luaType == LUA_STRING:
        ret = makeString(strValue)
    elif luaType == LUA_ARRAY:
        ret = makeArray(strValue)
    elif luaType == LUA_MAP:
        ret = makeMap(strValue)
    else:
        raise Exception('luaType %s is invalid!' % showTypeString(luaType))

    return ret

def exportLua(s):
    s = autoMake(s)

    def buildStr(typ,k,v = ''):
        if typ == list:
            return "[{0}]={1}".format(k+1,v)
        elif typ == dict:
            return "[{0}]={1}".format(buildStr(type(k), k), v)
        elif typ == str and k != "''":
            return "'%s'" % k
        return k

    if type(s) != list and type(s) != dict : return buildStr(type(s), s)

    def pairs(typ,ret):
        if typ == list:
            return range(len(ret))
        return ret

    def _dump(_data, indent,isValue = False):
        space = indent * g_spaceStr
        typ = type(_data)
        fms = ''
        if typ == list or typ == dict:
            if not isValue:
                fms += space
            # str += ('[' if typ == list else '{')
            fms += '{'
            index = 0
            orderkey = ''
            for k in pairs(typ,_data):
                if index > 0:
                    fms = fms + ","
                fms += '{0}'.format(buildStr(typ,k,_dump(_data[k],indent + 1, True)))
                if typ == dict:
                    orderkey = '{0},{1}'.format(orderkey, buildStr(type(k), k))
                index = index + 1
            if typ == dict:
                if len(orderkey) == 0:
                    fms += '__order={}}'
                else:
                    fms += ',__order={%s}}' % orderkey[1:]
            else:
                fms += '}'
            # fms += '{0}'.format('}')
        else:
            return buildStr(type(_data), _data)
        return fms

    return _dump(s, 0)

def write_line_str(fo, str2):
    global space
    fo.writelines("\n"+ "\t"*space + str2)

def write_table_str(fo, str2):
    write_line_str(fo, str2)
    global space
    space = space + 1

def write_table_over_str(fo, str2):
    global space
    space = space - 1
    write_line_str(fo, str2)


if __name__ == '__main__':
    input_path = sys.argv[1]
    out_path = sys.argv[2]

    record_colmun_index = 0

    print("input_path", input_path)
    print("out_path", out_path)

    default_arg = []
    default_val = []
    csv_list = []

    delFile(out_path)

    for file in getFiles(input_path, '.csv'):
        with open(file["path"], 'r', encoding='utf-8') as f:
            # print(out_path + file["name"])
            file_lua = open(out_path + file["name"] + ".lua", "w", encoding='utf-8')

            f_csv = csv.reader(f)
            record_row_index = 3
            space = 0

            lua_table = "csv." + file["name"]
            csv_list.append(file["name"])
            write_line_str(file_lua, "-- %s" % (lua_table))
            write_table_str(file_lua, "%s = {" % (lua_table))
            keys = ""

            for row in f_csv:
                if record_row_index <= 0 and row[0] != '':
                    pass
                    for i in range(len(row)):
                        if i == 0:
                            # csv_head = "[%s]" % (row[0])
                            write_table_str(file_lua, "[%s] = {" % (row[0]))
                        elif default_arg[i] != g_notes_tag:
                            val = row[i]
                            if val == '':
                                val = default_val[i]
                            write_line_str(file_lua, ("%s = %s,") % (default_arg[i], exportLua(val)))
                            if i == (len(row)-1):
                                write_table_over_str(file_lua, "},")
                else:
                    if record_row_index == 3:
                        default_arg = {}
                        for k in range(len(row)):
                            if k == 0 or "_" in row[k]:
                                default_arg[k] = g_notes_tag
                            else:
                                default_arg[k] = row[k]
                        print("default_arg", default_arg)
                    elif record_row_index == 2:
                        default_val = {}
                        for k in range(len(row)):
                            if default_arg[k] != g_notes_tag:
                                default_val[k] = row[k]
                        print("default_val", default_val)
                    record_row_index = record_row_index - 1

            s = ""
            write_table_str(file_lua, "__default = {")
            write_table_str(file_lua, "__index = {")
            for k in range(1, len(default_arg)):
                if default_arg[k] != g_notes_tag:
                    v = default_val[k]
                    key = default_arg[k]
                    if s == "":
                        s = "'%s'" % key
                    else:
                        s = s + ",'%s'" % key
                    write_line_str(file_lua, "%s = %s," % (key, exportLua(v)))
            write_line_str(file_lua, "__order = {%s}" % (s))
            write_table_over_str(file_lua, "}")
            write_table_over_str(file_lua, "}")
            write_table_over_str(file_lua, "}")
            # write_line_str(file_lua, "return csv.test")
            file_lua.close()
                # write_line_str(file_lua, "%s.__order = {%s}" % (lua_table, keys))
                # write_line_str(file_lua, "_setDefalutMeta(%s)" % (lua_table))

    file_lua = open(out_path + "csv.lua", "w", encoding='utf-8')
    write_line_str(file_lua, "globals.csv = {}\n")
    for v in csv_list:
        write_line_str(file_lua, 'require "config.%s"' % (v))
    file_lua.close()



