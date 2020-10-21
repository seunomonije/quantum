import cirq
import numpy as np
import matplotlib 
import random 
import socket
import select
import time
import pickle

class Sort:

  def __init__(self, arr):
    self.arr = arr

  def mergeSort(self, arr):
    if len(arr) > 1:
        mid = len(arr)//2 # // signifies floor division
        left = arr[:mid]
        right = arr[mid:]

        self.mergeSort(left)
        self.mergeSort(right)

        i=j=k = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i+=1
            else:
                arr[k] = right[j]
                j+=1
            k+=1

        # Handling stragglers
        while i < len(left):
            arr[k] = left[i]
            i+=1
            k+=1
        
        while j < len(right):
            arr[k] = right[j]
            j+=1
            k+=1
      
  def performMergeSort(self):
      self.mergeSort(self.arr)

  def printArray(self):
      for i in range(len(self.arr)):
          print(self.arr[i], end=" ")
        
