# running = False
# temp = input('Enter a number to check if it is prime: ')
# guess = int(temp)

# if guess==6:
#     running = True


# while running:

#     agent = input('Enter a number to check if it is prime: ')
#     tips = int(agent)

#     if tips == 8:
#         print('You entered eight!')
#         print('Eight is not a prime number.')
#         break  # 正确答案，跳出循环
#     else:
#         print('You errored! Try again.')

# print('Done')


from copy import deepcopy
import decimal
from itertools import count
from math import fabs
import string


score = 66

leave = (
    "D"
    if 0 <= score < 60
    else (
        "C"
        if 60 <= score < 70
        else "B" if 70 <= score < 80 else "A" if 80 <= score < 90 else "E"
    )
)
print(leave)

# while True:
#     answer = input("do i ending this game? (yes/no): ")
#     if answer == "yes":
#         break

i = 1
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}*{i}={i*j}", end="\t")
    print()

lenX = [1, 2, 3, 4, 5, "xxx"]
lenC = ["mm", "cc", "dd"]
num = len(lenX)
print(lenX[-2])
print(num)
print(lenX[0:3])
print(lenX[:3])
print(lenX[2:])
print(lenX[:])
print(lenX[0:6:2])

lenX.append(6)
print(lenX)
lenX.insert(0, "cc")
print(lenX)
lenX.remove(1)
print(lenX)
lenX.pop()
print(lenX)
lenX.extend(lenC)
print(lenX)

# 切片写入会覆盖原有元素
lenX[len(lenC) :] = ["切片写入1", "切片写入2", "切片写入3"]
print(lenX)

print(lenX.count("cc"))
print(lenX.index("cc"))
num1 = deepcopy(lenX)

print(num1)

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
arr = [i * 2 for i in arr]
print(arr)

stringX2 = [s * 2 for s in "hello"]
print(stringX2)

# 字符转ASCII码
code = [ord(c) for c in "hello"]
print(code)

words = ["great", "hello", "word", "python", "phone", "awesome"]
words_with_p = [word for word in words if word.startswith("p")]
print(words_with_p)

str1 = "12321"
print("判断回文字符串" if str1 == str1[::-1] else "不是回文字符串")

strEn = "hello, World!"
print(
    strEn.capitalize(),
    strEn.casefold(),
    strEn.title(),
    strEn.swapcase(),
    strEn.upper(),
    strEn.lower(),
)
strCn = "内鬼，终止交易"
print(strCn.center(5), strCn.center(20), strCn.center(20, "x"))
print(strCn.ljust(20, "="), strCn.rjust(20, "_"))
# 0填充 长度总共15
print("999".zfill(15))


print(".    asdasd".isalpha())
print(".    asdasd".isspace())
print(".    asdasd\n".isspace())
print("    ".isspace())
print("asdasd ".isprintable())


print("123123".isdigit())
print("1234".isdecimal())
print("12".isnumeric())

count1 = decimal.Decimal("123.456457")
print(count1.quantize(decimal.Decimal(".00"), decimal.ROUND_DOWN))
# f-string .2f 保留两位小数，逗号分隔千位 但是会四舍五入
print(f"{count1:,.2f}")

print("{:.2%}".format(0.9865))

x = [1, 2, 3, 4, 5, 6, 7]
# 2个格子跳动删除
del x[::2]
print(x)
# 清空 类似于 clean（）
del x[:]
print(x)

s = [1, 2, 3, 5, 6, 0]
print(sum(s, 10))

sorted(s)
print(sorted(s, reverse=False))

q = [1, 2, 10, 4, 5, 7, 9, 0]
print(list(reversed(q)))
print(any(q))

setD = set("helobg")
print(setD)
setD.update([1, 1], "d3")
print(setD)
