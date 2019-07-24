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



#  函数的内省

就是函数中形如\_\_xxx\_\_的属性。

使用**dir函数** 可以查看 类的实例 和 函数 的内省。

```python
>>> set(dir(实例1)) - set(dir(函数1)) # 查看常规对象没有而函数有的属性
```



#  函数参数问题

* 关键字参数：

关键字参数是Python函数中最基础也最常见的。

```python
# 关键字参数 的 声明
## 这里的a和b都是关键字参数
def ppp(a, b):
    return a

# 关键字参数 的 调用
## 关键字参数支持两种调用方式：1. 位置调用 。  2. 关键字调用
### 位置调用，就是按参数的位置进行调用， 比如
>>> ppp(1, 2) # 结果为1
>>> ppp(2, 1) # 结果为2
### 关键字调用，可以忽略参数顺序，直接指定参数。 比如
>>> ppp(a=1, b=2) # 结果为1
>>> ppp(b=2, a=1) # 结果为1

```

* 参数默认值

在函数声明时，指定参数默认值，调用时不传入参数则使用默认值，相当于可选参数。

```python
# 参数b 默认值的声明
## 在声明时， 默认参数需要设置在必选参数后面，不然会报错
def ppp(a, b=0):
    return b

# 默认参数 的 调用
## 默认参数 也 支持两种调用方式：1. 位置调用 。  2. 关键字调用
## 但是 默认参数在调用时也必须设置在必选参数后面
### 位置调用，就是按参数的位置进行调用， 比如
>>> ppp(1, 2) # 结果为2
>>> ppp(2, 1) # 结果为1
### 关键字调用，可以忽略参数顺序，直接指定参数。 比如
>>> ppp(1, b=2) # 结果为2
>>> ppp(b=2, 1) 这个报错，默认参数必须在必选参数后面
```

* 仅限关键字参数

  在python 3.0开始引入

  我们会发现参数多的时候通过关键字指定参数不仅更加清晰，也更具有可读性。如果我们希望**函数只允许关键字调用**,这个时候就需要 仅限关键字参数。

  

  **定义函数时想指定仅限关键字参数，要把它们放到前面有星号的参数后面**

  

  在Python中有星号的参数是可变参数的意思，如果不想支持可变参数，可以在参数中放一个星号作为分割。

  

  普通参数和仅限关键字参数中间由一个星号隔离开，星号以后的都是仅限关键字参数，**只可以通过关键字指定，而不能通过位置指定**。

  

  同时，仅限关键字参数不一定要有默认值，可以像下面例子中b，一样，强制必须传入实参，而不是指定默认值。

  ```python
  >>> def f(a, *, b):
  ...     return a, b
  ... 
  >>> f(1, b=2)
  (1, 2)
  >>> f(1, 2)
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  TypeError: f() takes 1 positional argument but 2 were given
  
  ```

  ```python
  >>> def f(a, *c, b=2):
  ...     return a,c,b
  ... 
  >>> f(1,b=1)
  (1, (), 1)
  >>> f(1,1,b=1)
  (1, (1,), 1)
  >>> f(1,1,2,3,4,5,b=1)
  (1, (1, 2, 3, 4, 5), 1)
  >>> f(1,1,1)
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  TypeError: f() missing 1 required keyword-only argument: 'b'
  
  ```

  **注意：** 要好好区分 仅限关键字参数 和 参数默认值 二者之间的区别。

  1.  仅限关键字参数 可以不用设定 默认值。 但是 要求 其在函数调动时 必须明确的用 关键字调用(b =2) ,不能够使用位置调用（直接传值），但可以 当成默认参数不调用。
  2.  可以理解为 函数参数声明中,星号之后的 参数名 都是 仅限关键字参数，以后调用必须明确用关键字调用。

  

* 可变长参数

  可变参数有两种

  1. 非关键字可变长参数
  2. 关键字可变长参数

  “可变长”顾名思义是允许在调用时传入多个参数，可变长参数适用于参数数量不确定的场景

1.  非关键字可变长参数

   写法是在参数名前加一个星号，Python会将这些多出来的参数的值放入一个**元组**中，由于元组中只有参数值而没有参数名称，所以是非关键字参数。

   ```python
   >>> def f(*a):
   ...     print(a)
   
   >>> f(1,2,3,4,5,6) # 输出元组 (1,2,3,4,5)
   (1, 2, 3, 4, 5, 6)
   
   >>> b = [1,2,3,4,5]
   >>> f(b) # 直接传入时， 列表a会被当作一个元素，所以输出([1,2,3,4,5],)
   ([1, 2, 3, 4, 5],)
   >>> f(*b) # 在传参时加星号可以将可迭代参数解包，所以列表a中每一个元素都当作一个参数传入，输出(1,2,3,4,5)
   (1, 2, 3, 4, 5)
   
   ```

   

2. 关键字可变长参数

写法是在参数名前加两个星号，Python会将这些多出来的参数的值放入一个**字典**中，由于字典中只有参数值而没有参数名称，所以是关键字参数。

```python
>>> def fff(**k):
...     print(k)

>>> a = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5}
>>> fff(a)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: fff() takes 0 positional arguments but 1 was given
>>> fff(**a)
{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
>>> fff(a=1, b=2, c=3, d=4, e=5)
{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

```



##  函数参数综述

```python
def f(name, age , weight=70, *content, height, tall, hhh= 30, **attrs):
    return 1
# 其中
## name, age , weight=70 都是普通的关键字参数。可以使用关键字调用； 也可以不输入关键字，直接输入数值调用(即位置调用)。
### 只是 weight还是默认参数。所以在调用时，name,age必须要有值，weight可有，也可没有。
### 如果 需要以关键字调用的方式 给weight 传值的话，weight= 必须在 位置调用的后面。

## height, tall, hhh= 30 都是仅限关键字参数。都必须以关键字调用的方式，传值。
### 注意，hhh同时也是默认参数，所以在使用函数时，可以不调用hhh, 但是height=, tall=, 必须都得出现

## *content , **attrs 是可变参数
### *content  是 非关键字可变长参数。 当你给参数 以位置调用的方式传值（也就是直接给值，没有指明参数名）， 如果传入的值的个数大于3， 那么前三个分别给了 name , age, weight, 剩下的都已元组的形式 放在了 变量content里面。

### **attrs 是关键字可变长参数。 当你给函数传参， 如果传入的参数中，有除name, age , weight，height, tall, hhh,之外的关键字，那么这些之外的关键字 都以字典的形式 存储在变量attrs中。
```

```python
# 如果你不想要 *content， 但是又想使用 仅限关键字参数，那么你可以
def f(name, age , weight=70, *, height, tall, hhh= 30, **attrs):
    return 1
```



##  inspect模块 获取函数/类 参数的信息

函数对象有个\_\_defaults\_\_属性，它的值是一个元组，里面保存着 函数参数名称 和默认参数的默认值

仅限关键字参数的默认值在\_\_kwdefaults\_\_属性中，但是参数名称在\_\_code\_\_属性中。



有的时候上面的方法也不好查看参数的信息，最好的方法是使用成熟的**inspect模块**。

(具体见流畅的python 第129, 130, 131页)



inspect模块主要提供了四种用处：

　　1.对是否是模块、框架、函数进行类型检查

　　2.获取源码

　　3.获取类或者函数的参数信息

　　4.解析堆栈



##  函数 参数/返回值 的注释

形如：

```python
def clip(text:str, max_len:'int > 0'=80) -> str:
    return "ok"
```

函数声明中的各个参数可以在：之后增加注解 表达式 。如果参数有默认值，注解放在参数名和=号之间。

如果想注释返回值，在 )  和函数声明末尾的 : 之间添加 -> 和 一个表达式。



以上表达式可以是任何类型。注释中最常用的类型是类(如 str 或 int) 和 字符串 (如 'int > 0')。

python对注释所做的唯一的事情是，把他们存储咋函数的 \_\_annotations\_\_属性里。仅此而已，python不做检查，不做强制，不做验证，什么操作都不做。



# 支持函数式编程的包

得益于operator和 functools 等包的支持，python可以实现函数式编程风格。

##  operator模块

operator模块为很多个**算术运算符**提供了对应的函数。

operator.itemgetter :  创建一个函数，这个函数可以提取对象中的 元素（包括深层的元素）

operator.methodcaller 创建一个函数，对 接收的对象 调用 参数指定的方法。

##  functools模块

functools.partialmethod : 创建一个函数，使用这个函数可以把接受一个或多个参数的函数改编成需要回调的API, 这样参数会更少。

