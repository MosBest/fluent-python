# 字符标识 和 字符的具体字节表述
谈谈我的理解：

一个字符串存在的形式大致可以分为两类：一类用于人类可读的文本字符串，另一个用于储存在计算机储存中的 字节序列.

人类可读的文本字符串 就是 Unicode字符， 也叫码位。他是人类可以直接理解的字符串。

字符的字节序列，人读取时可能会认为是乱码，因此字节序列不是给人读取的，而是以一种储存格式储存在计算机中的 。储存的格式不同，那么字符的字节序列就不同。

我们在编辑器中编辑的文本，都是可以理解的，所以这些文本都是 Unicode字符. 
由于硬盘中储存的是字节序列，所以当我们需要保存这些文本到本地硬盘中时，就必须先将Unicode字符编码为某种格式的字节序列，再才能写入硬盘（这个操作，一般软件会帮我们完成，我们只需在"写入函数write"中指定编码方式,encoding = '编码方式'）。

编码方式有很多种，比如UTF-8 , bdg12030。

由于人们希望看到的是可读字符串，所以当我们需要从硬盘中读取文本时，就必须先将硬盘中的字节序列 以它编码时的格式 解码 为 Unicode字符. （这个操作，一般软件会帮我们完成，我们只需在"读取函数read/open"中指定编码方式,decoding = '编码方式'）。解码的格式 应该是这个字节序列 编码时 格式。如果不对应，就会出现乱码。

 
 编码：  encode, 把 码位 转换为 字节序列, 即把字符串 编码为 用于储存或者传输的 字节序列
 解码： deocde， 把 字节序列 转换为 码位 ，即把字节序列 解码为 人类可读的文本字符串
 
 
 字节序列 有各种各样的存储方式。
 Unicode字符 只有一种，用于人类可读。
 
 字节序列： 晦涩难懂的机器磁芯转储
 Unicode字符串：“人类可读”的文本
 
 注意：
 从python3开始,  str对象中获取的元素是Unicode字符.
python2的str对象中获取的是字节序列.不过python2有unicode类型。
所以，python3的str类型基本上相当于python2的unicode类型.

```python
>>> s = 'abc'
>>> s.encode('utf-8')
b'abc'  //引号左边最开始是b , 表明结果是一个二进制序列， 即字节序列
>>> a = s.encode('utf-8')
>>> a.decode('utf-8')
'abc'
```
# python中的字节序列
**字节序列了类型 就是常说的 二进制序列类型**

python内置了两种基本的二进制序列类型：
	1.  从python2.6开始，添加的可变bytearray类型
	2.  python3 引入的不可变bytes类型

1. python2的str对象就是二进制类型，但在python3中，引入了不可变bytes类型, 而将str对象转化为Unicode字符类型.
2. 虽然python2的str类型就是二进制类型， 但是新的二进制序列类型（比如python3的bytes类型, python2.6的bytearray类型）在很多方面与python2的str类型又有很大的不同。
3. python2.6也有bytes类型，但这只是python2的str类型的别名，与pytho3的bytes类型是不同的.

**bytes或bytearray对象的各个元素是介于0~255之间的整数**
```python
>>> c = bytes('cofe', encoding = 'utf-8')
>>> c
b'cofe'  //有个b，表明是二进制序列

>>> c = bytes('大家好', encoding = 'utf-8')
>>> c
b'\xe5\xa4\xa7\xe5\xae\xb6\xe5\xa5\xbd'
```
# str类型，字节序列 与 其他类型序列 在处理 s[0] ,s[:1]的差异
对于str类型:
s[0] 是一个str类型， s[:1]也是一个str类型， 所以有 s[0] == s[:1]
```python
>>> s = "cofe"
>>> s[0]
'c'
>>> s[:1]
'c'
>>> type(s[0])
<class 'str'>
>>> type(s[:1])
<class 'str'>
>>> s[0] == s[:1]
True
```

对于 字节序列 和 其他类型序列 而言：
s[0] 得到的是 元素
s[:1] 得到的是 一个与 s 相同类型的序列
比如当s 是一个列表list时, s = [1,2,3]，那么s[0]得到的是元素 1,  s[:1]得到与s相同类型的序列（这里是list）即[1].

```python
>>> s = [1,2,3]
>>> s[0]
1
>>> s[:1]
[1]
>>> type(s[0])
<class 'int'>
>>> type(s[:1])
<class 'list'>
>>> s[0] == s[:1]
False

```

于此类似，字节序列也是一样。
s[0] 得到的是 元素
s[:1] 得到的是 一个与 s 相同类型的序列（bytes是一个序列）

```python
>>> s = bytes("cofe", encoding = 'utf-8')
>>> s[0]
99
>>> s[:1]
b'c'
>>> s[:2]
b'co'
>>> type(s[0])
<class 'int'>
>>> type(s[:1])
<class 'bytes'>
>>> type(s[:2])
<class 'bytes'>
>>> s[0] == s[:1]
False

```

**总之： 二进制序列的切片始终是同一种编码的二进制序列**
**任何类型的序列的切片始终是同一类型的序列**

# 二进制序列各个字节的值 可能出现的三种形式
**看一个字符序列是不是二进制序列，打印的时候看最开始有没有b,比如b'aa'，就是一个二进制序列，而'aa'可能就是一个Unicode字符了**
1. 对可打印的ASCII范围内的字节，直接使用ASCII字符本身。
比如，前面的字节形式的'c', 'o' .直接显示为 b'c', b'o' . 这里b表明这是二进制字符.
2. 制表符， 换行符， 回车符 和 \ 对应的字节，使用转义序列\t, \n, \r 和 \ \    .
3. 其他字节的值， 使用十六进制转义序列（例如，\x00是空字节）

# memoryview 模块 和 struct 模块
1. struct 模块：**可以从二进制序列中提取结构化的信息**
可以将打包的字节序列按照自己要求转换成不同类型字段组成的元组。同时还可以进行反向转换，把元组转换成打包的字节序列。
struct 模块可以处理bytes, bytearray 和 memoryview对象.

2. memoryview 内存视图对象 允许在二进制数据结构之间共享内存。
你可以字节访问数据的切片，而无需复制字节序列。

# 几种基本的编码格式
上面已经讲过，将Unicode 字符转为 字节序列(即二进制序列) 的过程 叫做 编码。

同一个Unicode 字符(人类可读的) 用不同的编码方式可以产生 不同的二进制序列(可理解为保存到硬盘中的).

python 自带了超过100种编解码格式.

为什么需要这么多编解码格式呢？
想要将Unicode 字符保存到硬盘中，就必须将Unicode 字符转为二进制序列。那么我们就要找到 一种方式 让 每一个不同的Unicode 字符 与一个二进制序列一一对应。
人类有各种语言，那么Unicode 字符(人类可读的) 就非常非常的多，我们很难设计出一种二进制序列 与 地球的所有Unicode 字符 一一对应。即使有，那这种对应关系表也会非常大，计算机查找缓慢，不好存储。
而且在现实生活中，对于说英语的人，就不可能用到 巴西语。 那么说英语的人只使用 只对应英文字母的二进制序列的编码方式就可以了。

所以，我们只是把那个最大的二进制序列的对应表(假设我们有)，拆分成 各个不同的小表，我们只需使用 我们需要的那个小表就可以了。比如 gb2312仅仅处理简体中文字符.

**因此，一般的编码方式都不可能表示所有Unicode字符**
**但是，UTF编码的设计目的就是处理每一个Unicode码位**
## 下面讲解一下常见的编码方式
### ascii
ASCII码
### latin1 (即iso8859_1)
非常重要的编码，是其他编码的基础，比如cp1252 和 Unicode 
### cp1252
Microsoft制作的latin1扩展，即在latin1上面添加了其他有用的符号。Windows中可能会用得到.
### gb2312
用于编码简体中文的标准.
### utf-8
目前Web中最常见的8为编码，与ASCII兼容(纯ASCII文本是有效的utf-8文本)。
### utf-16le
utf-16的16位编码方案的一种形式。包括逐逐渐流行的表情符号。

# 编解码中可能报的错误
**UnicodeError**: 一般性异常
**UnicodeEncodeError**: 把字符串转为二进制序列时
**UnicodeDecodeError**: 把二进制序列转为字符串时
**SyntaxError**: 如果python源码的编码与预期不符，加载python模块可能会抛出

这里所说的字符串就是 Unicode字符.

**出现与Uniode有关的错误时，首先要明确异常的类型。导致编解码问题的是UnicodeEncodeError, 还是UnicodeDecodeError, 还是SyntaxError，解决问题之前必须清楚这一点。**
## UnicodeEncodeError
**错误场合：**把字符串(Unicode字符)转为二进制序列时
**错误原因：**
多数非UTF编码器只能处理Unicode字符的一小部分子集。当把文本转换成字节序列时，编码器 没有这个文本中某个 Unicode字符与字节序列的对应，那就会抛出UnicodeEncodeError异常.
**解决方案：**
方法1： 更换编码格式
方法2：把error参数传给编码方法或函数，对错误进行特殊处理。以下是例子：
```shell
>>> h  = "aaa大bbb家ccc"

>>> h.encode('utf-8')
b'aaa\xe5\xa4\xa7bbb\xe5\xae\xb6ccc'

>>> h.encode('utf-16')
b"\xff\xfea\x00a\x00a\x00'Yb\x00b\x00b\x00\xb6[c\x00c\x00c\x00"

>>> h.encode('gb2312')
b'aaa\xb4\xf3bbb\xbc\xd2ccc'

>>> h.encode('latin1')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'latin-1' codec can't encode character '\u5927' in position 3: ordinal not in range(256)

>>> h.encode('latin1', errors = 'ignore')
b'aaabbbccc'

>>> h.encode('latin1', errors = 'replace')
b'aaa?bbb?ccc'

>>> h.encode('latin1', errors = 'xmlcharrefreplace')
b'aaa&#22823;bbb&#23478;ccc'

```
以上代码讲解：
这里字符串就是 Unicode 字符
**'utf-?'编码能编码任何字符串**
**latin1不能编码中文字符串,所以抛出UnicodeEncodeError**
**errors = 'ignore' 表示跳过无法编码的字符**
**errors = 'replace'表示把无法编码的字符用?替代**
**errors = 'xmlcharrefreplace'把无法编码的字符替换成XML实体**

## UnicodeDecodeError
从硬盘中读取二进制序列文件，然后进行解码，再才能够变为人类可读的字符串(Unicode 字符)。
但是这个解码用的 格式 必须要和 文件写入到硬盘时编码格式一致，不然一般会出现两种情况：
1. 抛出UnicodeDecodeError.
	
	虽然Unicode字符有千千万万个，但是字节序列又可以有千千万万个(比如随机噪声)。所以有的时候 某种解码器 的对应表中并没有 与 这个字节序列 相对于的Unicode字符。即可能某个字节序列也有可能出现无法转换的现象，这时就会抛出UnicodeDecodeError.

2. 可能出现乱码
	
	对于某些陈旧的8位编码------如latin1, cp1252------能够解码任何字节序列流(例如随机噪声)而不抛出错误， 但是得到的却可能是一堆乱码。

```
>>> h  = "aaa大bbb家ccc"

>>> h.encode('utf-8')
b'aaa\xe5\xa4\xa7bbb\xe5\xae\xb6ccc'

>>> a = h.encode('utf-8')

>>> a.decode('latin1')
'aaaå¤§bbbå®¶ccc'

>>> a.decode('ascii')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe5 in position 3: ordinal not in range(128)

>>> a.decode('gb2312')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'gb2312' codec can't decode byte 0xa7 in position 5: illegal multibyte sequence

>>> a.decode('gb2312', errors = 'replace')
'aaa澶�bbb瀹�ccc'
>>> a.decode('ascii', errors = 'replace')
'aaa���bbb���ccc'


>>> a.decode('utf-8')
'aaa大bbb家ccc'

```
## SyntaxError
这里的内容可能不太正确，以后真正弄明白了再来修改，这里就先记录以下当前的理解！！！

对于python3，它是默认你的.py文件是utf-8(python2默认是ASCII), 所以如果你的.py文件不是 utf-8，就会抛出错误SytaxError。

如果你不是用当前优秀的python的GUI(比如：pyCharm)， 而是用window系统自带的文本编辑器，那么就很容易抛出错误SytaxError。

因为 Windows系统自带的文本编辑器使用cp1252编码, 这个时候你的.py文件就是cp1252编码的。那么用python3编译，就会抛出错误SytaxError。

而GNU/Linux, OS X 系统自带的文本编辑器大都是使用UTF-8进行编码的，所以用他们自带的文本编辑器抛出的概率就会低一些。

**怎么解决问题：**
只需要在文件顶部添加一个coding注释即可。
比如你要在window系统自带的文本编辑器中写.py文件，那么只需
```python
# coding: cp1252
print("aaa")
```
# 找出字节序列的编码
如何找出字节序列的编码？
答案是，必须有人告诉你，否则不能知道。

或者你以纯文本的形式 查看字节流，然后通过试探和分析找出编码。（反正我是看不出来）

最后一种方法： 使用侦查包
即 统一字符编码侦测包Chardet (https://pypi.python.org/pypi/chardet), 它能识别所支持的30种编码.
Chardet是一个python库，可以在程序中运行，也提供命令行工具chardetect
