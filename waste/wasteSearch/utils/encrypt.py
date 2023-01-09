"""
特点
1.定长输出：md5 32位 16进制
2.不可逆：无法方向计算出对应明文
3.雪崩效应：输入密码改变一点，结果完全不同

使用场景
1.密码加密
2.文件完整性检验

使用方案
import hashlib
m = hashlib.md5(salt)     	salt加不加都可以
m.update(b'123')   					传入二进制
value = m.hexdigest()        结果为16进制
value = m.digest              结果为非16进制

"""
import hashlib
from django.conf import settings


def md5(data_string):
    """定长生成32为16进制加密数据"""
    # 加盐


    salt = settings.SECRET_KEY.encode('utf-8')

    # 根据salt生成规则进行加密
    obj = hashlib.md5(salt)
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
