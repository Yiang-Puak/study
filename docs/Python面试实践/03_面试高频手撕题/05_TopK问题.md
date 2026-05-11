# 05_TopK问题

> 来源: Python面试实践/03_面试高频手撕题/05_TopK问题.py

`python
"""
【面试高频】Top K 问题 —— 堆排序 / 快速选择

题目：给定整数数组 nums 和整数 k，返回其中最大的 k 个元素（第 K 大 / 前 K 大）。

示例：
  输入: nums = [3,2,1,5,6,4], k = 2
  输出: [5,6] 或第 2 大的元素 5

变体：
  - 前 K 大：返回数组（可无序）
  - 第 K 大：返回单个数字
  - 前 K 小：逻辑对称
"""

import heapq
import random


def find_kth_largest_heap(nums: list, k: int) -> int:
    """
    解法 1：最小堆 —— 维护大小为 k 的堆

    思路：
    1. 维护一个大小为 k 的最小堆
    2. 堆顶就是第 k 大的元素
    3. 遍历数组，如果当前元素 > 堆顶，替换堆顶

    时间：O(n log k) —— 每个元素最多一次堆操作
    空间：O(k)

    面试推荐：代码简洁，适合数据流场景
    """
    # Python heapq 是最小堆，直接存取反的值变成"最大堆"效果
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)

    return min_heap[0]  # 堆顶 = 第 k 大


def find_kth_largest_quickselect(nums: list, k: int) -> int:
    """
    解法 2：快速选择（Quick Select）—— 快排思想的优化

    思路：
    1. 随机选 pivot 分区
    2. 如果 pivot 位置正好在 n-k，找到答案
    3. 如果位置 < n-k，在右半区继续找
    4. 如果位置 > n-k，在左半区继续找

    时间：平均 O(n)，最坏 O(n²)
    空间：O(1) 原地

    面试加分项：理解快排 partition 的扩展应用
    """
    def partition(left, right, pivot_idx):
        pivot_val = nums[pivot_idx]
        # 将 pivot 移到末尾
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot_val:
                nums[store_idx], nums[i] = nums[i], nums[store_idx]
                store_idx += 1

        # 把 pivot 放回正确位置
        nums[right], nums[store_idx] = nums[store_idx], nums[right]
        return store_idx

    def select(left, right, k_smallest):
        """找第 k_smallest 小的元素"""
        if left == right:
            return nums[left]

        pivot_idx = random.randint(left, right)
        pivot_idx = partition(left, right, pivot_idx)

        if k_smallest == pivot_idx:
            return nums[k_smallest]
        elif k_smallest < pivot_idx:
            return select(left, pivot_idx - 1, k_smallest)
        else:
            return select(pivot_idx + 1, right, k_smallest)

    # 第 k 大 = 第 (n-k) 小（0-indexed）
    return select(0, len(nums) - 1, len(nums) - k)


def top_k_heap(nums: list, k: int) -> list:
    """
    返回前 K 大元素（无序）

    面试要点：前 K 大和 第 K 大的区别
    """
    # 用 heapq.nlargest 最简洁
    return heapq.nlargest(k, nums)


def top_k_sorted(nums: list, k: int) -> list:
    """
    返回前 K 大元素（降序排列）
    """
    return sorted(nums, reverse=True)[:k]


# ========================
# 测试
# ========================

if __name__ == "__main__":
    print("=" * 50)
    print("Top K 问题")
    print("=" * 50)

    test_cases = [
        ([3, 2, 1, 5, 6, 4], 2, 5),      # 第 2 大 = 5
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),  # 第 4 大 = 4
        ([1], 1, 1),
        ([7, 6, 5, 4, 3, 2, 1], 3, 5),   # 第 3 大 = 5
    ]

    for nums, k, expected in test_cases:
        r1 = find_kth_largest_heap(nums.copy(), k)
        r2 = find_kth_largest_quickselect(nums.copy(), k)
        status = "✅" if r1 == r2 == expected else "❌"
        print(f"{status} nums={nums}, k={k} | 期望: {expected} | 堆: {r1}, 快选: {r2}")

    print("\n" + "=" * 50)
    print("前 K 大元素")
    print("=" * 50)

    nums = [3, 2, 1, 5, 6, 4]
    k = 3
    print(f"nums={nums}, k={k}")
    print(f"top_k_heap: {top_k_heap(nums, k)}")
    print(f"top_k_sorted: {top_k_sorted(nums, k)}")

"""
【面试追问】

Q: 堆和快速选择怎么选？
A: - 数据量小、内存充足：快速选择平均 O(n) 更快
   - 数据流、海量数据：最小堆 O(n log k) 更省内存，且支持动态添加
   - 需要前 K 个有序输出：堆 + 额外排序，或直接用 sorted

Q: Python 的 heapq 是最小堆，怎么实现最大堆？
A: 1）存取反的值：push(-num)，取出后再取反
   2）自定义类实现 __lt__ 反向比较
   3）用 heapq.nlargest / nsmallest

Q: 如果要求"前 K 个高频元素"呢？
A: 先用 Counter 统计频率，再用堆找频率 Top K。
   即 LeetCode 347，时间 O(n log k)。

Q: 如果 K 接近 n/2，还有更快的做法吗？
A: 用快速选择找中位数（第 n/2 大），然后 partition
   分成两部分，但复杂度仍是 O(n)。
"""

`
