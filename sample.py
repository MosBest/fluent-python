def ressign(func):
    print("begin_ressign")
    func();
    def inner():  
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
