# 04_判断BST合法性

> 来源: Python面试实践/03_面试高频手撕题/04_判断BST合法性.py

`python
"""
【面试高频】判断二叉搜索树（BST）的合法性

题目：给定一个二叉树，判断其是否是一个有效的二叉搜索树。

BST 定义：
- 左子树所有节点值 < 根节点值
- 右子树所有节点值 > 根节点值
- 左右子树也必须是 BST

注意：是"所有"子树节点，不只是直接子节点！
  例如 [5,1,4,null,null,3,6] 不是 BST，因为 4 < 5 但 4 在右子树
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root: TreeNode) -> bool:
    """
    解法 1：递归 + 传递上下界

    思路：每个节点有合法值的范围，递归验证子树是否在范围内
    根节点范围 (-∞, +∞)
    左子树范围 (-∞, root.val)
    右子树范围 (root.val, +∞)

    面试推荐写法：简洁、直观
    """
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node:
            return True

        # 当前节点值必须在 (low, high) 范围内
        if node.val <= low or node.val >= high:
            return False

        # 递归验证左右子树
        return (validate(node.left, low, node.val) and
                validate(node.right, node.val, high))

    return validate(root)


def is_valid_bst_inorder(root: TreeNode) -> bool:
    """
    解法 2：中序遍历 —— BST 的中序遍历结果必须是递增的

    面试加分项：理解 BST 的中序遍历性质
    """
    prev_val = float('-inf')

    def inorder(node):
        nonlocal prev_val
        if not node:
            return True

        # 先遍历左子树
        if not inorder(node.left):
            return False

        # 检查当前节点
        if node.val <= prev_val:
            return False
        prev_val = node.val

        # 再遍历右子树
        return inorder(node.right)

    return inorder(root)


def is_valid_bst_iterative(root: TreeNode) -> bool:
    """
    解法 3：迭代中序遍历 —— 用栈模拟递归

    面试加分项：展示对迭代和递归的熟练掌握
    """
    if not root:
        return True

    stack = []
    prev_val = float('-inf')
    curr = root

    while stack or curr:
        # 走到最左边
        while curr:
            stack.append(curr)
            curr = curr.left

        # 弹出并处理
        curr = stack.pop()
        if curr.val <= prev_val:
            return False
        prev_val = curr.val

        # 转向右子树
        curr = curr.right

    return True


# ========================
# 测试
# ========================

if __name__ == "__main__":
    print("=" * 50)
    print("判断 BST 合法性")
    print("=" * 50)

    # 测试 1：有效 BST
    #     5
    #    / \
    #   1   8
    #      / \
    #     6   9
    root1 = TreeNode(5)
    root1.left = TreeNode(1)
    root1.right = TreeNode(8)
    root1.right.left = TreeNode(6)
    root1.right.right = TreeNode(9)

    # 测试 2：无效 BST
    #     5
    #    / \
    #   1   4
    #      / \
    #     3   6
    root2 = TreeNode(5)
    root2.left = TreeNode(1)
    root2.right = TreeNode(4)
    root2.right.left = TreeNode(3)
    root2.right.right = TreeNode(6)

    test_cases = [
        (root1, True, "有效 BST [5,1,8,None,None,6,9]"),
        (root2, False, "无效 BST [5,1,4,None,None,3,6]"),
        (None, True, "空树"),
        (TreeNode(1), True, "单节点"),
    ]

    for root, expected, desc in test_cases:
        r1 = is_valid_bst(root)
        r2 = is_valid_bst_inorder(root)
        r3 = is_valid_bst_iterative(root)
        status = "✅" if r1 == r2 == r3 == expected else "❌"
        print(f"{status} {desc}")
        print(f"   递归边界: {r1}, 中序递归: {r2}, 中序迭代: {r3}")
        print()

"""
【面试追问】

Q: 为什么不能只比较直接子节点？
A: BST 要求"左子树所有节点" < 根 < "右子树所有节点"。
   例如 [5,1,4,null,null,3,6]，4 的直接子节点 3 和 6 都满足，
   但 4 在右子树上，必须 > 5，所以不是 BST。

Q: 为什么用 float('-inf') 而不是 None？
A: 节点值可能是负数，用 float('-inf') 和 float('inf') 作为
   边界更安全。

Q: 中序遍历为什么能判断 BST？
A: BST 的中序遍历结果一定是严格递增的。如果不是，说明有问题。
   这个性质也常用于 BST 的排序输出。

Q: 时间/空间复杂度？
A: 三种方法都是 O(n) 时间（每个节点访问一次），
   递归法 O(h) 空间（递归栈深度，h 为树高），
   迭代法 O(h) 空间（显式栈）。
"""

`
`
