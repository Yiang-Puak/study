# ============================================================
# 【零基础也能懂】上下文管理器 —— with 语句
# ============================================================


# ============================================================
# 第一部分：为什么需要 with？
# ============================================================

print("=" * 50)
print("第一部分：为什么需要 with？")
print("=" * 50)

# --- 1.1 不用 with 的麻烦 ---

# 打开文件的传统写法
print("\n--- 传统写法（容易出错）---")
f = open("temp_test.txt", "w")
try:
    f.write("hello world")
    # 如果这里出错了，f 不会被关闭，导致资源泄漏！
    # 比如：1 / 0
except Exception as e:
    print(f"出错了: {e}")
finally:
    f.close()  # 必须手动关闭，很容易忘记
    print("文件已关闭")

# --- 1.2 用 with 的简洁 ---

print("\n--- with 写法（简洁安全）---")
with open("temp_test.txt", "w") as f:
    f.write("hello world with")
    # 不管这里是否出错，with 退出时自动调用 f.close()
print("with 结束，文件已自动关闭")


# ============================================================
# 第二部分：with 的底层原理
# ============================================================

print("\n" + "=" * 50)
print("第二部分：with 的底层原理")
print("=" * 50)

# with 语句依赖两个特殊方法：
#   __enter__()  ：进入 with 代码块时调用
#   __exit__()   ：离开 with 代码块时调用（不管是否出错都会调用）

class MyResource:
    """模拟一个需要管理的资源"""

    def __init__(self, name):
        self.name = name
        print(f"[{self.name}] 资源对象被创建")

    def __enter__(self):
        print(f"[{self.name}] __enter__：获取资源")
        return self  # 返回的值会赋给 as 后面的变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type: 异常类型，exc_val: 异常值，exc_tb: 异常追踪
        if exc_type:
            print(f"[{self.name}] __exit__：发现异常 {exc_type.__name__}: {exc_val}")
        else:
            print(f"[{self.name}] __exit__：正常退出，释放资源")
        return True  # True 表示异常已处理，不向外传播

    def do_something(self):
        print(f"[{self.name}] 执行业务逻辑")
        # 模拟出错
        # raise ValueError("模拟错误")


print("\n--- 正常情况 ---")
with MyResource("连接A") as r:
    r.do_something()
# 输出：__enter__ -> 业务逻辑 -> __exit__

print("\n--- 异常情况 ---")
try:
    with MyResource("连接B") as r:
        r.do_something()
        raise ValueError("出错了！")
except ValueError:
    print("异常被外层捕获")


# ============================================================
# 第三部分：contextlib 简化写法
# ============================================================

print("\n" + "=" * 50)
print("第三部分：contextlib 简化装饰器写法")
print("=" * 50)

from contextlib import contextmanager

# 用装饰器快速创建上下文管理器，不用写类
@contextmanager
def managed_resource(name):
    """用生成器实现的上下文管理器"""
    print(f"[{name}] 获取资源（yield 之前）")
    try:
        yield name  # yield 的值会赋给 as 后面的变量
    except Exception as e:
        print(f"[{name}] 发生异常: {e}")
        raise
    finally:
        print(f"[{name}] 释放资源（yield 之后）")


print("\n--- 使用简化版 ---")
with managed_resource("数据库连接") as conn:
    print(f"使用资源: {conn}")


# ============================================================
# 第四部分：面试考点
# ============================================================

print("\n" + "=" * 50)
print("面试考点")
print("=" * 50)

print("""
Q: with 语句的原理是什么？
A: with obj as x:
       block
   等价于：
   x = obj.__enter__()
   try:
       block
   finally:
       obj.__exit__(...)

Q: __exit__ 的三个参数是什么？
A: exc_type（异常类型）、exc_val（异常值）、exc_tb（异常追踪）
   如果没有异常，三个参数都是 None

Q: __exit__ 返回 True 和 False 有什么区别？
A: 返回 True：异常被"吞掉"，不向外传播
   返回 False：异常继续向外抛出
   不写 return 默认返回 None（等价于 False）

Q: 常见应用场景？
A: 文件操作（自动关闭）、数据库连接（自动释放）、
   线程锁（自动 acquire/release）、性能计时、临时修改配置
""")

print("=" * 50)
print("本节完毕！")
print("=" * 50)
