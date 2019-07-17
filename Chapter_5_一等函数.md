[TOC]



# 一等函数



**一等对象** 定义：

* 在运行中创建
* 能赋值给变量或者能赋值给数据结构中的元素
* 能作为参数传给函数
* 能作为函数的返回结果

**当函数也是一等对象，则称该函数为 一等函数**

**在python中，所有函数是一等对象。即python的所有函数都是一等函数。 **

比如以下实例:

```python
# 在运行中创建 ————> python可以在命令行中 编辑，运行
>>> def f(x):
    return x
# 能赋值给变量或者能赋值给数据结构中的元素
>>> a = f
>>> a(5)

# 能作为参数传给函数
>>> sortd(data, key = f)
>>> list(map(f, range(11)))

# 能作为函数的返回结果 ————>比如 装饰器，闭包
```



```python
# 声明 函数f()
def f():
    """
    这是函数的帮助文档
    """
    return 1

print(f.__doc__) ## 输出函数开头""" """ 里面的内容
print(type(f))
```



函数 f 是 function 类的实例。(python 竟然还有一个叫做function的类)



**\_\_doc\_\_** 属性用于打印对象的帮助文档，输出函数开头""" """ 里面的内容。



#  高阶函数

接收函数为参数，或者把函数作为结果返回的函数是**高阶函数** 。

在函数式编程范式中，最为人熟知的高阶函数有map, filter, reduce 和 apply。

其中, apply在python 3 中已被移除。如果想使用不定量的参数来调用函数，可以编写形如 f(*args, **keywords)这样形式的函数，而不需要使用apply。

map, filter, reduce 这三个高阶函数虽然还能见到，但是多数场合 我们有更好的替代品。



##  map, filter 的替代品 --------> 列表推导 或者 生成器表达式

在python 3 中，map, filter 依然函数内置函数

在python 3中，map, filter 返回生成器(一种迭代器), 因此现在他们的直接替代品是 生成器表达式。

在python 2中，map, filter 返回列表，因此最接近的替代品是列表推导。

```python
>>> list(map(fact, range(6))) 相当于 [fact(n) for n in range(6)]
>>> list(map(factorial, filter(lambda n:n % 2, range(6)))) 相当于 [factorial(n) for n in range(6) if n % 2]
```



##  reduce 的替代品---------> sum函数

在python 2中reduce 是内置函数

在python 3中放在了functools模块里了

这个函数最常用于求和，自python 2.3开始，最好使用内置的sum函数。

sum和reduce的通用思想是把某个操作连续应用到序列的元素上，累计之前的结果，把一系列值归约成一个值。

```python
>>> from functools import reduce
>>> from operator import add
>>> reduce(add, range(100))

>>> sum(range(100))
```



#  all 和 any 函数

all 函数 和 any 函数都是内置的归约函数。

* all(iterable)

  如果iterable的每个元素都是真值，返回True, 但是 all([])返回 True

* any(iterable)

  只要iterable中有元素是真值，就返回True, any([])返回False.

  

#  匿名函数 lambda

使用**lambda关键字**在**python表达式内** 创建匿名函数。

lambda句法只是语法糖：  与def语句一样，lambda表达式只是创建了函数对象。

```python
>>> lambda x:x[1:] for x in list_data if x!=a
>>> lambda x,y:x+y for x in list_data for f in list_cc
```

python限制 lambda函数的定义体只能使用纯表达式。也就是说，lambda函数的定义体中不能赋值，也不能使用while 和 try等python语句。



#  对象 是否 可调用

* ( )  括号 叫做 调用运算符。
* **如果想要判断对象能否调用，可以使用内置函数 callable()**



## python的7中可调用对象：

* 用户自定义的函数

  即使用def 语句 或者 lambda表达式 创建。

  

* 内置函数

  **python的内置函数 是使用c语言(CPython)实现的函数。**

  

* 内置方法 (内置对象中的函数)

  使用c语言实现的方法。

  

* 方法

  在类定义提中定义的函数

  

* 类

  **调用类的过程：**

  **调用类时会运行类的\_\_new\_\_方法创建一个实例，然后运行\_\_init\_\_方法 ,初始化实例，最后把实例返回给调用方。**

  

* 类的实例

  如果类定义了\_\_call\_\_方法，那么它的实例就可以作为函数调用。

  

* 生成器函数

  使用yield关键字的函数和方法。调用生成器函数返回的是生成器对象。



python 中有各种各样可调用的类型，因此判断对象能否调用，最安全的方法是使用**内置的callable()函数**。



##  如何使 类的实例 也可以是 可调用的

**python对象**：  就是  python某一个 类的实例 。

最开始讲过，python任何一个函数 其实也是function类的实例。

在python中，函数是真正的对象。当然，我们也可以使得任何的python对象 表现得像函数一样（即 如果 a 是一个list的实例 ,a = [1,2,3], 我们也希望 对象a 表现得像 函数一样 a() 使用）。

**方法是：只需在产生这个实例的类中实现实例方法\_\_call\_\_ 。**

这样，用这个类产生的任何实例a，a() 现对于执行了a.\_\_call\_\_()操作。

```python
class Bingo:
    def __init__(self, items):
        self._items = list(items)
    
    def pick(self):
        return self._items.pop()
    
    def __call__(self):
        return self.pick()
    
>>> bon = Bingo(range(3))
>>> bon() #bon是实例,bon() 相当于调用了 bon.__call__()函数
>>>callable(bon)
        
```



