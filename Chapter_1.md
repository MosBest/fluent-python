__特殊方法__（也叫　魔术方法 magic method）：　就是　\_\_xxx\_\_()方法　。　所以也称为　双下划线方法

python解析器在遇到一些　特殊的句法时，　其背后的原理都是去调用　该句法　背后的特殊方法\_\_xxx\_\_()，完成的。

比如，当python解析器遇到　a[b]这个句法，其背后的原理就是调用\_\_getitem\_\_方法。即为了求a[b], python解析器实际上是调用a.\_\_getitem\_\_(b)



a[b]这个句法，其背后的原理就是调用\_\_getitem\_\_方法。即为了求a[b], python解析器实际上是调用a.\_\_getitem\_\_(b)

len(a) 其背后的原理就是调用\_\_len\_\_方法。即为了求len[a], python解析器实际上是调用 a.\_\_len\_\_()

for i in x: 背后器实用的是 iter(x)，　而这个函数的背后则是x.\_\_iter\_\_()



__如果你自己写了一个了类，那么你可以根据自己的需求　重写　python的这些句法。__

比如：

```python
class A:
    def __init__(self, l):
        self._list = l
        self._l = l + l
        
    def __len__(self):
        return 5
    
    def __getitem__(self, pos):
        return self._list[pos]

a = A([1,3,5,7,9,11,13])
print("len(a)", len(a))
print("a[2]", a[5])
```

结果是

```python
len(a) 5
a[2] 11
```

一般地，如下所示，如果不重写　特殊方法\_\_xxx\_\_()可能会报错。

```python
class A:
    def __init__(self, l):
        self._list = l
        self._l = l + l

a = A([1,3,5,7,9,11,13])
print("len(a)", len(a))
print("a[2]", a[5])

```

结果是

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-7-4392bd3b8b6c> in <module>()
      5 
      6 a = A([1,3,5,7,9,11,13])
----> 7 print("len(a)", len(a))
      8 print("a[2]", a[5])

TypeError: object of type 'A' has no len()
```

__\_\_getitem\_\___方法的特点：
    １．重写 [] 操作，　即以后自己写的类，如果想要实现　[] 操作，只需在该类中　根据自己的功能需求　编写__getitem__函数即可。
    ２．如果类中包含__getitem__, 那么这个类自动支持　切片（slicing）操作。
    ３．如果类中包含__getitem__, 那么这个类自动　变成　可迭代。（所谓迭代，可以理解为　支持for i in a:）
    4. 如果类中包含__getitem__, 那么这个类自动　变成　可反向迭代reversed(a)。


如果某个类　同时实现了　__\_\_getitem\_\___方法　和　__\_\_len__\_\_方法　这两个特殊方法:

    那么这个类就跟一个python自有的序列数据类型（比如 列表 list）一样了，可以体现出python的核心语言特性(比如list列表的一些特性，迭代，切片等等)。同时这个类还可以用于标准库中诸如　random.choise, reversed, sotred这些函数。__也就是如同列表list一样了__。

首先明确一点，　特殊方法的存在是为了被python解释器调用的，并不需要自己去调用它。

也就是说　应该使用a[b], len(a),　而不要写出a.\_\_getitem\_\_(b) , a.\_\_len\_\_()。

在执行len(a)时
       
       如果a是一个自定义类的对象，那么python会自己去调用　自己实现的 __len__方法。
       如果a是python内置的类型，比如列表(list),字符串(str)，字节序列(bytearray)等，那么Cpython会抄近路，__len__实际上会直接返回PyVarObject里的ob_size属性。PyVarObject是表示内存中长度可变的内置对象的c语言结构体。直接读取这个值比调用一个方法要快得多。
尽可能的使用　内置的函数（例如　len,　iter, str等等），哪怕自己写特殊方法\_\_xxx\_\_()，　方法里面也尽可能使用内置函数。

不要想当然随意添加特殊方法，　比如\_\_foo\_\_之类的，因为这个名字现在没被python内部使用，以后就不一定了。



## 用特殊方法　重写　数值运算符

```
  __add__ +, __sub__ - , __mul__ * 等等　见fluent python 第11页　表1-2
```

##  字符串表示形式

```
repr(): 把一个对象用字符串的形式表达出来以便辨认。repr()通过特殊方法 \_\_repr\_\_()得到。
 
 \_\_str\_\_ : 当你使用str()时，或者用print()是调用。

 如果一个对象没有\_\_str\_\_函数，而python又需要调用它的时候，解释器会用\_\_repr\_\_作为替代。
```

## 自定义的布尔值

bool() 该函数只能返回True 或者　False.

bool(x)的背后是调用x.\_\_bool\_\_()的结果。　如果不存在\_\_bool\_\_方法，　那么bool(x)会尝试调用x.\_\_Len\_\_()。若返回0, 则bool会返回False, 否则返回True。

若果存在\_\_bool\_\_(), 我们对\_\_bool\_\_的实现很简单，如果一个向量的模是0,那么就返回False, 其他情况则返回True.

如果x是内置类型的实例，那么len(x)会非常快。因为CPython 会直接从一个C结构体里读取对象的长度, 完全不会调用任何方法。



decimal:
    
     python 函数库　
     
     固定小数点和浮点运算


​    
Decimal类型是在浮点类型的基础上设计的，但是它在几个地方上要优于floating point：

        1）Decimal类型可以非常精确地在计算机中存储，而学过c++的都知道，浮点型在计算机中是无法精确存储的，比如1.1和2.2在计算机中存储后，运算（1.1+2.2）表达式的值结果会是3.3000000000000003；Decimal类型则不会出现这种情况。同样，由于无法精确存储，浮点型也就无法精确计算（相对于Decimal类型），可以再测试（0.1+0.1+0.1-0.3）两种类型的计算结果。
        2）Decimal类型会自动保留小数点后面不需要的0，以与输入的精度相匹配，比如下面小程序中的例子：浮点型的1.20+1.30结果是2.5；而Decimal类型结果是2.50，这样貌似比较人性化。
        3）Decimal类型可以根据需要自己设置小数点后精度。通过getcontext().prec = x （x为你想要的精度来设置，getcontext()函数下面再详细介绍）。
        4）Decimal类型有很强的管理功能，它能够根据需要设置，来控制输出的格式，得到或者忽略某类错误（如除0，可以设置忽略它，而得到一个Infinity的Decimal值）
fractions:
    
    python 函数库
    
    fractions模块提供了分数类型的支持。


```python
print( list('JQKA') )
print( list('123') )
结果: 
['J', 'Q', 'K', 'A']
['1', '2', '3']
```

in 运算符：

    一般情况下，迭代是非常常见的，但是又是在不知不觉中就完成了。
    
    比如如果一个集合类型没有实现__contains__方法，那么in运算符就会按顺序做一次迭代搜索。（in运算符操控的对象必须是可迭代的）
python collections模块：

    我们都知道，Python拥有一些内置的数据类型，比如str, int, list, tuple, dict等， collections模块在这些内置数据类型的基础上，提供了几个额外的数据类型：
    
    namedtuple(): 生成可以使用名字来访问元素内容的tuple子类
    deque: 双端队列，可以快速的从另外一侧追加和推出对象
    Counter: 计数器，主要用来计数
    OrderedDict: 有序字典
    defaultdict: 带有默认值的字典
```python
import collections
card = collections.namedtuple('card', ['rank', 'suit'])
a = card('aaa','bbb')
print(a.rank)
print(a.suit)
print(a)

结果是：
aaa
bbb
card(rank='aaa', suit='bbb')
```

