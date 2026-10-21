# ------------------------------
# Component 1 : รับคะแนน
# ------------------------------
def input_score():
    score = float(input("กรอกคะแนน (0-100): "))
    return score


# ------------------------------
# Component 2 : คำนวณเกรด
# ------------------------------
def calculate_grade(score):
    if score >= 80:
        return "A"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "C+"
    elif score >= 60:
        return "C"
    elif score >= 55:
        return "D+"
    elif score >= 50:
        return "D"
    else:
        return "F"


# ------------------------------
# Component 3 : แสดงผล
# ------------------------------
def display_result(score, grade):
    print("\n===== ผลการคำนวณ =====")
    print(f"คะแนน : {score}")
    print(f"เกรด   : {grade}")


# ------------------------------
# Main Program
# ------------------------------
def main():
    score = input_score()
    grade = calculate_grade(score)
    display_result(score, grade)


if __name__ == "__main__":
    main()
