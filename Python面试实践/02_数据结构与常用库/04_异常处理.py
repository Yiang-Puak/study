# ============================================================
# 【零基础也能懂】异常处理 —— try / except / finally / else
# ============================================================


# ============================================================
# 第一部分：什么是异常？
# ============================================================

print("=" * 50)
print("第一部分：什么是异常？")
print("=" * 50)

# 异常 = 程序运行过程中出现的错误
# 比如：除以零、访问不存在的文件、类型不匹配...

print("\n--- 没有异常处理时 ---")
# 下面的代码会报错并导致程序终止
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"捕获到除零错误: {e}")


# ============================================================
# 第二部分：try / except 基础
# ============================================================

print("\n" + "=" * 50)
print("第二部分：try / except 基础")
print("=" * 50)

# 基本结构：
# try:
#     可能出错的代码
# except 异常类型:
#     出错后的处理

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print(f"警告：{a} 除以 0 不允许")
        return None

print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")
print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")


# --- 捕获多种异常 ---

print("\n--- 捕获多种异常 ---")

def parse_int(s):
    try:
        return int(s)
    except ValueError:
        print(f"'{s}' 不是有效的整数")
        return None
    except TypeError:
        print(f"传入的类型不对：{type(s)}")
        return None

print(f"parse_int('123') = {parse_int('123')}")
print(f"parse_int('abc') = {parse_int('abc')}")
print(f"parse_int(None)  = {parse_int(None)}")


# --- 捕获所有异常（不推荐，除非最后兜底） ---

print("\n--- 捕获所有异常 ---")
try:
    # 一些可能出各种问题的代码
    x = {}
    val = x["不存在的key"]
except Exception as e:
    print(f"捕获到异常: {type(e).__name__}: {e}")


# ============================================================
# 第三部分：else 和 finally
# ============================================================

print("\n" + "=" * 50)
print("第三部分：else 和 finally")
print("=" * 50)

# --- else：没出错时才执行 ---

print("\n--- else 的作用 ---")

def read_number_from_string(s):
    try:
        num = int(s)
    except ValueError:
        print("转换失败")
        return None
    else:
        # try 没出错才执行
        print("转换成功，执行 else")
        return num * 2

print(f"read_number_from_string('5') = {read_number_from_string('5')}")
print(f"read_number_from_string('x') = {read_number_from_string('x')}")

# --- finally：不管出不出错都执行 ---

print("\n--- finally 的作用 ---")

def demo_finally(will_error):
    try:
        if will_error:
            raise ValueError("故意出错")
        print("try 执行完毕")
    except ValueError:
        print("except 执行完毕")
    finally:
        print("finally：无论如何都会执行！")

print("--- 正常情况 ---")
demo_finally(False)

print("\n--- 异常情况 ---")
demo_finally(True)


# ============================================================
# 第四部分：自定义异常
# ============================================================

print("\n" + "=" * 50)
print("第四部分：自定义异常")
print("=" * 50)

# 继承 Exception 创建自己的异常
class ValidationError(Exception):
    """数据校验失败的异常"""
    pass

class NegativeNumberError(ValidationError):
    """负数不允许"""
    pass


def process_number(n):
    if n < 0:
        raise NegativeNumberError(f"不接受负数: {n}")
    return n * 10

try:
    result = process_number(-5)
except NegativeNumberError as e:
    print(f"自定义异常被捕获: {e}")


# ============================================================
# 第五部分：面试考点
# ============================================================

print("\n" + "=" * 50)
print("面试考点")
print("=" * 50)

print("""
Q: try/except/else/finally 的执行顺序？
A: 1. try 块执行
   2. 如果出错 -> 匹配 except -> 执行 finally
   3. 如果没出错 -> 执行 else -> 执行 finally
   finally 永远最后执行！

Q: 为什么不建议 except Exception？
A: 会捕获所有异常，包括系统退出信号 KeyboardInterrupt、SystemExit
   导致程序无法正常退出，掩盖真正的问题
   正确做法：捕获具体的异常类型

Q: finally 和 __exit__ 的区别？
A: finally 是语法层面的保证，不管是否异常都会执行
   __exit__ 是上下文管理器的协议方法，和 with 语句配合使用

Q: 怎么让异常不被吞掉同时做清理？
A: try:
       # 业务代码
   except SpecificError:
       # 记录日志
       raise  # 重新抛出异常
   finally:
       # 清理资源
""")

print("=" * 50)
print("本节完毕！")
print("=" * 50)
