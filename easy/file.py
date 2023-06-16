import os

def getFiles(dir, suffix): # 查找根目录，文件后缀
    res = []
    for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename) # =>文件名,文件后缀
            if suf == suffix:
                res.append({
                    'path' : os.path.join(root, filename),
                    'name' : name
                })
    return res


def delFile(pathData):
    for i in os.listdir(pathData) :# os.listdir(pathData)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        fileData = pathData + "\\" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(fileData) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(fileData)
        else:
            delFile(fileData)

def absPath(path):
    return "{}\\{}".format(os.getcwd(), path)

