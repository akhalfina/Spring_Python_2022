from typing import List


'''Решение задачи с алгоритмической сложностью O(n)'''
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dictionary = {}  # создание пустого словаря
        for element in range(len(nums)):  # итерация по всем элементам передаваемого списка
            diff = target - nums[element]  # элемент который необходимо найти
            if diff in dictionary:  # если элемент искомый для разницы находится в словаре
                return [element, dictionary[diff]]  # возвращаем лист c элементом по которому шла итерация и элемент с разницой из словаря
            dictionary[nums[element]] = element  # добавляем элемент и его позицию в словарь


