import mmh3
import numpy as np

class CountMinSketch:
    def __init__(self, width, depth,max_counter_size=2**16-1):
        """
        初始化 Count-Min Sketch
        :param width: 哈希表的宽度（每个哈希函数的桶数）
        :param depth: 哈希表的深度（哈希函数的个数）
        """
        self.width = width
        self.depth = depth
        self.table = np.zeros((depth, width), dtype=int)
        self.max_counter_size=max_counter_size

    def _hash(self, item, seed):
        """
        使用 MurmurHash 生成哈希值
        :param item: 输入的元素
        :param seed: 哈希种子
        :return: 哈希值（在 [0, width) 范围内）
        """
        return mmh3.hash(item, seed) % self.width

    def add(self, item):
        """
        将一个元素添加到 Count-Min Sketch
        :param item: 要添加的元素
        """
        item = str(item)  # 确保输入是字符串

        for seed in range(self.width,self.depth+self.width):
            index = self._hash(item, seed)
            self.table[seed-self.width][index]=np.minimum(self.table[seed-self.width][index]+1,self.max_counter_size)

    def count(self, item):
        """
        查询某个元素的频率
        :param item: 要查询的元素
        :return: 元素的频率
        """
        item = str(item)  # 确保输入是字符串
        min_count = float('inf')  # 初始化为正无穷，便于比
        for seed in range(self.width,self.depth+self.width):
            index = self._hash(item, seed)
            min_count = min(min_count, self.table[seed-self.width][index])  # 更新最小值

        return min_count

    def display(self):
        for i, row in enumerate(self.table):
            print(f"row {i + 1}: {row}")
        return

# 测试 Count-Min Sketch
if __name__ == "__main__":
    cms = CountMinSketch(width=10, depth=5)

    # 添加元素
    for i in range(115361):
        cms.add("apple")
    cms.add("banana")
    cms.add("apple")
    cms.add("apple")
    cms.add("cherry")
    cms.add("apple")
    # 查询元素频率
    print("apple:", cms.count("apple"))  # 输出 2
    print("banana:", cms.count("banana"))  # 输出 1
    print("cherry:", cms.count("cherry"))  # 输出 0
    cms.display()
