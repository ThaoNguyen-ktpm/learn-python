# n = int(input("nhập số phần tử: "))
# numbers = []
# for i in range(n):
#     num = int(input(f"nhập phần tử thứ {i+1}: "))
#     numbers.append(num)
# print(numbers)
##############################################################
# for i in range(n):
#     for j in range(i + 1, n):
#         if numbers[i] > numbers[j]:
#             numbers[i], numbers[j] = numbers[j], numbers[i]
# print("Danh sách sau khi sắp xếp:", numbers)
##############################################################
# tổng = sum(numbers)
# print("Tổng các phần tử trong danh sách:", tổng)

# trung_bình = sum(numbers) / n if n > 0 else 0
# print("Trung bình cộng các phần tử trong danh sách:", trung_bình)

# max_value = max(numbers) if numbers else None
# print("Giá trị lớn nhất trong danh sách:", max_value)

# min_value = min(numbers) if numbers else None
# print("Giá trị nhỏ nhất trong danh sách:", min_value)   

##################################################################
# def sum_of_numbers(a, b):
#     return a + b

# a = int(input("nhập số phần tử a: "))
# b = int(input("nhập số phần tử b: "))
# result = sum_of_numbers(a, b)
# print("Tổng của hai số là:", result)

# def is_even(num):
#     return num % 2 == 0

# if is_even(a):
#     print(f"{a} là số chẵn")
# else:
#     print(f"{a} là số lẻ")
    
# if is_even(b):
#     print(f"{b} là số chẵn")
# else:
#     print(f"{b} là số lẻ")
    
###################################################################################

# student= {}
# name = input("nhập tên học sinh: ")
# student["name"] = name

# age = int(input("nhập tuổi học sinh: "))
# student["age"] = age

# class_name = input("nhập lớp học sinh: ")
# student["class"] = class_name   

# print("Thông tin học sinh:", student)

# if student["age"] >= 18:
#     print(f"{student['name']} là học sinh trưởng thành.")
# else:
#     print(f"{student['name']} là học sinh chưa trưởng thành.")
#############################################################################
# numbers = set()

# for i in range(5):
#     value = int(input(f"nhập phần tử thứ {i+1}: "))
#     numbers.add(value)

# print(numbers)
# print(len(numbers))

# if 10 in numbers:
#     print("Có số 10")
# else:
#     print("Không có số 10")
#######################################################################
# a = int(input("Nhap a: "))
# b = int(input("Nhap b: "))
# c = int(input("Nhap c: "))

# t = (a, b, c)
# print(t)
# print(len(t))
# print(t[0], t[-1])

####################################################################
#nhập chuỗi
# text = input("Nhập chuỗi: ")
# print(text.upper())
# print(text.lower())
# print(text.strip())
# print(len(text.strip()))
# print(text.strip().split())

################################################################
# bắt lỗi nhập đúng yêu cầu
# try:
#     num = int(input("Nhập số: "))
#     print(f"Bình phương: {num ** 2}")
# except:
#     print("Lỗi: vui lòng nhập số nguyên")


################################################################

# numbers = []
# for i in range(1, 6):
#     numbers.append(i)
# print(numbers)  # [1, 2, 3, 4, 5]

# squared_numbers = [x ** 2 for x in numbers]
# print(squared_numbers)  # [1, 4, 9, 16, 25]

# odds = [x for x in range(1, 11) if x % 2 != 0]
# print(odds)  #[1, 3, 5, 7, 9]

##############################################################
# thêm danh sách cá nhân
# class Student:
#     def __init__(self, name, age, grade):
#         self.name = name
#         self.age = age
#         self.grade = grade
    
#     def display(self):
#         return f"Tên: {self.name}, Tuổi: {self.age}, Lớp: {self.grade}"

# student1 = Student("Thao", 21, "12A")
# print(student1.display())

##############################################################
# bình phương list 
# numbers = [1, 2, 3, 4, 5, 6]
# evens = list(filter(lambda x: x % 2 == 0, numbers))
# print(evens)  # [2, 4, 6]

###########################################################
# kiểm tra email hợp lệ
# import re

# pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
# email = "thao@gmail.com"

# if re.match(pattern, email):
#     print("Email hợp lệ")
# else:
#     print("Email không hợp lệ")
#############################################################
#thay thế số trong chuỗi bằng X
# import re

# text = input("Nhập chuỗi: ")
# numbers = re.findall(r"\d+", text)
# new_text = re.sub(r"\d+", "X", text)

# print(f"Số tìm được: {numbers}")
# print(f"Chuỗi sau khi thay thế: {new_text}")
##############################################################

# thêm sửa xóa cơ bản
tasks = []

while True:
    print("\n=== To-do List ===")
    print("1. Thêm công việc")
    print("2. Xem danh sách")
    print("3. Xóa công việc")
    print("4. Thoát")
    
    choice = input("Chọn (1-4): ")
    
    if choice == "1":
        task = input("Nhập công việc: ")
        tasks.append(task)
        print("✓ Thêm thành công")
    
    elif choice == "2":
        if tasks:
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
        else:
            print("Danh sách trống")
    
    elif choice == "3":
        if tasks:
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
            idx = int(input("Xóa công việc số: ")) - 1
            if 0 <= idx < len(tasks):
                tasks.pop(idx)
                print("✓ Xóa thành công")
            else:
                print("Số không hợp lệ")
        else:
            print("Danh sách trống")
    
    elif choice == "4":
        print("Tạm biệt!")
        break
    
    else:
        print("Chọn không hợp lệ")
