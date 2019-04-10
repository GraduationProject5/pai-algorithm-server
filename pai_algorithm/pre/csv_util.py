import os
import csv
import uuid
import pandas as pd #数据分析
baseDir = os.path.dirname(os.path.abspath(__name__))
csvDir = os.path.join(baseDir, 'static')

# post_file为通过django接收的csv文件
def upload(post_file):
    uuid_str = uuid.uuid4().hex
    tmp_file_name = 'tmpfile_%s.csv' % uuid_str
    filename = os.path.join(csvDir, tmp_file_name)
    fobj = open(filename, 'wb')
    for chrunk in post_file.chunks():
        fobj.write(chrunk)
    fobj.close()
    return filename

# file为pandas dataframe格式数据
def save(file):
    uuid_str = uuid.uuid4().hex
    tmp_file_name = 'tmpfile_%s.csv' % uuid_str
    filename = os.path.join(csvDir, tmp_file_name)
    pd.DataFrame.to_csv(file,filename,',',index=False)
    return filename

# 返回csv文件时用于写入文件流的函数
def file_iterator(file_name, chunk_size=5120):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

