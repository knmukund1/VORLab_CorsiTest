import random, math
trial_nums = []
ROWS = 5
COLUMNS = 5
random.seed(0)


"""
def task_offset(level):
   if level == 1:
      return 2
   elif level == 2:
      return 4
   elif level == 3:
      return 1
   elif level == 4:
      return 3
   else:
      return 0
"""

def grid_square(r, c):
   global ROWS, COLUMNS
   if (r < 1 or c < 1 or r > ROWS or c > COLUMNS) or round((r - 1) * COLUMNS + c) == 0:
      return -1
   return round((r - 1) * COLUMNS + c)

"""
1. Structured Long
2. Structured Short
3. Unstructured Long
4. Unstructured Short
"""
def set_gen(type):
   global trial_nums, ROWS, COLUMNS
   c = trial_nums[len(trial_nums) - 1] % COLUMNS
   if c == 0:
      c = COLUMNS
   r = int(trial_nums[len(trial_nums) - 1] - c) / COLUMNS + 1
      
   nums = []
   
   #structured long: type 1
   if type == 1:
      for i in range(3,5):
         nums.append(grid_square(r + i, c))
         nums.append(grid_square(r - i, c))
         nums.append(grid_square(r, c + i))
         nums.append(grid_square(r, c - i))
         nums.append(grid_square(r + i, c + i))
         nums.append(grid_square(r + i, c - i))
         nums.append(grid_square(r - i, c + i))
         nums.append(grid_square(r - i, c - i))
   
   #structure short: type 2
   elif type == 2:
      nums.append(grid_square(r, c + 2))
      nums.append(grid_square(r, c - 2))
      nums.append(grid_square(r + 2, c))
      nums.append(grid_square(r - 2, c))
      nums.append(grid_square(r + 2, c + 2))
      nums.append(grid_square(r + 2, c - 2))
      nums.append(grid_square(r - 2, c + 2))
      nums.append(grid_square(r - 2, c - 2))
      
   #unstructured long: type 3
   elif type == 3:
      for i in range(1, 4):
         nums.append(grid_square(r + 4, c + i))
         nums.append(grid_square(r + 4, c - i))
         nums.append(grid_square(r - 4, c + i))
         nums.append(grid_square(r - 4, c - i))
         nums.append(grid_square(r + i, c + 4))
         nums.append(grid_square(r + i, c - 4))
         nums.append(grid_square(r - i, c + 4))
         nums.append(grid_square(r - i, c - 4))
      for i in range(1, 3):
         nums.append(grid_square(r + 3, c + i))
         nums.append(grid_square(r + 3, c - i))
         nums.append(grid_square(r - 3, c + i))
         nums.append(grid_square(r - 3, c - i))
         nums.append(grid_square(r + i, c + 3))
         nums.append(grid_square(r + i, c - 3))
         nums.append(grid_square(r - i, c + 3))
         nums.append(grid_square(r - i, c - 3))
         
   #unstructured short: type 4
   elif type == 4:
      nums.append(grid_square(r + 1, c + 2))
      nums.append(grid_square(r + 1, c - 2))
      nums.append(grid_square(r - 1, c + 2))
      nums.append(grid_square(r - 1, c - 2))
      nums.append(grid_square(r + 2, c + 1))
      nums.append(grid_square(r + 2, c - 1))
      nums.append(grid_square(r - 2, c + 1))
      nums.append(grid_square(r - 2, c - 1))
   
   nums = [ele for ele in nums if ele > 0]
   nums = [ele for ele in nums if ele not in trial_nums]
   if 0 in nums:
      print("hi")
   return nums

def random_sequence_gen(n, limit, type):
   global trial_nums
   temp_nums = []
   trial_nums.append(random.randint(1, limit))
   i = 0
   while i < n - 1:
      temp_nums = set_gen(type)
      #print(str(trial_nums[len(trial_nums) - 1]) + ": " + str(temp_nums))
      if len(temp_nums) != 0:
         random.shuffle(temp_nums)
         added = False
         for item in temp_nums:
            if item != -1 and item != 0 and not added:
               trial_nums.append(temp_nums[0])
               added = True
         i += 1
      else:
         trial_nums = []
         trial_nums.append(random.randint(1, limit))
         i = 0
   #print(trial_nums)
   copy_nums = trial_nums
   trial_nums = []
   return copy_nums

def random_num_set_gen(n, limit):
   all_nums = []
   nums = []
   cur_num = 0
   for i in range(1, limit):
      all_nums.append(i)
   random.shuffle(all_nums)
   for j in range(0, n):
      cur_num = all_nums[j]
      nums.append(cur_num)
   return nums

"""
def simple_random_num_set_gen(n):
   all_nums = []
   nums = []
   cur_num = 0
   if n < 10:
      for i in range(0, 10):
         all_nums.append(i)
   else:
      for i in range(0, n):
         all_nums.append(i % 10)
   random.shuffle(all_nums)
   for j in range(0, n):
      cur_num = all_nums[j]
      nums.append(cur_num)
   return nums
"""

def simple_random_num_set_gen(n):
   all_nums = []
   nums = []
   cur_num = 0
   if n < 10:
      for i in range(0, 10):
         all_nums.append(i)
   else:
      for i in range(0, n):
         all_nums.append(i % 10)
   random.shuffle(all_nums)
   for j in range(0, n):
      cur_num = all_nums[j]
      while len(nums) > 0 and cur_num == nums[-1]:
         random.shuffle(all_nums)
         cur_num = all_nums[0]
      nums.append(cur_num)
   if n >= 10:
      print(nums)
   return nums
