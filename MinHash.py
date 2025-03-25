from hashlib import sha256
import array  # 使用数组结构减少内存占用


def minhash_similarity(mh1, mh2,k_minhash):
    # 使用数组遍历优化比较速度
    matches = sum(s1 == s2 for s1, s2 in zip(mh1.signature, mh2.signature))
    return matches / k_minhash

def generate_hash_params(seed,k):
    """生成16位参数，确保a为奇数"""
    a_list = array.array('H')
    b_list = array.array('H')

    for i in range(k):
        unique_seed = f"{seed}_{i}".encode()
        hash_bytes = sha256(unique_seed).digest()[:4]  # 取前4字节

        # 分解为两个16位参数
        a = int.from_bytes(hash_bytes[:2], 'big') | 1  # 强制a为奇数
        b = int.from_bytes(hash_bytes[2:4], 'big')

        # 限制在16位范围内
        a_list.append(a & 0xFFFF)
        b_list.append(b & 0xFFFF)

    return a_list, b_list

class MinHash16:
    def __init__(self, k, hash_params):
        self.k = k
        self.a_list, self.b_list, self.p = hash_params
        # 使用unsigned short数组存储（16位/2字节）
        self.signature = array.array('H', [0xFFFF] * k)  # 初始值为最大无符号短整型

    def update(self, element):
        element_hash = self._element_hash(element)
        for i in range(self.k):
            a = self.a_list[i]
            b = self.b_list[i]
            # 计算哈希值并限制在16位范围内
            h = (a * element_hash + b) % self.p
            # 直接操作数组元素减少类型转换
            if h < self.signature[i]:
                self.signature[i] = h

    @staticmethod
    def _element_hash(element):
        # 取SHA256前2字节生成16位哈希
        return int.from_bytes(
            sha256(str(element).encode()).digest()[:2],
            byteorder='big'
        ) & 0xFFFF  # 确保返回16位无符号数


class MinHashSystem16:
    def __init__(self, k=200, seed="minhash_seed"):
        self.k = k
        # 使用16位最大质数 (0xFFFF is 65535，但选择小于该值的质数更安全)
        self.p = 65521  # 最大16位质数（2^16 - 15）

        # 生成16位哈希参数
        self.a_list, self.b_list = generate_hash_params(seed)

        self.collections = {}



    def process_element(self, collection_id, element):
        if collection_id not in self.collections:
            self.collections[collection_id] = MinHash16(
                k=self.k,
                hash_params=(self.a_list, self.b_list, self.p)
            )
        self.collections[collection_id].update(element)

    def similarity(self, id1, id2):
        mh1 = self.collections.get(id1)
        mh2 = self.collections.get(id2)

        if not mh1 or not mh2:
            raise ValueError("集合不存在")

        # 使用数组遍历优化比较速度
        matches = sum(s1 == s2 for s1, s2 in zip(mh1.signature, mh2.signature))
        return matches / self.k


# 验证
if __name__ == "__main__":
    # 测试可复现性
    system1 = MinHashSystem16(seed="fixed_seed")
    system1.process_element("A", "apple")
    system1.process_element("A", "banana")
    sig1 = system1.collections["A"].signature.tolist()

    system2 = MinHashSystem16(seed="fixed_seed")
    system2.process_element("A", "apple")
    system2.process_element("A", "banana")
    sig2 = system2.collections["A"].signature.tolist()

    print("16位签名一致:", sig1 == sig2)  # 输出True

    # 性能测试
    test_system = MinHashSystem16(seed="test")
    data_stream = [
        ["A", "apple"],
        ["A", "banana"],
        ["A", "cherry"],
        ["A", "apple"],
        ["A", "apple"],
        ["A", "apple"],
        ["A", "banana"],
        ["A", "banana"],
        ["B", "apple"],
        ["B", "orange"],
        ["B", "grape"]
    ]
    for cid, elem in data_stream:
        test_system.process_element(cid, elem)

    print("A-B相似度:", test_system.similarity('A', 'B'))  # 示例输出0.0-0.3之间
    print("A-A相似度:", test_system.similarity('A', 'A'))  # 应为1.0