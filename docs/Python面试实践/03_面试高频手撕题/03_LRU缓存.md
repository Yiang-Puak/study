# 03_LRU缓存

> 来源: Python面试实践/03_面试高频手撕题/03_LRU缓存.py

`python
"""
【面试高频】LRU 缓存 —— 哈希表 + 双向链表

题目：设计和实现一个 LRU (最近最少使用) 缓存机制。
  - get(key)：如果 key 存在则返回 value，否则返回 -1
  - put(key, value)：插入或更新，如果容量满则淘汰最久未使用的

要求：get 和 put 操作时间复杂度都是 O(1)

示例：
  cache = LRUCache(2)
  cache.put(1, 1)
  cache.put(2, 2)
  cache.get(1)    # 返回 1
  cache.put(3, 3) # 淘汰 key 2
  cache.get(2)    # 返回 -1
"""


class ListNode:
    """双向链表节点"""
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU 缓存 —— 面试标准解法

    数据结构：哈希表 + 双向链表
    - 哈希表：key -> ListNode，O(1) 查找
    - 双向链表：按访问时间排序，头部最新，尾部最旧

    面试要点：
    - 为什么用双向链表？—— 删除节点时需要知道前驱，单链表无法 O(1) 删除
    - 为什么是 O(1)？—— 哈希表 O(1) 定位 + 双向链表 O(1) 移动节点
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> ListNode
        self.size = 0

        # 伪头部和伪尾部（简化边界处理）
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: ListNode) -> None:
        """从链表中移除节点"""
        prev, nxt = node.prev, node.next
        prev.next = nxt
        nxt.prev = prev

    def _add_to_head(self, node: ListNode) -> None:
        """将节点添加到头部（最新使用）"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: ListNode) -> None:
        """将已有节点移动到头部"""
        self._remove(node)
        self._add_to_head(node)

    def _pop_tail(self) -> ListNode:
        """移除尾部节点（最久未使用）"""
        node = self.tail.prev
        self._remove(node)
        return node

    def get(self, key: int) -> int:
        """获取值，并将节点移到头部"""
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_head(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        """插入或更新"""
        if key in self.cache:
            # 更新已有值
            node = self.cache[key]
            node.val = value
            self._move_to_head(node)
        else:
            # 创建新节点
            node = ListNode(key, value)
            self.cache[key] = node
            self._add_to_head(node)
            self.size += 1

            # 超出容量，淘汰尾部
            if self.size > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]
                self.size -= 1


# ========================
# Pythonic 版本（面试快速演示）
# ========================

from collections import OrderedDict


class LRUCacheOrderedDict:
    """
    使用 OrderedDict 的简洁版本 —— 适合快速展示思路

    OrderedDict 的 move_to_end + popitem(last=False) 天然支持 LRU
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# ========================
# 测试
# ========================

if __name__ == "__main__":
    print("=" * 50)
    print("LRU 缓存 —— 哈希表 + 双向链表")
    print("=" * 50)

    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(f"get(1) = {cache.get(1)} (期望: 1)")
    cache.put(3, 3)  # 淘汰 key 2
    print(f"get(2) = {cache.get(2)} (期望: -1)")
    cache.put(4, 4)  # 淘汰 key 1
    print(f"get(1) = {cache.get(1)} (期望: -1)")
    print(f"get(3) = {cache.get(3)} (期望: 3)")
    print(f"get(4) = {cache.get(4)} (期望: 4)")

    print("\n" + "=" * 50)
    print("LRU —— OrderedDict 版本")
    print("=" * 50)

    cache2 = LRUCacheOrderedDict(2)
    cache2.put(1, 1)
    cache2.put(2, 2)
    print(f"get(1) = {cache2.get(1)} (期望: 1)")
    cache2.put(3, 3)
    print(f"get(2) = {cache2.get(2)} (期望: -1)")

"""
【面试追问】

Q: 为什么不用单链表？
A: 删除节点时需要找到前驱节点，单链表需要 O(n) 遍历，
   双向链表直接通过 prev 指针 O(1) 访问前驱。

Q: 为什么用伪头部和伪尾部？
A: 避免处理头尾为空的边界情况，简化代码逻辑。

Q: Python 3.7+ dict 是有序的，可以直接用 dict 实现吗？
A: dict 确实保持插入顺序，但没有 move_to_end 方法。
   每次 get 时需要删除再插入才能更新顺序，比较麻烦。
   OrderedDict 提供了 move_to_end 和 popitem，更适合 LRU。

Q: 如果用 Redis 实现分布式 LRU？
A: Redis 的 LRU 淘汰策略（maxmemory-policy allkeys-lru），
   或者自己用 sorted set（score = 最后访问时间戳）实现。
"""

`
`
