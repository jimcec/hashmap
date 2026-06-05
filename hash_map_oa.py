# Name: James Cecconi
# OSU Email: cecconiJ@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/1/2026
# Description:hash map implementation using open addressing with quadratic probing for collision resolution.
#           utilizes dynamic array to store hash table and hashentry objects to store key/value pairs directly inside array.
#           maintains average case performance of all operations at o(1) time complexity.
#           automatically resizes to double capacity when load factor reaches or exceeds zero point five.

from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        updates key/value pair in hash map.
        if key already exists, associated value is replaced.
        if key does not exist, new key/value pair is added.
        resizes table if load factor is >= 0.5.
        """
        # calculate load factor and resize if necessary
        if (self._size / self._capacity) >= 0.5:
            self.resize_table(self._capacity * 2)

        # calculate initial hash index
        initial_index = self._hash_function(key) % self._capacity

        # track first available tombstone index
        tombstone_idx = -1

        # initialize quadratic probing variable
        j = 0

        # probe until we find match or empty slot
        while True:
            # calculate quadratic probe index
            index = (initial_index + j ** 2) % self._capacity
            entry = self._buckets[index]

            # if slot is completely empty
            if entry is None:
                if tombstone_idx != -1:
                    self._buckets[tombstone_idx] = HashEntry(key, value)
                else:
                    self._buckets[index] = HashEntry(key, value)

                # increment size
                self._size += 1
                return

            # if matching key is found
            if entry.key == key:
                if entry.is_tombstone is True:
                    entry.is_tombstone = False
                    self._size += 1

                entry.value = value
                return

            if entry.is_tombstone is True and tombstone_idx == -1:
                tombstone_idx = index

            j += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        changes capacity of internal hash table.
        all active key/value pairs are rehashed into new table.
        """
        # return early if new capacity is smaller than current size
        if new_capacity < self._size:
            return

        # ensure new capacity is prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # store reference to old array of buckets
        old_buckets = self._buckets

        # reinitialize hash map state with new capacity
        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(None)

        self._capacity = new_capacity
        self._size = 0

        # iterate through old array to rehash items
        for i in range(old_buckets.length()):
            entry = old_buckets[i]

            # only rehash if entry exists and is not tombstone
            if entry is not None and entry.is_tombstone is False:
                self.put(entry.key, entry.value)

    def table_load(self) -> float:
        """
        returns current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        returns number of empty buckets in hash table.
        bucket is empty if it is none or is marked as tombstone.
        """
        # initialize counter for empty buckets
        empty_count = 0

        # loop through all buckets
        for i in range(self._capacity):
            entry = self._buckets[i]

            # check if bucket is completely empty or is tombstone
            if entry is None or entry.is_tombstone is True:
                empty_count += 1

        return empty_count

    def get(self, key: str) -> object:
        """
        returns value associated with given key.
        if key is not in hash map, returns none.
        """
        # calculate initial hash index
        initial_index = self._hash_function(key) % self._capacity

        # initialize probe counter
        j = 0

        while True:
            index = (initial_index + j ** 2) % self._capacity
            entry = self._buckets[index]

            if entry is None:
                return None

            # if we find matching key and it is not deleted
            if entry.key == key and entry.is_tombstone is False:
                return entry.value

            j += 1

    def contains_key(self, key: str) -> bool:
        """
        returns true if given key is in hash map, otherwise returns false.
        empty hash map does not contain any keys.
        """
        # handle empty map edge case
        if self._size == 0:
            return False

        # calculate initial hash index
        initial_index = self._hash_function(key) % self._capacity

        # initialize probe counter
        j = 0

        while True:
            index = (initial_index + j ** 2) % self._capacity
            entry = self._buckets[index]

            if entry is None:
                return False

            if entry.key == key and entry.is_tombstone is False:
                return True

            j += 1

    def remove(self, key: str) -> None:
        """
        removes given key and its associated value from hash map.
        if key is not in hash map, method does nothing.
        """
        # calculate initial hash index
        initial_index = self._hash_function(key) % self._capacity

        # initialize probe counter
        j = 0

        # probe until match or empty slot found
        while True:
            index = (initial_index + j ** 2) % self._capacity
            entry = self._buckets[index]

            if entry is None:
                return

            if entry.key == key and entry.is_tombstone is False:
                # mark as deleted using tombstone flag
                entry.is_tombstone = True
                # decrement total size
                self._size -= 1
                return

            j += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns dynamic array where each index contains tuple of key/value pair stored in hash map.
        order of keys in dynamic array does not matter.
        """
        # instantiate empty dynamic array to store results
        result_array = DynamicArray()

        # iterate through all slots based on capacity
        for i in range(self._capacity):
            entry = self._buckets[i]

            # check if slot has entry and is not marked as deleted
            if entry is not None and entry.is_tombstone is False:
                result_array.append((entry.key, entry.value))

        return result_array

    def clear(self) -> None:
        """
        clears contents of hash map.
        does not change underlying hash table capacity.
        """
        # reinitialize dynamic array
        self._buckets = DynamicArray()

        # populate array with none up to current capacity
        for _ in range(self._capacity):
            self._buckets.append(None)

        # reset size counter
        self._size = 0

    def __iter__(self):
        """
        enables hash map to iterate across itself.
        initializes tracking variable for progress.
        """
        # initialize index tracker for iteration
        self._iterator_index = 0

        # return instance as iterator
        return self

    def __next__(self):
        """
        returns next active item in hash map based on current location of iterator.
        only iterates over active items.
        """
        # loop until end of capacity
        while self._iterator_index < self._capacity:
            entry = self._buckets[self._iterator_index]

            # increment tracker for next call
            self._iterator_index += 1

            # if entry exists and is active, return it
            if entry is not None and entry.is_tombstone is False:
                return entry

        # raise stop iteration exception
        raise StopIteration


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f'Check that the load factor is acceptable after the call to resize_table().\n'
                  f'Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5')

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print('\nPDF - __iter__(), __next__() example 1')
    print('---------------------')
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print('\nPDF - __iter__(), __next__() example 2')
    print('---------------------')
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
