
#prueba con pipes
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
filtered = []
for n in numbers:
    if n % 2 == 0:
        filtered.append(n)

multiplied = []
for n in filtered:
    multiplied.append(n * 10)
print(multiplied)

added = []
for n in multiplied:
    added.append(n + 5)
print(added)

total = 0
count = 0
for n in added:
    total += n
    count += 1
average = total / count
print(average)

from functools import reduce

pipe = lambda *fns: (lambda x: reduce(lambda v, f: f(v), fns, x))

set_lower_case = lambda str_: str_.lower()
concat_hash = lambda str_: "#" + str_
delete_spaces = lambda str_: str_.replace(" ", "")

str_format = pipe(
    concat_hash,
    delete_spaces,
    set_lower_case
)("texto EN tubería")

print(str_format)
# #textoentuberia