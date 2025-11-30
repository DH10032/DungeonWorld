import prompt
import sys
# from rich.layout import Layout
# from rich.panel import Panel
# from rich.console import Console
# from blessed import Terminal

player = {
        "hp": "현재HP",
        "max_hp": "최대HP",
        "stats": {
            "STR": 3,
            "DEX": 2,
            "CON": 0,
            "INT": 0,
            "WIS": -1,
            "CHA": 1,
        },
        "inventory": ['도검'],
        "conditions": []  #// 부상, 버프, 디버프 등
    }

# console = Console()

# console.print("밑줄 + 글자 굵게 빨갛게 출력!", style="bold underline red")
# console.print("가운데 정렬", justify="center", style="bold")
# console.print("왼쪽 정렬", justify="center", style="bold")
# console.print("오른쪽 정렬", justify="right", style="bold")

# term = Terminal()

# with term.fullscreen(), term.cbreak():
#     while True:
#         # Rich로 UI 그리기
#         print(term.home + term.clear)
        
#         layout = Layout()
#         layout.split_column(
#             Layout(name="header", size=3),
#             Layout(name="main"),
#             Layout(name="footer", size=3)
#         )

#         layout["main"].split_row(
#             Layout(name="stats"),
#             Layout(name="scene"),
#             Layout(name="inventory")
#         )
        
#         layout["header"].update(Panel("던전월드"))
#         layout["stats"].update(Panel("HP: 10"))
#         layout["scene"].update(Panel("동굴 입구"))
#         layout["inventory"].update(Panel("횃불\n단검"))
#         layout["footer"].update(Panel("입력"))
        
#         console.print(layout)
        
#         # 커서를 input 위치로
#         print(term.move_xy(2, term.height - 2) + "> ", end='', flush=True)
        
#         # 한 글자씩 입력 받기
#         user_input = ""
#         while True:
#             key = term.inkey()
#             if key.name == 'KEY_ENTER':
#                 break
#             elif key.name == 'KEY_BACKSPACE':
#                 user_input = user_input[:-1]
#             else:
#                 user_input += key
            
#             # 입력창 업데이트
#             print(term.move_xy(2, term.height - 2) + "> " + " " * 50, end='')
#             print(term.move_xy(2, term.height - 2) + "> " + user_input, end='', flush=True)
        
#         if user_input == "종료":
#             break

a = prompt.prompt_created()

now_situation = f'''
    === 현재 상황 ===
    - 어두운 동굴 입구
    - 고블린 전사(HP 12/12)가 단검을 들고 막고 있음
    - 플레이어는 한손검을 뽑은 상태"
    '''

while True:
    player_move = input("입력 : ")
    inp = input("보내시겠습니까? (y/n)")
    if inp == 'y':
        a.send_prompt(player_move, now_situation)
        b = a.resend_prompt(player, now_situation)

        player = b['player_info']
        now_situation = b['situation']
        print(b['narrative'])
        print()
        print(now_situation)
        print(player['stats'])
        print(player['inventory'])