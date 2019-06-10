python对字典的实现做了高度优化，　而删列表则是字典类型性能出众的根本原因．
集合set的实现其实也依赖与删列表．

# 字典 dict
只有可删列的数据类型才能够作为dict的键．
如果一个对象是可删列的，那么在这个对象的生命周期中，它的删列表是不变的，而且这个对象需要实现__hash__方法．另外可删列对象还要有__eq__()方法，这样才能跟其他键做比较．如果两个可删列对象是相等的，那么它们的删列值一定是一样的．

||可删列类型|
|-----|-----|
||原子不可变数据类型(str,  bytes,  数值类型)|
||frozenset|
||当元组包含的所有元素都是可删列类型的情况下，它才是可删列的|
||用户自定义类型的对象(删列值就是他们的id() 函数的返回值)|

如果一个对象实现了__eq_-方法，并且在方法中用到了这个对象的内部状态的话，那么只有当所有这些内部状态都是不可变的状态下，这个对象才是可删列的．

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
	
