# ============================================================
# 【零基础也能懂】列表推导式 vs 生成器表达式
# ============================================================


# ============================================================
# 第一部分：列表推导式 —— 一行代码创建列表
# ============================================================

print("=" * 50)
print("第一部分：列表推导式（List Comprehension）")
print("=" * 50)

# --- 1.1 传统写法 vs 列表推导式 ---

# 传统写法：找出 1~10 中的偶数，并平方
result_old = []
for i in range(1, 11):
    if i % 2 == 0:
        result_old.append(i ** 2)
print(f"传统写法结果: {result_old}")

# 列表推导式：同样的逻辑，一行搞定
# 语法：[表达式 for 变量 in 可迭代对象 if 条件]
result_new = [i ** 2 for i in range(1, 11) if i % 2 == 0]
print(f"推导式结果: {result_new}")

# --- 1.2 列表推导式的语法结构 ---

# 最基础形式：[x for x in iterable]
simple = [x for x in [1, 2, 3]]
print(f"\n最基础: {simple}")  # [1, 2, 3]

# 带变换：[x * 2 for x in iterable]
doubled = [x * 2 for x in [1, 2, 3]]
print(f"带变换: {doubled}")  # [2, 4, 6]

# 带过滤：[x for x in iterable if 条件]
filtered = [x for x in [1, 2, 3, 4, 5] if x > 2]
print(f"带过滤: {filtered}")  # [3, 4, 5]

# 带变换 + 过滤
combined = [x ** 2 for x in [1, 2, 3, 4, 5] if x % 2 == 0]
print(f"变换+过滤: {combined}")  # [4, 16]

# 嵌套循环的推导式
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"\n二维数组展平: {flattened}")
# 等价于：
# for row in matrix:
#     for num in row:
#         flattened.append(num)


# ============================================================
# 第二部分：生成器表达式 —— 省内存的"惰性版"
# ============================================================

print("\n" + "=" * 50)
print("第二部分：生成器表达式（Generator Expression）")
print("=" * 50)

# --- 2.1 什么是生成器表达式？ ---

# 把列表推导式的 [] 换成 ()，就变成了生成器表达式
list_comp = [x ** 2 for x in range(1000000)]      # 列表推导式：全部存入内存
gen_expr = (x ** 2 for x in range(1000000))      # 生成器表达式：惰性计算

import sys
print(f"列表推导式内存: {sys.getsizeof(list_comp)} bytes")
print(f"生成器表达式内存: {sys.getsizeof(gen_expr)} bytes")
# 列表可能占用几十 MB，生成器只占几十 bytes！

# --- 2.2 怎么使用生成器？ ---

# 方法 1：逐个取（用 next）
gen = (x ** 2 for x in range(5))
print(f"\nnext(gen): {next(gen)}")  # 0
print(f"next(gen): {next(gen)}")  # 1
print(f"next(gen): {next(gen)}")  # 4
# 取完后再取会抛出 StopIteration 异常

# 方法 2：用 for 循环遍历
gen2 = (x ** 2 for x in range(5))
print("for 循环遍历生成器:", end=" ")
for val in gen2:
    print(val, end=" ")
print()

# 方法 3：转成列表（会立即计算所有值）
gen3 = (x ** 2 for x in range(5))
print(f"转成列表: {list(gen3)}")

# --- 2.3 面试考点：什么时候用哪个？ ---

print("\n--- 面试考点 ---")
print("""
列表推导式 []  ：当你需要多次访问结果、需要索引、需要全部结果时
生成器表达式 () ：当你只需遍历一次、数据量巨大、关注内存时

面试常见陷阱：
  1. 生成器只能用一次！遍历完就空了
  2. len(生成器) 报错，因为不知道有多少个
  3. 生成器不支持索引访问 gen[0] 报错
""")

# 演示"只能用一次"
gen_demo = (x for x in range(3))
print(f"第一次遍历: {list(gen_demo)}")
print(f"第二次遍历: {list(gen_demo)}")  # [] 已经空了！


# ============================================================
# 第三部分：字典推导式和集合推导式
# ============================================================

print("\n" + "=" * 50)
print("第三部分：字典推导式 & 集合推导式")
print("=" * 50)

# 字典推导式：{key: value for ...}
squares_dict = {x: x ** 2 for x in range(1, 6)}
print(f"字典推导式: {squares_dict}")  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 集合推导式：{value for ...}
squares_set = {x ** 2 for x in range(1, 11)}
print(f"集合推导式: {squares_set}")  # 自动去重，如 4 只出现一次


# ============================================================
# 第四部分：面试真题
# ============================================================

print("\n" + "=" * 50)
print("面试真题")
print("=" * 50)

# Q1: 列表推导式和生成器表达式有什么本质区别？
print("\nQ1: 列表推导式 vs 生成器表达式？")
print("A: 列表推导式立即计算所有结果，存入内存，返回列表")
print("   生成器表达式惰性计算，遍历时才生成值，返回生成器对象")
print("   内存占用：列表 O(n)，生成器 O(1)")

# Q2: 下面代码有什么问题？
# data = [line.strip() for line in open('huge_file.txt')]
print("\nQ2: 用列表推导式读取 1GB 的日志文件？")
print("A: 列表推导式会把所有行同时载入内存，导致内存溢出")
print("   正确做法：用生成器表达式 line.strip() for line in open(...)")
print("   或者直接用 for line in f: 逐行处理")

print("\n" + "=" * 50)
print("本节完毕！建议运行代码观察内存差异")
print("=" * 50)
