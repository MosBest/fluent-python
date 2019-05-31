[toc]
#  python用统一的风格去处理序列数据：
 不管你是哪种数据结构（字符串，列表，XML...），他们都公用一套丰富的操作：迭代，切片，排序，拼接......
 
 
#  容器序列类型 和 扁平序列类型 
 容器序列类型 和 扁平序列类型  都存在于python标准库，且都是用 c实现。
 
 ||容器序列|扁平序列|
|-----|-----|-----|
|优点1|1. 一个 容器序列 能够存放不同类型的数据 |1. 一个扁平序列 只能容纳一种类型|
|优点2|2. 容器序列 存放的是他们所包含的任意类型的对象的引用|2. 扁平序列 里存放的是值 而不是引用。|
|序列包括|list, tuple, collections.deque|str, bytes, bytearray, memoryview, array.array|


# 可变序列类型  和　不可变序列类型
||可变序列类型|不可变序列类型|
|-----|-----|-----|
|特点|序列内的值可以改变|序列内的值不可改变|
|序列包括|list, bytearray, array.array, collections.deque, memoryview|tuple, str, bytes|


#  列表推导  和　生成器表达式
通常情况，列表推导仅仅时用来创建新的列表，并且尽量保持简短。如果列表推导太长，还不如用for循环重写

||列表推导|生成器表达式|
|-----|------|------|
|功能|快捷的构建 列表list|快捷的构建(除列表外)其他任何类型的序列|
|目的|提高可读性高，快捷|提高可读性高，快捷|
|使用方式|使用[], 如[i for i in s if i > 1]|使用(), 如( i for i in s if i > 1)|
|内部实现|执行了[i for i in x]后，解释器会将整个完整的列表都保存在内存中|遵守迭代器协议，执行了(i for i in x) 后，得到的仅仅是一个迭代器，里面的代码其实并没有执行,所以内存也没有数据，只是可以在以后的代码中逐个地拿出 数据， 迭代器的优势就是在于，减少内存的消耗|
	


# 元组tuple

元组的两个特性：　
1. 
	** 作为　不可变的列表list**
	 * 元组其实就是一个列表，只是里面的值　是不能够改变的．
	*  除了跟增减元素相关的方法之外，元组支持列表的其他所有方法
 2.   
 	**对数据的记录（数据 和 数据的位置信息）--> 具名元组 (collections.nametuple)**
        元组与列表第二点的不同：　就是元组不仅仅存储了数据，还存储了该数据的位置信息．
        所以，如果你仅仅将元组看成不可变的列表，那么这些位置信息和元素的总数信息　　也就没什么作用．
        但是，如果你将元组当成一些字段的集合，那么数据和位置信息就变得非常重要了．

一般，这些功能在　python内置函数库　**collections.namedtuple** 中有很好的实现．

**collections.namedtuple**　用来构建一个　类，　这个类的实例有很多有用的方法　供我们使用，而且实例所消耗的内存　跟　元组是一样的．

创建一个具名元组的类需要两个参数：collections.namedtuple(aaa, bbb)
1. aaa　是　类名
2. bbb  是　类的各个字段的名字 : 有两种方法创建：
```python
1. 由数个字符串组成的可迭代对象　collections.namedtuple('Ca', ['rank', 'suit'])

2. 由空格分隔开的字段名组成的字符串　collections.namedtuple('Ca', "rank suit")
```

创建一个具名元组的类的实例：
```python
import collections
C1 = collections.namedtuple('Ca', ['rank', 'suit'])
t = C1(1,2)
print(t)
    # 输出：Ca(rank=1, suit=2)
```

你可以通过字段名或者位置来获取一个字段的信息
```python
print(t.rank)
print(t[1])
```




# 元组(1,2,3) 与 生成器表达式( i for i in range(3)) 的区别：

tuple() 和 生成器表达式(xxx) 是不同的东西。
一个最终得到的是 元组tuple, 一个最终得到的是 生成器 
比如下面操作：
```python
a = tuple([1,2,3])
print(type(a),a)
# 结果是　<class 'tuple'> (1, 2, 3)

a = (i for  i in range(3))
print(type(a),a)
# 结果是　<class 'generator'> <generator object <genexpr> at 0x0000023C1CFFD780>
```




# [] , {}, () 对　换行符号的忽略
在编辑器（如pycharm）中写代码时，为了代码可读性，当一行代码太长时，就需要在下一行 继续写，这个时候就需要使用 续行符"\"。
比如
```python
a = numpy.xxx.xxx(xxx).xxx().xxx.xxx \ 
	xxxxxxxxx
```

但是如果在括号里面换行就不一样了。

python 会忽略代码里[] ,{}, () 中的换行，因此如果你的代码里有多行的列表，列表推导， 生成器表达式， 字典这一类的，就可以省略不太好看的续行符"\"。

比如
```
a = [xxxxxxxxxxxxxxxxxxxxxxxxxxx 
        xxxxxxxx]
```

#  列表推导， 生成器表达式， 集合(set)推导， 字典推导 在 python2.x 和 python3.x 的不同：
(以下以 列表推导为例，但也同时适用于 另外 3个)

在python2.x中，列表推导里面的变量作用域 和 列表推导外面的变量作用域 是公共的。 也就是说，列表推导里面 变量值得改变 是 会影响 列表推导外面的变量的值的。

比如：
```python
# 在python2.x
x = 1

a = [x for x in range(6)]

print(x)
# 结果为5
```

但是在python3 中 列表推导 都有自己的局部作用域。表达式内部的变量和赋值只会在局部起作用，局部变量并不会影响 表达式上下文的同名变量。

比如
```python
# 在python3.x
x = 1

a = [x for x in range(6)]

print(x)
# 结果为1

```

# ord()
ord('a')函数：　将单个字符转会为对应的ASCII码值

