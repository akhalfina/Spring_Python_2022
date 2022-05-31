from typing import List

'''Решение задачи с алгоритмической сложностью O(n^2)'''
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for element in range(len(nums)):  # итерация по всем элементам передаваемого списка
            for nearbyElement in range(element + 1, len(nums)):  # итерация по соседнему элементу от исходного
                if nums[nearbyElement] == target - nums[element]:
                    return [element, nearbyElement]
