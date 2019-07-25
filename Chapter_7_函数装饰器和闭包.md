[TOC]



函数装饰器用于在源码中“标记”函数，以某种方式增强函数的行为。



#  装饰器的基本知识

```python
def decorate(func):
    def inner():
        func()
        print('running inner()')
    return inner

@decorate
def target():
    print('running target()')
    
```

以上代码的效果相当于

```python
def decorate(func):
    def inner():
        func()
        print('running inner()')
    return inner

def target():
    print('running target()')
    
target = decorate(target)
```



所以，装饰器 `@decorate`就是一个语法糖。功能就是 接收一个函数，再返回另一个函数(或者可调用对象 )以此来替代原函数。

上面`@docerate` 接收了target()函数，然后在docerate()中经过处理，docerate()返回另一个函数 传给 target。 这样 target()不再是原来的那个函数，docerate()返回的那个函数，即函数 inner() 。



装饰器的两大特性：

1. 能把被装饰的函数替换成其他函数
2.  装饰器在加载模块时立即执行。



#  python 何时执行装饰器

我们知道，平时 的普通函数, 只有在 调用的时候才会执行，在导入模块的时候，编译器仅仅看看对普通函数进行声明，而不会执行函数里面的内容。



但是，对于装饰器就不同了。

```python
@aaa
def f():
    print('q')
```

在导入模块时(即 加载 .py文件时),   python会将上面的 语句执行一遍。即转化为 普通函数相当于

```python
def f():
    print('q')
f = aaa(f)
```

那么，就一定会打印出 'q'的。

再举一个例子。下面是在模块 sample.py的内容

```python
# sample.py
def ressign(func):
    print("begin_ressign")
    def inner():
        func();
        print("run inner")
        print("/n")
    return inner

@ressign
def f1():
    print('f1')

@ressign
def f2():
    print('f2')

if __name__ == '__main__':
    print("begin_main")
    f1()
    f2()

"""
输出结果为：
begin_ressign
f1
begin_ressign
f2
begin_main
run inner
/n
run inner
/n
"""    

```



以上的代码其实可以理解为：

```python
# sample.py
def ressign(func):
    print("begin_ressign")
    def inner():
        func();
        print("run inner")
        print("/n")
    return inner

def f1():
    print('f1')
f1 = ressign(f1)


def f2():
    print('f2')
f2 = ressign(f2)
if __name__ == '__main__':
    print("begin_main")
    f1()
    f2()

"""
输出结果为：
begin_ressign
f1
begin_ressign
f2
begin_main
run inner
/n
run inner
/n
"""    

```



综上所述，装饰器在导入模块时立即执行。

通常情况下，装饰器在一个模块中定义，然后应用到其他模块的函数中。





#  python 变量作用域规则

比较下面两个代码的差异

```python
>>> b = 1
>>> def f1(a):
...     print(a)
...     print(b)
... 
>>> f1(5)
5
1
```

当在

```python
>>> b = 1
>>> def f2(c):
...     print(c)
...     print(b)
...     b = 2
... 
>>> f2(5)
5
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in f2
UnboundLocalError: local variable 'b' referenced before assignment
```

python 不要求声明变量，但是当你**在函数定义体中给某个变量复制**，那么他就设定这个变量是局部变量。对于一个局部变量，在没有值的情况下，使用它(打印它)，是一定会报错的。

```python
>>> b = 1
>>> def f3(c):
...     global b
...     print(c)
...     print(b)
...     b = 2
... 
>>> f3(5)
5
1
```

如果在函数中赋值时，想让解释器把b当成全局变量，要使用**global声明**。这个时候b 就是一个全局变量。

#  闭包 与 自由变量(free variable)

```python
def make_averager():
    series = []
    
    def averager(new_value):
        series.append(new_value)
        return len(series)
    
    return averager
```



![](/home/zhaodao/桌面/github/fluent-python/7.png)

闭包是一个延伸了作用域的函数。 **看是否为闭包，就看它能否访问在函数定义体之外定义的非全局变量**。这个非全局变量并不是 局部变量，而是自由变量(free variable)。

比如上面的例子，make_averager()就是一个闭包。

```python
>>> avg = make_averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
```

观看代码输出，你会发现结果和我们期望的并不相同。avg应该就是　函数averager()，但是它又可以一直使用averager() 函数外面的变量 series。

这个 series 对于　函数　averager()（或者avg函数）, 是一个不在全局作用域的外部变量，即自由变量。虽然　series 又不在averager()的函数定义体内, 但是avg函数依然可以访问series，　这就是自由变量的特点。

在python里面的实现是，python在avg的\_\_code\_\_属性（表示编译后的函数定义体）中保存了局部变量和自由变量。自由变量series的地址在avg函数的\_\_closure\_\_属性。

闭包是一种函数，它会保留定义函数时存在的自由变量的绑定，这样调用函数时，虽然定义作用域不可用，但是仍然使用那些绑定。

注意，只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量。



#  nonlocal声明　：　将变量标记为自由变量

我们依据上面闭包的思路编写下面的代码，发现同样的思路，为何下面的会报错？？？

```python
>>> def make_averager():
...     count = 0
...     total = 0
...     
...     def averager(new_value):
...         count += 1
...         total += new_value
...         return total / count
...     
...     return averager
... 
>>> avg = make_averager()
>>> avg(10)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 6, in averager
UnboundLocalError: local variable 'count' referenced before assignment

```



错误产生的原因：

当count是数字或任何不可变类型时，count += 1 语句的作用其实与　count = count + 1一样。因此，我们在averager的定义体中为count赋值了，这会把count变为局部变量。同理，现在total也是局部变量，而不是自由变量。

在闭包中的例子没有遇到这个问题，是因为我们没有给series赋值，我们只是调用series.append, 并把它传给sun和len, 也就是说，我们在闭包的例子中利用的是列表，而列表是可变的对象。

但是对于　数字，字符串，元组等不可变类型来说，只能读取，不能更新。如果尝试重新绑定，例如　count = count + 1, 其实会隐式创建局部变量count。这样,count就变成了局部变量，而不是自由变量。因此count 不会保存在闭包中。



为了解决这个问题，python3　引入 nonlocal声明。它的作用是把变量标记为自由变量，计算在函数中为变量赋予了新值，也会变为自由变量。

```python
>>> def make_averager():
...     total = 0
...     total = 0
...     count = 0
...     def averager(new_value):
...         nonlocal count, total
...         count += 1
...         total += new_value
...         return total / count
...     return averager
... 
>>> avg = make_averager()
>>> avg(10)
10.0
>>> avg(11)
10.5
>>> avg(12)
11.0
```

​                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

#  实现一个简单的装饰器

在本节笔记开始的地方，已经多多少少讲解了一些关于装饰器的知识。

所以，希望你能够将这里内容和前面装饰器的内容结合的看一看。

创建一个clockdeco.py　文件,编辑以下代码：

```python
# clockdeco.py
# 定义一个　clock　装饰器
def clock(func):
    @functools.wraps(func) # 这一句还是有必要的，在下个知识点讲解
    def clocked(*args, **kwargs):
        """this is the clocked"""
        #do some things
        result = func(*args, **kwargs) # 这里函数func是一个自由变量
        #do other some things
        return result
    return clocked
```

下一步，创建一个clock_demo.py　文件，并编辑以下内容

```python
# clock_demo.py
from clockdeco import clock

@clock
def snooze():
    print("hello")
    time.sleep(5)

if __name__ == "__main__":
    snooze()
```



```python
>>> import clock_demo　# 装饰器在模块导入的时候就会执行，而普通函数则是只能在调用时执行
>>> clock_demo.snooze.__name__
'clocked'
```

你会发现clock_demo.py 里面的　snooze　里面保存的是clocked函数的引用/地址,  而不再是snooze原来函数的功能。



**装饰器的典型行为：　把被装饰的函数替换为新函数，二者接受相同的参数，而且(通常)返回被装饰的函数本该返回的值，同时还会做些额外操作。**



**装饰器模式: 动态的给一个对象/函数 添加一些额外的职责。**



#  python内置函数中常用的装饰器

python内置了三个用于装饰方法的函数：　property,  classmethod  和 staticmethod 。

这三个在以后的章节讲解。



# python标准库中常用的装饰器

##  functools.wraps

在　前面　“实现一个简单的装饰器”　的小节中，我们看到代码中　出现　`＠functools.wraps(func)` ,这是用于干什么的？？？

```python
#对于普通的，不使用装饰器的函数
>>> def snooze():
...     """this is snnoze doc"""
...     print("hello")
... 
>>> snooze.__doc__
'this is snnoze doc'
```

```python

# 如果在snooze上面加上装饰器的话
>>> def clock(func):
...     def clocked(*args, **kwargs):
...         """this is the clocked"""
...         result = func(*args, **kwargs)
...         return result
...     return clocked
... 
>>> @clock
... def snooze():
...     """this is snnoze doc"""
...     print("hello")

>>> print(snooze)
<function clock.<locals>.clocked at 0x7f8202fe6d08>
>>> print(snooze.__name__)
clocked
>>> snooze.__doc__
'this is the clocked'
```



首先，我们不要`＠functools.wraps(func)` 这一句。发现，当snooze被装饰器装饰后，函数snooze()所有属性(比如,\_\_name\_\_,\_\_doc\_\_  等等)将会丢失，取而代之的是　clocked函数的属性。也就是说，snooze()完完全全变成了clocked函数，完完全全丢失了自己所有的东西。

但实际项目中，我们使用装饰器的目的　是　在原有的函数snooze()　上面增加　功能，而不是完完全全丢掉snooze()函数。简而言之，我们在装饰snooze()函数的时候，保留sｎooze()原有的相关的属性。

这个时候就需要　使用`＠functools.wraps(func)` 了。

```python
# 如果在snooze上面加上装饰器的话
>>> import functools
>>> def clock(func):
...     @functools.wraps(func) # 这一句还是有必要的，在下个知识点讲解
...     def clocked(*args, **kwargs):
...         """this is the clocked"""
...         #do some things
...         result = func(*args, **kwargs) # 这里函数func是一个自由变量
...         #do other some things
...         return result
...     return clocked
... 
>>> @clock
... def snooze():
...     """this is the snooze"""
...     print()
... 

>>> print(snooze)
<function snooze at 0x7f757992ed08>

>>> print(snooze.__name__)
snooze
>>> snooze.__doc__
'this is the snooze'
```

使用完`＠functools.wraps(func)`之后，snooze虽然已经变为clocked()函数了，但是　属性(比如\_\_doc\_\_,  \_\_name\_\_)依然是原来的snooze()函数，而没有变为clocked()函数。



##  functools.lru_cache

functools.lru_cache是一个非常非常非常实用的装饰器，它实现了一个优化技术。它能够把耗时的函数的结果保存起来，避免传入相同的参数时重复计算。

这个有点像非递归版本的动态规划。保留函数曾经计算过的值，从而减少运算量。

```python
#实现斐波拉契数列
import functools

@functools.lru_cache()
def f(n):
    if n < 2:
        return n
    return f(n-2) + f(n-1)

if __name__ == '__main__':
    print(f(6))
```

注意：　装饰器`@functools.lru_cache()` 是像常规函数那样调用lru_cache。也就是后面有个括号(), 这么做的原因是，lru_cache 可以接受配置参数。(参数化装饰器见后面讲解)

**特别要注意**, lru_cache可以使用两个可选的参数来配置

```python
functools.lru_cache(maxsize=128, typed=False)
```

maxsize参数指定存储多少个调用的结果。缓存满了之后，旧的结果会被丢掉，腾出空间。

为了得到最佳性能，maxsize应该设为2的幂。

typed参数如果设为True,　把不同参数类型得到的结果	分开保存，即把通常认为相同的浮点数和整数参数(如 1和1.0)区分开。



注意：因为lru_cache使用字典存储结果，而且键根据调用时传入的定位参数和关键字参数创建，所以被lru_cache装饰的函数，**它的所有参数都必须是可散列的**。

##  functools.singledispatch　（功能可理解为函数重载）

因为python不支持重载方法或函数，所以不能够像c++重载(用一个函数名重写多次，仅仅通过输入参数的格式和类型区别) 。

在python中，一种常见的做法是把 函数f 变成一个分派函数，使用一串 if/elif/elif,　在每个判断里面调用专用的函数。这样不便于模块的用户扩展，还显笨拙。时间一长，分派函数f会变得很大，而且它和各个专门函数之间的耦合也很紧密。



**最优的方法: 使用python3.4新增的functools.singledispatch装饰器。**



python3.4新增的functools.singledispatch装饰器可以把整体方案拆分成多个模块。

当你的类是写死的，不能修改的时，可以使用functools.singledispatch来给类增加函数。

`@singledispatch` 装饰的普通函数会变为泛函数： 根据第一个参数的类型，以不同方式执行相同操作的一组函数。



```python
from functools import singledispatch
from collections import abc
import numbers

#基函数 
@singledispatch
def f(obj):
    print("main f")
    return 0

# 以下三个函数　就相当于函数f的三种重载
## 因此，下面三个函数的函数名并不重要(以后使用也是使用函数名f,根据输入参数的类型来判断进入哪个函数)
@f.register(str)
def _(text):
    print("context str")
    return 0

@f.register(numbers.Intergral)
def _(n):
    print("context Intergral")
    return 0

#可以叠加多个register装饰器，让同一个函数支持不同类型
@f.register(tuple)
@f.register(abc.MutableSequence) #可以叠加多个register装饰器，让同一个函数支持不同类型
def _(seq):
    print("context tuple")
    return 0
```

上面三种重载:

只要可能，register()里面尽可能使用抽象基类(numbers.Intergral)不要处理具体实现(int)。这样，代码支持的兼容类型更广泛。

`@singledispatch` 的优点是支持模块化扩展: 各个模块可以为它支持的各个类型注册(f.register)一个专门函数(也可以理解为重载一个专门的函数)。



#  叠放装饰器

即　在一个函数下面叠放多个装饰器。

把@d1 和 @d2 两个装饰器按顺序应用到f函数上，作用相当于 f = d1(d2(f))

即

```python
@d1
@d2
def f():
    print('f')
```

等同于

```python
def f():
    print('f')

f = d1(d2(f))
```



#  参数化装饰器

解析源码中的装饰器时，python把被装饰的函数作为第一个参数传给装饰器函数。那么怎样让装饰器接受其他参数呢？

答案是：创建一个装饰器工厂函数，把参数传给它，它会返回一个装饰器，然后再把它应用到要装饰的函数中。

所谓的装饰器工厂函数，其实就是一个返回装饰器的函数。它是一个函数，对装饰器的封装，可以接受任意参数，在函数内部对参数进行处理，然后返回　根据参数选择的装饰器。

比如 :

```python
def f1_factory(active=True):# f1_factory就是一个装饰器工厂函数
    
    # do some thing 
    
    ###################################
    # 装饰器的实现
    def clock(func):
        def clocked(*args, **kwargs):
            # do some things
            # 比如　if active: xxx else xxx
            result = func(*args, **kwargs)
            # do some things
            return result
        return clocked
    ###################################
    
    # do other things
    
    return clock #返回装饰器
```

f1_factory就是一个装饰器工厂函数, 它内部封装了一个装饰器clock, 可以接收参数，并返回这个装饰器。

所以，使用方法是:

```python
@f1_factory(active=False)
def f2():
    print('running f2')

@f1_factory()
def f3():
    print('running f3')
```

上面的代码等价于:

```python
@clock
def f2():
    print('running f2')

@clock
def f3():
    print('running f3')
```

因为

```python
@f1_factory(active=False) 是由两部分组成: 一个是符号@ , 另一个是 f1_factory(active=False)
而f1_factory(active=False)就是　函数在输入参数active=False执行后的返回值clock (要知道，f1_factory是函数名，括号()是调用对象的运算符，f1_factory()　就是在执行函数)

也就是
@f1_factory(active=False) 是由两部分组成: 一个是符号@ , 另一个是 f1_factory(active=False)
而f1_factory(active=False)　是　clock 
所以@f1_factory(active=False)　就是　@clock
```

所以，参数化的装饰器其实核心思想是对　**函数的调用**。

综上所述，使用参数化的装饰器的方法是:

1. 对装饰器进行封装，得到一个新的函数，这个函数可以接收参数，但返回值必须是　封装的装饰器。

```python
def f1_factory(active=True):
    
    # do some thing 
    
    ###################################
    # 装饰器 clock 的实现
    def clock(func):
        def clocked(*args, **kwargs):
            # do some things
            # 比如　if active: xxx else xxx
            result = func(*args, **kwargs)
            # do some things
            return result
        return clocked
    ###################################
    
    # do other things
    
    return clock #返回装饰器
```

2. 由于 f1_factory(xxx) 的返回值是clock，　所以

```python
@f1_factory(xxx) 　就是　@clock
```



3. 使用

```python
@f1_factory(active=False)
def f2():
    print('running f2')
```





#  locals() 函数

local 函数会以字典类型返回当前位置的全部局部变量。

```python
>>> a = 1
>>> def f():
...     b = 2
...     q = [1, 2]
...     print("locals() = ", locals())
... 
>>> f()
locals() =  {'q': [1, 2], 'b': 2}

```

