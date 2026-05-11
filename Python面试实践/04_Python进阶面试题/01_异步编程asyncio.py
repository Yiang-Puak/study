# ============================================================
# 【零基础也能懂】异步编程 asyncio
# ============================================================
# 类比：餐厅服务员点单
#   同步 = 一次只服务一桌，点完单等厨师做完才服务下一桌（低效）
#   异步 = 同时服务很多桌，点完单让厨师去做，服务员先去服务其他桌（高效）
# ============================================================

import asyncio
import time


# ============================================================
# 第一部分：同步 vs 异步 直观对比
# ============================================================

print("=" * 50)
print("第一部分：同步 vs 异步 直观对比")
print("=" * 50)

# --- 同步写法：串行执行 ---

print("\n--- 同步执行 ---")

def sync_task(name, duration):
    """模拟一个耗时的任务"""
    print(f"[{name}] 开始，预计耗时 {duration} 秒")
    time.sleep(duration)  # time.sleep 会"卡住"整个线程
    print(f"[{name}] 完成")
    return f"{name} 的结果"


def run_sync():
    start = time.time()
    sync_task("任务A", 1)
    sync_task("任务B", 1)
    sync_task("任务C", 1)
    print(f"同步总耗时: {time.time() - start:.2f} 秒")


run_sync()

# --- 异步写法：并发执行 ---

print("\n--- 异步执行 ---")

async def async_task(name, duration):
    """异步版本的耗时任务"""
    print(f"[{name}] 开始，预计耗时 {duration} 秒")
    await asyncio.sleep(duration)  # await = "挂起"这个任务，去做别的事
    print(f"[{name}] 完成")
    return f"{name} 的结果"


async def run_async():
    start = time.time()

    # 创建三个任务，让它们同时运行
    task_a = async_task("任务A", 1)
    task_b = async_task("任务B", 1)
    task_c = async_task("任务C", 1)

    # asyncio.gather 同时运行多个任务
    results = await asyncio.gather(task_a, task_b, task_c)

    print(f"异步总耗时: {time.time() - start:.2f} 秒")
    print(f"结果: {results}")


# 运行异步代码需要事件循环
asyncio.run(run_async())


# ============================================================
# 第二部分：async / await 核心概念
# ============================================================

print("\n" + "=" * 50)
print("第二部分：async / await 核心概念")
print("=" * 50)

print("""
核心三要素：

1. async def  ：定义一个"异步函数"
   - 调用 async def 函数不会立即执行，而是返回一个"协程对象"（coroutine）
   - 就像预约了一件事，但还没真正去做

2. await       ："等待"一个异步操作完成
   - await 后面的对象必须是"可等待的"（协程、任务、Future）
   - await 时，当前任务"挂起"，事件循环可以去执行其他任务
   - 类比：等咖啡的时候，服务员先去服务其他顾客

3. asyncio.run() ：启动事件循环
   - 创建事件循环，运行最顶层的协程，最后关闭循环
   - 一个程序通常只有一个 asyncio.run() 入口
""")


# --- 直观演示 ---

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def demo():
    print("开始于", time.strftime("%X"))

    # 顺序执行（用了 await，会等前一个完成）
    await say_after(1, "hello")
    await say_after(1, "world")

    print("结束于", time.strftime("%X"))


print("\n--- 顺序执行（共 2 秒）---")
asyncio.run(demo())


async def demo_concurrent():
    print("开始于", time.strftime("%X"))

    # 并发执行（创建 Task，交给事件循环调度）
    task1 = asyncio.create_task(say_after(1, "hello"))
    task2 = asyncio.create_task(say_after(1, "world"))

    await task1
    await task2

    print("结束于", time.strftime("%X"))


print("\n--- 并发执行（约 1 秒）---")
asyncio.run(demo_concurrent())


# ============================================================
# 第三部分：asyncio.gather 和 create_task
# ============================================================

print("\n" + "=" * 50)
print("第三部分：asyncio.gather vs create_task")
print("=" * 50)

print("""
asyncio.create_task(coro)  ：
  - 将协程"包装"成 Task，放入事件循环的任务队列
  - Task 会立即被调度，不需要 await 才启动
  - 返回 Task 对象，可以 await 它获取结果

asyncio.gather(*tasks)     ：
  - 同时运行多个任务，等全部完成后返回结果列表
  - 等价于分别 create_task 再分别 await
  - 有一个出错时，其他任务继续运行（默认行为）
""")


# ============================================================
# 第四部分：面试考点
# ============================================================

print("\n" + "=" * 50)
print("面试考点")
print("=" * 50)

print("""
Q: async/await 和 threading 有什么区别？
A: - threading 是真正的多线程，由操作系统调度，有 GIL 限制
   - async/await 是单线程的"协程"，由事件循环调度，没有线程切换开销
   - 协程更适合大量 I/O 等待场景（如爬虫、Web 服务器）

Q: asyncio 能解决 CPU 密集型任务吗？
A: 不能！asyncio 只解决"等待"问题，不解决"计算"问题。
   CPU 密集型仍需 multiprocessing 绕过 GIL。

Q: await 后面的函数必须是 async def 吗？
A: 不一定。await 后面可以是：
   - 协程对象（async def 的返回值）
   - Task 对象
   - Future 对象
   - 任何实现了 __await__ 方法的对象

Q: 常见的 asyncio 坑？
A: 1. 在同步函数里直接调用 async 函数（要用 asyncio.run）
   2. 在 async 函数里用 time.sleep 而不是 asyncio.sleep
   3. 忘记 await（协程对象没有真正执行）
   4. 在 Jupyter 里 asyncio.run 报错（用 await 直接运行）
""")

print("=" * 50)
print("本节完毕！")
print("=" * 50)
