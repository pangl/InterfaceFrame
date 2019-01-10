#encoding=utf-8
import hashlib

def md5_encrypt(text):
    '''md5加密'''
    md5 = hashlib.md5()
    md5.update(text)    #转码
    return md5.hexdigest()  #返回加密后的值

if __name__ == "__main__":
    print md5_encrypt("test123")