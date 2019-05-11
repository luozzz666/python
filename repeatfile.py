# _*_ coding:utf-8 _*_

import MySQLdb
import os
import hashlib
import time

#数据库信息
host='192.168.230.23'
user='xxx'
passwd='xxx'
db='xxx'
charset='utf8'

#需要处理的路径
path=r'E:\soft'

#连接数据库
conn=MySQLdb.connect(host=host,user=user,passwd=passwd,db=db,charset=charset)
cursor=conn.cursor()
 
#判断是否重复，0为重复，其他为重复次数
def juderepeat(md5):
    countsql="select count(1) from fileinfo where md5='%s';" %md5
    cursor.execute(countsql)
    count=cursor.fetchall()
    return count[0][0]

#获取文件的md5值
def calcmd5(filepath):
    with open(filepath,'rb') as f:
        md=hashlib.md5()
        md.update(f.read())
        filemd5=md.hexdigest()
        return filemd5
#遍历目录    
def walkpath(path):
    for roots,dirs,files in os.walk(path):
        for file in files:
            #print file
            file_format=file.decode('gbk').encode('utf-8')
            filepath=os.path.join(roots,file)

            #文件路径格式转换
            if os.name == 'nt':
                filepath_format=filepath.decode('gbk').encode('utf-8')
                filepath_format='/'.join(filepath_format.split('\\'))
            else:
                filepath_format=filepath.decode('gbk').encode('utf-8')
            
            #文件属性
            filedata=os.stat(filepath)
            size=filedata[6]/1024
            atime=filedata[7]
            mtime=filedata[8]
            ctime=filedata[9]
            
            #md5
            filemd5=calcmd5(filepath)
            status=juderepeat(filemd5)
            #时间
            nowtime=time.strftime('%Y-%m-%d %H:%M:%S')
            
            #插入mysql
            sql="insert into fileinfo (name,localpath,size,md5,status,atime,mtime,ctime,update_time) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s');" %(file_format,filepath_format,size,filemd5,status,atime,mtime,ctime,nowtime)
            cursor.execute(sql)
            conn.commit()
    
            #输出
            if status != 0:
                print filepath_format

    conn.close()

walkpath(path)

#数据库建表sql
############################################################################################
'''
CREATE TABLE fileinfo (
  id int(11) NOT NULL AUTO_INCREMENT COMMENT '文件信息id',
  name varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件名称',
  localpath varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件路径',
  size int(11) DEFAULT NULL COMMENT '文件大小',
  md5 varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件md5值',
  status int(3) DEFAULT NULL COMMENT '文件状态 0：文件不重复 ，1：文件重复',
  atime int(11) DEFAULT NULL COMMENT '最近一次访问文件的时间',
  mtime int(11) DEFAULT NULL COMMENT '最近一次文件内容被修改的时间',
  ctime int(11) DEFAULT NULL COMMENT '最近一次文件状态改变的时间',
  update_time datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
'''
############################################################################################

