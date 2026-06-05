# Name: James Cecconi
# OSU Email: cecconij@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/1/2026
# Description:hash map implementation using separate chaining for collision resolution.
#             utilizes dynamic array to store hash table and singly linked list objects to store chains of key/value pairs.
#             maintains average case performance of all operations at o(1) time complexity.
#             automatically resizes to double capacity when load factor reaches or exceeds one.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        updates a key/value pair in the hash map.
        if the key already exists, its value is replaced.
        if the key does not exist, a new key/value pair is added.
        resizes the table if the load factor is >= 1.0.
        """
        # check load factor and resize if necessary
        if (self._size / self._capacity) >= 1.0:
            self.resize_table(self._capacity * 2)

        # calculate hash and index
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity

        # retrieve linked list (bucket) at calculated index
        bucket = self._buckets[index]

        # check if key already exists in linked list
        existing_node = bucket.contains(key)

        if existing_node is not None:
            existing_node.value = value

        else:
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        changes the capacity of the internal hash table.
        all existing key/value pairs are rehashed into the new table.
        """
        # check if new_capacity is valid
        if new_capacity < 1:
            return

        # make sure new capacity is a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # create new empty DynamicArray with new capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        old_buckets = self._buckets

        # update map's internal state to new, empty table
        self._buckets = new_buckets
        self._capacity = new_capacity
        self._size = 0  # Reset size because put() will increment it back up

        # rehash all existing key/value pairs into new table
        for i in range(old_buckets.length()):
            bucket = old_buckets[i]

            #  LinkedList class has an iterator, loop through nodes directly
            for node in bucket:
                self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        returns the current hash table load factor.
        calculated as (total number of elements) / (total number of buckets).
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        returns number of empty buckets in hash table.
        """
        # initialize counter for empty buckets
        empty_count = 0

        # iterate through dynamic array of buckets
        for i in range(self._buckets.length()):
            # check if linked list at current index is empty
            if self._buckets[i].length() == 0:
                empty_count += 1

        # return final count
        return empty_count

    def get(self, key: str) -> object:
        """
        returns value associated with given key.
        if key is not in hash map, returns none.
        """
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity

        node = self._buckets[index].contains(key)

        if node is not None:
            return node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        returns true if given key is in hash map, otherwise returns false.
        empty hash map does not contain any keys.
        """
        if self._size == 0:
            return False

        hash_val = self._hash_function(key)
        index = hash_val % self._capacity

        if self._buckets[index].contains(key) is not None:
            return True

        return False

    def remove(self, key: str) -> None:
        """
        removes given key and its associated value from hash map.
        if key is not in hash map, method does nothing.
        """
        # calculate hash value and index for given key
        hash_val = self._hash_function(key)
        index = hash_val % self._capacity

        # access bucket at calculated index
        bucket = self._buckets[index]

        # attempt to remove key from linked list
        # remove method returns true if successful
        if bucket.remove(key) is True:
            # decrement size of hash map
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns dynamic array where each index contains tuple of key/value pair stored in hash map.
        order of keys in dynamic array does not matter.
        """
        # initialize empty dynamic array to hold results
        result_array = DynamicArray()

        # iterate through all buckets in hash map
        for i in range(self._buckets.length()):
            bucket = self._buckets[i]

            # iterate through nodes in current linked list
            for node in bucket:
                result_array.append((node.key, node.value))

        # return populated array
        return result_array

    def clear(self) -> None:
        """
        clears contents of hash map.
        does not change underlying hash table capacity.
        """
        # create new dynamic array to replace existing one
        self._buckets = DynamicArray()

        # populate array with empty linked lists matching current capacity
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # reset size counter to zero
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    finds mode or modes and returns them in dynamic array along with highest frequency.
    must run in o(n) time complexity.
    """
    # instantiate separate chaining hash map
    map = HashMap()

    # loop through elements in provided dynamic array
    for i in range(da.length()):
        key = da[i]
        current_count = map.get(key)

        if current_count is None:
            # key is not in map yet, add it with count of one
            map.put(key, 1)
        else:
            # key exists, increment count
            map.put(key, current_count + 1)

    # retrieve all key and value tuples from map
    pairs = map.get_keys_and_values()

    # initialize variables to track highest frequency and corresponding modes
    max_freq = 0
    modes = DynamicArray()

    # iterate over pairs to determine which ones are modes
    for i in range(pairs.length()):
        key, count = pairs[i]

        if count > max_freq:
            # found new highest frequency
            max_freq = count
            # reset modes array with fresh dynamic array
            modes = DynamicArray()
            modes.append(key)
        elif count == max_freq:
            # found tie for highest frequency
            modes.append(key)

    return modes, max_freq


# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print('\nPDF - put example 1')
    print('-------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - put example 2')
    print('-------------------')
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - resize example 1')
    print('----------------------')
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print('\nPDF - resize example 2')
    print('----------------------')
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print('\nPDF - table_load example 1')
    print('--------------------------')
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print('\nPDF - table_load example 2')
    print('--------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - empty_buckets example 1')
    print('-----------------------------')
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print('\nPDF - empty_buckets example 2')
    print('-----------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print('\nPDF - get example 1')
    print('-------------------')
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print('\nPDF - get example 2')
    print('-------------------')
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print('\nPDF - contains_key example 1')
    print('----------------------------')
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print('\nPDF - contains_key example 2')
    print('----------------------------')
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print('\nPDF - remove example 1')
    print('----------------------')
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print('\nPDF - get_keys_and_values example 1')
    print('------------------------')
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print('\nPDF - clear example 1')
    print('---------------------')
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print('\nPDF - clear example 2')
    print('---------------------')
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print('\nPDF - find_mode example 1')
    print('-----------------------------')
    da = DynamicArray(['apple', 'apple', 'grape', 'melon', 'peach'])
    mode, frequency = find_mode(da)
    print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}')

    print('\nPDF - find_mode example 2')
    print('-----------------------------')
    test_cases = (
        ['Arch', 'Manjaro', 'Manjaro', 'Mint', 'Mint', 'Mint', 'Ubuntu', 'Ubuntu', 'Ubuntu'],
        ['one', 'two', 'three', 'four', 'five'],
        ['2', '4', '2', '6', '8', '4', '1', '3', '4', '5', '7', '3', '3', '2']
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}\n')
