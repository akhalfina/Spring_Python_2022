from typing import List

'''Решение задачи с алгоритмической сложностью O(n log n). Бинарный поиск'''
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dictionary = {}  # делаем мапу, что бы потом получить индекс в исходном листе по элементу
        for element in range(len(nums)):
            dictionary[nums[element]] = element

        sortedList = sorted(nums)
        leftElementIndex = 0
        rightElementIndex = len(sortedList) - 1
        while leftElementIndex < rightElementIndex:
            sumElements = sortedList[leftElementIndex] + sortedList[rightElementIndex]
            if sumElements < target:
                leftElementIndex += 1
            elif sumElements > target:
                rightElementIndex -= 1
            else:
                return [dictionary[sortedList[leftElementIndex]], dictionary[sortedList[rightElementIndex]]]
