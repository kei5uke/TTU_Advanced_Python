import sys


def calculate(x: float, y: float):
    if x < 0 or y < 0: 
        raise ValueError("Negative value cannot be used")
    return (x * y)/2

def main():
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    result = calculate(x, y)
    print(result)

if __name__ == "__main__":
    main()