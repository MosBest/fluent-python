python对字典的实现做了高度优化，　而删列表则是字典类型性能出众的根本原因．
集合set的实现其实也依赖与删列表．

# 字典 dict
只有可删列的数据类型才能够作为dict的键．
如果一个对象是可删列的，那么在这个对象的生命周期中，它的删列表是不变的，而且这个对象需要实现__hash__方法．另外可删列对象还要有__eq__()方法，这样才能跟其他键做比较．如果两个可删列对象是相等的，那么它们的删列值一定是一样的．

||可散列类型|
|-----|-----|
||原子不可变数据类型(str,  bytes,  数值类型)|
||frozenset|
||当元组包含的所有元素都是可散列类型的情况下，它才是可散列的|
||用户自定义类型的对象(删列值就是他们的id() 函数的返回值)|
 
如果一个对象实现了\_\_eq\_\_方法，并且在方法中用到了这个对象的内部状态的话，那么只有当所有这些内部状态都是不可变的状态下，这个对象才是可删列的．

## zip函数	
```python
>>> a = zip([1,1,1],  ['a','b','d'])
>>> list(a)
[(1, 'a'), (1, 'b'), (1, 'd')]
```
## 字典推导
字典推导可以从任何以键值对　作为元素的可迭代对象中构建出字典．
```python
a = { b:c  for b, c in xxx}
b = { a: c for s,d in xxx.items()  if s < 66}
```

## 字典方法：setdefault　处理不存在的键
默认情况下，字典d[k]没有找到键k的话，python会抛出异常．
解决方法：
方法1. 	使用d.get(k, default)代替d[k]

如果在字典d中找不到键k, 则返回默认的返回值default.
缺点：
	此方法用于获得值还行，但是如果要更新某个键对应的值时，　就显得非常的低效．基本步骤为：
```python
index = {}
a = index.get('word', [])
a.append('s')
index['word'] = a
```

方法2.	使用d.setdefault(k, default) 解决
如果在字典d中找不到键k, 则返回默认的返回值default.
好处是，解决了d.get　低效的问题．
```python
index = {}
index.setdefault('word', []).append('s')
```
```python
# 以上代码相当于
if 'word' not in index:
	index['word'] = []
index['word'].append('s')
```

## d[k], d.get(k,  default),  d.setdefault(k, default) 三种区别
总结　　d[k], 　d.get(k,  default),  　d.setdefault(k, default) 三种区别：
（d 为　字典　dict）

**dict[key]**
```python
>>> d = {}
>>> d['1']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: '1'
>>> d['1'] = 1
>>> d['1']
1

```
在Python中。我们一般对于字典取值会有dict[key]的方法取值，但是如果键key不存在，则会出现报错KeyError.所以 可以使用dict.get(key[,default]) 的方法。




**dict.get(key[,default])** 会查询字典中的key键，要是存在key键，则返回key键的值，要是没有key键，则返回 default， 若是没有 default，则返回 None。

**dict.setdefault(key[,default])** 实现的功能　和　**dict.get(key[,default])**　是一样的．也是在没有key键，则返回 default， 若是没有 default，则返回 None。
二者不同的地方在于　
	调用　**d.get(key[,default])**　并不会对原字典d 做任何改变．
	而调用  **d.setdefault(key[,default])**  不管有没有default,  键key已经在字典d中生成出来了．
```python
>>> a
{}

>>> a.get("s", [2]) + [1]
[2, 1]  #结果表明　a.get("s", [2])的返回值是列表[2]
>>> a.get("s", [1]).append(2)
>>> a
{} #结果表明　a 并没有发生任何改变

# d.get()仅仅适用于获取值，而不适用于更新字典d．
# 所以要想使用d.get()　更新字典d, 只能做出以下操作:
index = {}
a = index.get('word', [])
a.append('s')
index['word'] = a
# 可以发现十分的低效
```

```python
# 然而　d.setdefault就非常适合　更新字典d
>>> s = {}
>>> s.setdefault('q', [])
[]
>>> s
{'q': []}  # 发现字典已经更新
>>> s.setdefault('w')
>>> s
{'q': [], 'w': None} #哪怕没有设置default值，也会更新字典，key对应的value为None

```
	
# collections.defaultdict 的使用
 
 **collections.defaultdict** 实现的功能　和 **d.setdefault(key[,default])** 一模一样．
 二者的区别：　明显区别还不知道，现在只是认为　
 ** collections.defaultdict** 在使用过程中，比**d.setdefault(key[,default])**更加优雅．
 
##   d.setdefault(key[,default])的使用方法  

```python
index = {}
index.setdefault('s', []).append(location)
index.setdefault('f', []).append(location)
```
 
 index.setdefault(key, aa)要输入两个参数：
 key是要寻找的键，如果字典index内已经包含了键key, 那么直接返回key,　否则放回aa.
** 注意** : aa是返回值，而不是调用值．也就是说，如果aa是一个函数，
那么 
	index.setdefault(key, aa)　相当于 index[key] =  aa , 
	index.setdefault(key, aa())　相当于 index[key] =  aa()
```python
>>> index = {}
>>> index.setdefault(5, [1])
[1]
>>> def aa():
...     return 11
>>> index.setdefault(1, aa)
<function aa at 0x7fd66bddabf8>
>>> aa()
11
>>> index.setdefault(1, aa())
<function aa at 0x7fd66bddabf8> # 因为index[1]前面已经生成出来了
>>> index.setdefault(2, aa())
11

```
##    collections.defaultdict的使用方法  
```python
import collections
index = collextions.defaultdict(aa)
index['s'].append(location)
index['f'].append(location)
```
  collections.defaultdict(aa)必须输入一个可调用的对象（函数），要不然会报错．而且如果输入像[1,2]这样的数值对象，也会报错.


```python
>>> index = collections.defaultdict([1])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: first argument must be callable or None
>>> index = collections.defaultdict([1,2])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: first argument must be callable or None

>>> def aa():
...     return 5
... 
>>> index = collections.defaultdict(aa)
>>> index['s']
5
```  

与d.setdefault(key[,default])比较 ，　collections.defaultdict只需一开始在声明字典时有`index = collextions.defaultdict(aa)`, 那么以后每次调用字典index, 如果键key 不在index, 那么就会调用函数.

##  collections.defaultdict 和　d.setdefault(key[,default])不同之处是
1. 
使用方法不同:
collextions.defaultdict是只需要在字典声明中有　index = collextions.defaultdict(aa), 那么以后每次使用字典index是直接使用的index[key]

	d.setdefault　的字典声明　是 index = {} , 　以后每次都要写为　index.setdefault(key, [1,2])

	所以　collections.defaultdict更优雅．

2.  
collextions.defaultdict(aa) 中　必须是可调用的对象（函数），像[1,2]是会报错的
而　index.setdefault(key, [1,2])是没问题的．

collextions.defaultdict功能的使用使用的是　\_\_missing\_\_
\_\_missing\_\_会在collextions.defaultdict(default_factory)遇到找不到键的时候调用default_factory．

\_\_missing\_\_对所有映射类型都可以支持．

# 特殊方法　__missing__

所有的映射类型在处理找不到的键的时候，都会牵扯到\_\_missing\_\_方法.
哪怕是一个类继承了dict, 然后这个继承类　提供了\_\_missing\_\_　方法, 那么在\_\_getitem\_\_碰到找不到的键的时候，python会自动调用\_\_missing\_\_, 而不是抛出一个keyError异常．

\_\_missing\_\_方法只会被\_\_getitem\_\_调用（比如在表达式d[k]中），而不会对get或者\_\_contains\_\_(in运算符调用的方法)有影响．

# 其它　字典
## collections.OrderedDict
这个类型在添加键的时候会保持顺序，　因此键的迭代次序总是一致的．

## collections.ChainMap
该类型可以容纳　数个不同的映射对象

## collections.Counter
这个映射类型会给键准备一个整数计数器．每次更新一个键的时候都会增加这个计数器．

## collections.UserDict
其实就是把dict用纯python又实现了一遍．
这样做的原因是：
在有的时候，我们想要以　字典　为基类　构建自己的类．
但是，由于dict内部使用c语言写的，也就是有的方法的实现上走了一些捷径，所以构建的类里面就不得不重写这些方法．

但是collections.UserDict解决了这些问题，它是一五一十的用python对dict实现了一遍.

# type.MappingProxyType  不可变的映射类型
标准库中的所有映射类型都是可变的．但是在有的场合，我们不希望用户在错误的场合修改某个映射．
type模块中封装的一个类名为　MappingProxyType 的类．对这个类输入一个映射类型，他会返回这个映射类型的只读的视图．你如果想修改这个视图，那么会报错．但是如果你修改原来的映射，那么这个视图就会跟着修改．
```python

>>> from types import MappingProxyType
>>> d = {1:'1'}
>>> d_proxy = MappingProxyType(d) # 对这个类输入一个映射类型，他会返回这个映射类型的只读的视图．
>>> d_proxy[1]
'1'
>>> d_proxy[1] = '2' # 你如果想修改这个视图，那么会报错．
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'mappingproxy' object does not support item assignment
>>> d[1] = '2'
>>> d_proxy[1] # 但是如果你修改原来的映射，那么这个视图就会跟着修改．
'2'


```

# dict 的实现及其导致的结果
## 1. 键必须是可散列的
因为dict的实现就是对键计算hash值，从而可以直接找到value，而不用遍历．
而要求hash值的前提是　hash函数的输入必须是　可散列的．	

一个可散列的对象必须满足：

	1.  支持hash函数，并且通过\_\_hash\_\_()方法得到的散列值是不变的．
	2.  支持通过\_\_eq\_\_()方法来检测相等性.
	3.  如果a == b, 则 hash(a) == hash(b)　也为真.


可散列类型：　见该篇最开始有．

**如果你实现了一个类的\_\_eq\_\_方法，并且希望它是可散列的，那么它一定要有个恰当的\_\_hash\_\_方法，保证在a==b为真的情况下hash(a) == hahs(b)也必为真．**

## 2. 字典在内存上的开销巨大
**dict的实现是典型的空间换时间.**
散列表必须是稀疏的．不像数组，值是一个挨着一个的．数据在散列表中存储的位置是根据hash值计算的．所以有的时候两个相近的值的散列值可能差别很大（所以python会设法保证大概还有三分之一的表元是空的）．

因为字典使用散列表，而散列表又是稀疏的，这就导致它在空间上的效率底下．

**因此，当你的存储空间有限的时候，而且你需要存储数据巨大的记录，那么放在由元组或是具名元组构成的列表中会是　比较好的选择．
最好不要根据 JSON风格，用由字典组成的列表来存放这些记录．**

## 3. 键查询很快
只要字典能够被装放在内存中，那么**字典可以提供无视数据量大小的快速访问**.

因为键的查询是计算散列值，而不是遍历.

## 4. 键的次序取决于添加顺序
创建两个字典，内容相同，但是添加的顺序不同．
**当两个键的出现的顺序却可能不一样，　但字典的内容不一样时，这两个键是相等的．**
```python
>>> dict1 = {1:1, 2:2, 3:3}
>>> dict2 = {3:3, 2:2, 1:1}
>>> dict1 == dict2
True
>>> dict1.keys()
dict_keys([1, 2, 3])
>>> dict2.keys()
dict_keys([3, 2, 1])

```

## 5. 向字典中添加新键可能会改变原来键的顺序
### 所以，千万不要对字典进行迭代和修改
前面已讲，字典背后的实现原理 是使用hash算法．
hash算法的特点就是，将无限的数据data　映射到　有限的空间上面．那么就一定会存在"散列冲突"的问题．（**见最后面 散列表算法　和 散列冲突　的讲解**）

无论何时往字典里添加新的键，python解释器都可能做出为字典扩容的决定．扩容导致的结果就是要新建一个更大的删列表，并把字典里原有的元素重新添加到新表中．这个过程可能会发生新的散列冲突．导致新散列表中键的次序发生变化．

但是字典何时扩容，何时发生散列冲突　都依赖与字典背后的具体实现，我们是不能够确定的．

所以，** 千万不要对字典进行迭代和修改**，**如果你在迭代一个字典的所有键的过程中同时对字典进行修改，那么这个循环很有可能会跳过一些键－－甚至是跳过那些字典中已经有的键**．


 ** 因此，如果想扫描并修改一个字典，最好分为两步来进行：
 1. 首先对字典迭代，以得出需要添加的内容，把这些内容放在一个新字典里
 2. 迭代结束后再对原有字典进行更新．
 **
 

# 字典的 .keys(), items() 和 .values() 的非常特别的特性
**字典视图**
在python3 中，.keys() , .items() 和 .values() 方法返回的都是**字典视图**.
视图具有动态特性，它们可以实时的反馈字典的变化（就像c语言中的字典一样）.
也就是说，在对原字典的内容进行修改时，视图也会跟着一起改变.
```python
>>> dict1 = {1:1, 2:2, 3:3}

>>> dict1.keys()
dict_keys([1, 2, 3])

>>> a = dict1.keys()
>>> a
dict_keys([1, 2, 3])
>>> dict1[7] = 7
>>> a		# 你会发现，在对原字典的内容进行修改时(这里是增加一个键)，视图a也跟着一起改变
dict_keys([1, 2, 3, 7])
```

# 散列表算法
为了获取dict[key]的value, python首先会调用hash(key)来计算key的散列值，把这个值的最低的几位数字当做偏移量(具体几位，得看当前散列表的大小)，在散列表里面查找表元.
1. 如果找到的表元是空的，则抛出KeyError异常．
2. 如果不是空的，则表元里会有一堆key\_1:found\_value. 这个时候python会检验 key == key_1是否为真，
	
		1. 如果他们相等，就会返回found_value.
		2. 如果不相等，这种情况称为　散列冲突（见下面讲解）．

# 散列冲突
因为散列表所做的　相当于是将无限的数据映射到有限的空间中，而且散列表本身的索引又只依赖于这个hash值的一部分．那么就会出现 dict[key]中key的hash值搜索出的表元key\_1:found\_value，出现key_1 != key.这就是散列冲突

为了解决散列冲突，算法会在散列值中另取几位，然后用特殊的方法处理一下，把新得到的数字再当作索引来寻找表元．
若这次找到的表元是空的，则同样抛出KeyError.
若非空，且键匹配，则返回这个值
若非空，但是键不匹配，则表明又发生了散列冲突，则重复上面的操作．