correctness = False
while not correctness:
    size = input()
    if size.isdigit():
        size = int(size)
        correctness = True
    else:
        print("Please enter a correct number.")
queensLocations = [-1] * size
solutions = 0

def checkPlace(targetRow, column) :
    """چک می کند وزیری که قرار داریم توسط وزیران دیگر مورد حمله قرار می گیرد یا خیر"""
    # global queensLocations مکان هایی که وزیر ها در ان قرار دارند
    for i in range(targetRow):
        if (
            queensLocations[i] == column
            or queensLocations[i] - i == column - targetRow
            or queensLocations[i] + i == column + targetRow
        ):

            return False
    return True


def putQueen(targetRow):
    """وزیر را قرار می دهد(اصل منطق برنامه)
    یک تابع باز گشتی است """
    global queensLocations, size, solutions
    if targetRow == size: # شرط پایان تابع بازکشتی است
        solutions += 1 # راه حل جدید پیدا شده است
    else:
        for column in range(size):
            if checkPlace(targetRow, column):
                queensLocations[targetRow] = column
                putQueen(targetRow + 1)
                
                
def initialize() -> None:
    putQueen(0)
    print(solutions)

initialize()
