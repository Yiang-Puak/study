# ============================================================
# 【零基础也能懂】内存管理与 GIL
# ============================================================

import sys


# ============================================================
# 第一部分：Python 的内存管理
# ============================================================

print("=" * 50)
print("第一部分：Python 的内存管理")
print("=" * 50)

# --- 1.1 变量和对象的关系 ---

print("\n--- 变量不是盒子，是标签 ---")

# Python 中，变量是对对象的"引用"（标签）
a = [1, 2, 3]  # 创建列表对象 [1,2,3]，a 指向它
b = a           # b 也指向同一个对象！不是复制！
b.append(4)     # 通过 b 修改对象
print(f"a = {a}")  # [1, 2, 3, 4] —— a 也变了！

print("""
类比：对象就像一栋房子，变量就像门牌号。
  a = [1,2,3]  => 在 100号 建了一栋房子，挂上门牌 "a"
  b = a        => 给同一栋房子再加一个门牌 "b"
  b.append(4)  => 从 "b" 门进去装修
  从 "a" 门进去看，当然也变样了！
""")

# --- 1.2 引用计数 ---

print("\n--- 引用计数：垃圾回收的基础 ---")

x = "hello"     # "hello" 的引用计数 = 1
y = x           # "hello" 的引用计数 = 2
del x           # "hello" 的引用计数 = 1
y = None        # "hello" 的引用计数 = 0 -> 被回收

print("每个对象都有引用计数，计数归零时自动释放内存")
print(f"空列表的引用计数: {sys.getrefcount([]) - 1}")  # 显示为当前代码中的引用数

# --- 1.3 循环引用问题 ---

print("\n--- 循环引用：引用计数搞不定的情况 ---")

class Node:
    def __init__(self, name):
        self.name = name
        self.next = None
        print(f"Node {name} 创建")

    def __del__(self):
        print(f"Node {self.name} 被销毁")

# 循环引用：A 指向 B，B 指向 A
node_a = Node("A")
node_b = Node("B")
node_a.next = node_b
node_b.next = node_a

# 删除外部引用
print("\n删除外部引用...")
del node_a
del node_b

# 但 A 和 B 的引用计数都是 1（互相引用），不会自动释放！
# 这时需要 "垃圾回收器（GC）" 介入

print("""
循环引用：
  A.next -> B, B.next -> A
  即使外部没有变量指向它们，A 和 B 互相指着对方
  引用计数永远不为 0，导致内存泄漏！

解决：Python 有"分代垃圾回收器（Generational GC）"
  - 定期检查是否存在"孤岛"（只有互相引用的对象群）
  - 发现孤岛后，强制回收
  - gc.collect() 可手动触发
""")

import gc
gc.collect()  # 手动触发垃圾回收


# ============================================================
# 第二部分：GIL 深入理解
# ============================================================

print("\n" + "=" * 50)
print("第二部分：GIL 深入理解")
print("=" * 50)

print("""
Q: 什么是 GIL？
A: GIL = Global Interpreter Lock（全局解释器锁）
   是 CPython 解释器的一把"大锁"，保证同一时刻只有一个线程在执行 Python 字节码

Q: 为什么要有 GIL？
A: 1. 简化内存管理：Python 用引用计数管理内存，多线程同时修改引用计数需要加锁
      GIL 避免了每个对象都加一把小锁的复杂设计
   2. 防止死锁：统一的大锁比无数小锁更容易管理
   3. 历史原因：Python 诞生时单核 CPU 为主，GIL 设计足够简单有效

Q: GIL 的影响？
A: - 多线程对 CPU 密集型任务无效（甚至因为切换开销更慢）
   - 多线程对 I/O 密集型任务有效（等待 I/O 时释放 GIL，其他线程可以运行）

Q: 怎么绕过 GIL？
A: 1. multiprocessing：多进程，每个进程独立 GIL
   2. C 扩展：C 代码在执行时可释放 GIL
   3. asyncio：单线程协程，避免线程切换开销
   4. 换解释器：Jython、IronPython 没有 GIL（但有其他问题）
""")

# --- 验证：多线程对 CPU 密集任务无效 ---

import threading


def cpu_task(n):
    """纯计算任务"""
    count = 0
    for i in range(n):
        count += i * i
    return count


print("\n--- 单线程 vs 多线程 CPU 计算 ---")

N = 10_000_000

# 单线程
start = time.time()
cpu_task(N)
cpu_task(N)
print(f"单线程 2 次: {time.time() - start:.2f} 秒")

# 多线程
start = time.time()
t1 = threading.Thread(target=cpu_task, args=(N,))
t2 = threading.Thread(target=cpu_task, args=(N,))
t1.start()
t2.start()
t1.join()
t2.join()
print(f"多线程 2 次: {time.time() - start:.2f} 秒")
print("（多线程并没有更快，因为 GIL 让它们实际上串行执行）")


# ============================================================
# 第三部分：面试考点汇总
# ============================================================

print("\n" + "=" * 50)
print("面试考点汇总")
print("=" * 50)

print("""
Q: Python 中 is 和 == 的区别？
A: == 比较值是否相等（调用 __eq__）
   is 比较内存地址是否相同（是否是同一个对象）
   例：a = [1,2]; b = [1,2]; a == b 为 True，a is b 为 False

Q: 可变对象做函数默认参数有什么问题？
A: def func(items=[]):
       items.append(1)
       return items
   默认参数在函数定义时只创建一次，所有调用共享同一个 list！
   解决：def func(items=None): items = items or []

Q: 深浅拷贝的区别？
A: copy.copy()  只拷贝最外层容器，内部对象共享引用
   copy.deepcopy() 递归拷贝所有层级，完全独立
   例：a = [[1]]; b = copy.copy(a); b[0].append(2) -> a 也变了

Q: 为什么 Python 没有真正的多线程并行？
A: 因为 GIL，同一时刻只有一个线程执行 Python 字节码
   真正的并行需用 multiprocessing（多进程）

Q: 垃圾回收的三种机制？
A: 1. 引用计数：主要机制，计数归零立即回收
   2. 标记-清除：解决循环引用
   3. 分代回收：新对象检查频繁，老对象检查稀疏
""")

print("=" * 50)
print("本节完毕！")
print("=" * 50)
