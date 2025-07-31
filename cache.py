from moment import moment

class ListNode:
    def __init__(self, key, val, staleTime = 0):
        self.key = key
        self.val = val
        self.staleTime = moment().unix() + staleTime # default staleTime is immediate

class LRUCache:
    def __init__(self, options = { 'staleTime': 0, 'capacity': 100 }):
        self.staleTime = options.staleTime
        self.capacity = options.capacity
        self.hashMap = {}
        self.head = ListNode(0,0)
        self.tail = ListNode(0,0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def set(self, key, val):
        print('calling set with:', key, val)
        if key in self.hashMap:
            # remove original node from cache
            self.remove(self.hashMap[key])
        else:
            if len(self.hashMap) == self.capacity:
                # evict from tail
                print('evicting lru')
                evicted = self.tail.prev
                self.remove(evicted)
                del self.hashMap[evicted.key]
        # add new node to hashmap and head of cache
        node = ListNode(key, val, self.staleTime)
        self.add(node)
        self.hashMap[key] = node
        return 0
    
    def get(self, key):
        print('calling get with', key)
        if key in self.hashMap:
            node = self.hashMap[key]
            self.remove(node)
            self.add(node)
            print('value is', node.val)
            return node
        print('key not in cache')
        return -1

    def add(self, node):
        temp = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = temp
        temp.prev = node
    
    def remove(self, node):
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev
