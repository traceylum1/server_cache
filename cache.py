import time
class ListNode:
    def __init__(self, key, val, staleTime = 0):
        self.key = key
        self.val = val
        self.expiresAt = int(time.time()) + staleTime # default staleTime is immediate
        self.next = None
        self.prev = None

    def is_stale(self):
        return time.time() > self.expiresAt


'''
LRU Cache options defaults:
    staleTime = 0
    capacity = 100
'''
class LRUCache:
    def __init__(self, options=None):
        if options is None:
            options = {}
        self.staleTime = options.get('staleTime', 0)
        self.capacity = options.get('capacity', 100)
        self.hashMap = {}
        self.head = ListNode(0,0)
        self.tail = ListNode(0,0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def set(self, key, val):
        print('Calling set with:', key, val)

        node = self.hashMap.get(key)

        if node:
            # Update existing node
            self.remove(node)

        elif len(self.hashMap) == self.capacity:
            # Evict least recently used node
            print('Evicting LRU')
            lru = self.tail.prev
            self.remove(lru)
            del self.hashMap[lru.key]

        # Insert fresh node
        new_node = ListNode(key, val, self.staleTime)
        self.add(new_node)
        self.hashMap[key] = new_node
        return 0
    
    def get(self, key):
        print('Calling get with', key)
        
        node = self.hashMap.get(key)

        if not node: 
            print('Key not in cache')
            return None
        
        if node.is_stale:
            print('Record stale')
            self.remove(node)
            del self.hashMap[key]
            return None
        
        self.add(node)
        print('Value is', node.val)
        return node.val


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
