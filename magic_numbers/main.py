from pathlib import Path

def next_magic_num(num: str) -> str:
    length = len(num)
    if num == "9" * length:
        return "1" + "0" * (length - 1) + "1"
    half_idx = (length + 1) // 2
    left_half = num[:half_idx]
    if length % 2 == 0:
        candidate = left_half + left_half[::-1]
    else:
        candidate = left_half + left_half[:-1][::-1]
    if candidate > num:
        return candidate
    new_left_part = str(int(left_half) + 1)
    if (length % 2 == 0):
        return new_left_part + new_left_part[::-1]
    else:
        return new_left_part + new_left_part[:-1][::-1]

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    parsed = (x.strip() for x in data.split("\n") if x.strip())
    for num in parsed:
        print(next_magic_num(num))


if __name__ == "__main__":
    main()
