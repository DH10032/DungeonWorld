import random

def Roll(num_dice, dice_size, modifier):
    val = modifier
    for i in range(num_dice):
        val = val + random.randint(1, dice_size)
    return val

def evaluate_roll(Dice_Value):
    match Dice_Value:
        case n if n>=10:
            return "완전한 성공"
        case n if n>6:
            return "불완전 성공"
        case _:
            return "치명적 실패"
