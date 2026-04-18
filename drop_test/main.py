import math
from pathlib import Path

def min_num_of_drops(n: int, h: int) -> int:
    if n <= 0 or h <= 0:
        return 0
    if n == 1:
        return h
    max_useful_devices = math.ceil(math.log2(h + 1))
    if n >= max_useful_devices:
        return max_useful_devices
    dp = [0] * (n + 1)
    m = 0
    while dp[n] < h:
        m += 1
        for i in range(n, 0, -1):
            dp[i] += dp[i - 1] + 1
    return m

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    parsed = ((int(y.strip()) for y in x.strip().split(",")) for x in data.split("\n") if x.strip())
    for [n, h] in parsed:
        print(min_num_of_drops(n, h))


if __name__ == "__main__":
    main()
