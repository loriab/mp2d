import pathlib

with open(pathlib.Path(__file__).parent / 'GrimmeC6.txt') as handle:
    lines = handle.readlines()

GrimmeC6 = []
for line in lines:
    if line.strip():
        numbers = [float(itm) for itm in line.strip().split()]
        numbers[0] = int(numbers[0])
        numbers[1] = int(numbers[1])
        GrimmeC6.append(numbers)
