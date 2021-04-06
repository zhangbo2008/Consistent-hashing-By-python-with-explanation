'''
一致性哈希算法:

'''

# -*- coding: utf-8 -*-
import hashlib


class YHash(object):
    def __init__(self, nodes=None, n_number=3):
        """
        :param nodes:           所有的节点
        :param n_number:        一个节点对应多少个虚拟节点
        :return:
        """
        self._n_number = n_number  # 每一个节点对应多少个虚拟节点，这里默认是3个
        self._node_dict = dict()  # 用于将虚拟节点的hash值与node的对应关系
        self._sort_list = []  # 用于存放所有的虚拟节点的hash值，这里需要保持排序
        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        """
        添加node，首先要根据虚拟节点的数目，创建所有的虚拟节点，并将其与对应的node对应起来
        当然还需要将虚拟节点的hash值放到排序的里面
        这里在添加了节点之后，需要保持虚拟节点hash值的顺序
        :param node:
        :return:
        """
        for i in range(self._n_number):  # 对于每一个节点, 我们添加3个虚拟节点.
            node_str = "%s%s" % (node, i) # 所以哈希的子节点就是节点名字后面加上0,1,2
            key = self._gen_key(node_str)
            self._node_dict[key] = node      # 这个是哈希和node的对应表.-------注意这里面使用了3个虚拟节点,他们返回的服务器名字都是node!!!!!!!!!!!!
            self._sort_list.append(key)  # 这个排序数组在get算法中使用.
        self._sort_list.sort()

    def remove_node(self, node):
        """
        这里一个节点的退出，需要将这个节点的所有的虚拟节点都删除
        :param node:
        :return:
        """
        for i in range(self._n_number):
            node_str = "%s%s" % (node, i)
            key = self._gen_key(node_str) # 核心操作就是下面2个删除功能就够了.
            del self._node_dict[key]
            self._sort_list.remove(key)

    def get_node(self, key_str):
        """
        返回这个字符串应该对应的node，这里先求出字符串的hash值，然后找到第一个小于等于的虚拟节点，然后返回node
        如果hash值大于所有的节点，那么用第一个虚拟节点
        :param :
        :return:
        """
        if self._sort_list: # 如果有node
            key = self._gen_key(key_str)
            for node_key in self._sort_list:
                if key <= node_key:
                    return self._node_dict[node_key] # 根据node_key返回真实服务器地址即可.#  从这里面可以看出虚拟节点的使用效果.不适用虚拟节点之前.的图是这样的

                '''
                        2
                1                      3
                
                           4                          
                4个服务器绕城一圈. 这样比如删除4之后, 那么1 上覆盖的弧长就是2,3的2倍了.
            但是使用虚拟节点之后.我们的图变成这样. 比如每个服务器对应虚拟节点是2个.
                         41
                 20                   21
            10                        30
                40                11
                      31                         比如绕城这样一圈,因为哈斯算法的随机性.所以等分布的.
                                                这时我们删除4这个节点. 那么 40,41 都没了.
                                                所以40那部分的数据给10了.41那部分的给21了.所以还是均衡的.
                                                不会像上面那个都给1. 所以虚拟节点多,是一个好方法!!!!!!!!!!!!!
                
                
                
                
                
                
                
                
                '''










            return self._node_dict[self._sort_list[0]] # 如果大于所有的哈希值,就用第一个就行了.
        else:
            return None

    @staticmethod
    def _gen_key(key_str):
        """
        通过key，返回当前key的hash值，这里采用md5
        :param key:
        :return:
        """
        input_name = hashlib.md5()

        input_name.update(key_str.encode("utf-8"))

        return  input_name.hexdigest()


fjs = YHash(["127.0.0.1", "192.168.1.1"])
fjs.add_node('127.0.0.2')
fjs.add_node('127.0.0.3')
fjs.add_node('127.0.0.4')
fjs.remove_node('127.0.0.1')
print(fjs.get_node("fjs32121"))  # 输入一个字符串表示数据,然后 get_node返回应该用什么服务器来处理这个数据.
print(fjs.get_node("12"))