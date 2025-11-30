import json
# import ActionClassifier
import Dice
import anthropic
import re
'''
HackAndSlash()
Volley()
DefyDanger()
Defend()
SpoutLore()
DiscernRealities()
Parley()
AidOrInterfere()
근력
체력
민첩
지능
지혜
매력
자유행동

당신은 던전 월드 GM입니다. 다음 상황을 단계별로 분석하세요.

=== 현재 상황 ===
{current_scene}

=== 플레이어 행동 ===
{player_action}

=== 판정 결과 ===
무브: {move_name}
주사위: {dice_result}

=== 단계별 분석 (내부 추론) ===
1. 무브 규칙 확인:
   - 이 무브의 10+, 7-9, 6- 결과는?
   
2. 현재 결과({dice_result}) 해석:
   - 어떤 결과 범위에 속하나?
   - 규칙상 어떤 일이 일어나야 하나?
   
3. 극적 요소 고려:
   - 현재 긴장감은?
   - 어떤 합병증이 흥미로울까?
   
4. 결과 결정:
   - 구체적으로 무슨 일이 일어나나?

=== GM 묘사 ===
[위 분석을 바탕으로 플레이어에게 전달할 묘사를 작성]


'''


client = anthropic.Anthropic(

    api_key=input("api키를 입력해주세요 : ")  # 실제 키로 교체
)

def sendMessage(msg):
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=20000,
        temperature=1,
        messages=[{"role": "user", "content": msg}]
    )
    return message

player = {
    "name" : "다몬",
    "stat" : {
        "STR": 3,      # 힘 (근력)
        "DEX": 2,     # 민첩
        "CON": 1,  # 체력 (근력으로 표기했지만 실제로는 체력/건강)
        "INT": 0,  # 지능
        "WIS": -1,        # 지혜
        "CHA": 0
    }
}

# def action(Input_action):
#     if Input_action != None:
#         move_type = Input_action['move']
#         mofifier_stat = Input_action['stat']
#         player_input = Input_action['player_input']

#     else:
#         print("행동이 부정확합니다.")

#     return Dice.Roll(2, 6, player['stat'][mofifier_stat])



class prompt_created:
    def __init__(self):
        print("초기 세팅 중..")
        self.init_msg = f"""
        1. 괴물, 장소, 위험요소의 액션을 사용한다.
        2. 반갑지 않은 사실을 드러낸다.
        Critical_Question -> 마법 도구의 비밀, 황제의 비밀 등등 (답변이 고정됨) Major_Question -> 중요하지만, 유동성이 있음 Minor_Question -> (답변이 랜덤성을 가짐)

        3. 다가오는 위험의 징조를 보인다.
        위협의 종류를 정의 전투 -> 환경 -> 사회적/정치적 -> 초자연적 -> 자원고갈 -> 시간제한 ->

        4. 자원을 소비시킨다.
        5. PC의 액션을 역이용한다.
        6. PC들을 서로 떨어뜨린다.
        7. 특정 직업에 어울리는 기회를 제공한다.
        8. 특정 직업, 종족, 장비의 약점을 부각시킨다.
        9. 대가를 요구하는, 또는 대가 없는 기회를 제공한다.
        10. 누군가를 곤경에 빠뜨린다.
        11. 조건이나 결과를 내걸고 의향을 묻는다.
        던전 액션
        1. 풍경을 바꾼다.
        2. 도사린 위험의 징조를 드러낸다.
        3. 새로운 파벌이나 새로운 종류의 괴물을 등장시킨다.
        4. 기존의 파벌이나 이미 나온 종류의 괴물을 활용한다.
        5. 왔던 길을 돌아가게 한다.
        6. 대가를 치르면 얻을 수 있는 보물을 보여 준다.
        7. 캐릭터 중 한 명이 넘을 난관을 제시한다
        """
        sendMessage(self.init_msg)
        
    def send_prompt(self, player_move, now_situation):
        self.prompt1 = f"""
        어떤 판정이 필요할지만 알려주세요
        === 플레이어 행동 ===
        {player_move}
        === 현재 상황 ===
        {now_situation}
        응답은 반드시 이 JSON 형식으로만:
        {{
            "move": "무브 이름 또는 None",
            "stat": "STR/DEX/CON/INT/WIS/CHA 또는 null",
            "trigger": "무브가 발동된 이유",
            "confidence": 0.0~1.0
            "required_rolls": [
                {{
                    "type": "move_check",  // 무브 판정 (2d6+능력치)
                    "dice": "2d6",
                    "stat_modifier": "STR"  // 어떤 능력치 보너스
                }},
                {{
                    "type": "damage",  // 피해 굴림
                    "dice": "1d8",  // 무기 피해 주사위
                    "stat_modifier": "STR"  // 어떤 능력치 보너스
                }}
            ]
        }}
        """
        # text = re.sub(r'```json\s*|\s*```', '', text)
        # text = text.strip()
        message = sendMessage(self.prompt1)
        self.move_prompt = re.sub(r'```json\s*|\s*```', '', message.content[0].text)
        self.move_prompt = json.loads(self.move_prompt)
        # print(self.move_prompt)


    def resend_prompt(self, player_info, now_situation):
        for i in self.move_prompt['required_rolls']:
           dice = i['dice'].split('d')
           val = Dice.Roll(int(dice[0]), int(dice[1]), player_info['stats'][i['stat_modifier']])
           i['result'] = Dice.evaluate_roll(val)
        print('판정 : ', self.move_prompt['required_rolls'][0]['result'])
        self.prompt2 = f"""
        === 무브 정의 ===
        {self.move_prompt["trigger"]}
        {self.move_prompt["required_rolls"]}
        === 캐릭터 정보 ===
        {player_info}
        === 현재 상황 ===
        {now_situation}
        === 플레이어 행동 ===
        *판단 기준**:
        1. 위 행동이 무브를 발동시키는가?
        2. 발동된다면 정확히 어떤 무브인가?
        3. 어떤 능력치(STR/DEX/CON/INT/WIS/CHA)를 사용하는가?

        **중요**:
        - 단순 이동, 대화, 아이템 사용 등은 무브가 아님
        - 위험이나 목표 없는 행동은 무브가 아님
        - 애매하면 가장 가까운 무브 선택

        현재 상황과 무브정의로 아래 json을 작성

        응답은 반드시 이 JSON 형식으로만:
        {{
            "triggered_move": "무브명 (없으면 null)",
            "situation": 기존 형식처럼 문장열로 입력,
            "stat_used": "사용 능력치 (STR/DEX/CON/INT/WIS/CHA, 없으면 null)",
            "narrative": "현재 상황을 4~5줄로 생동감있게 서술",
            "player_info": {{
                "hp": 현재HP,
                "max_hp": 최대HP,
                "stats": {{
                    "STR": 근력값,
                    "DEX": 민첩값,
                    "CON": 체력값,
                    "INT": 지능값,
                    "WIS": 지혜값,
                    "CHA": 매력값
                }},
                "inventory": ["아이템1", "아이템2"],
                "conditions": ["상태1", "상태2"]  // 부상, 버프, 디버프 등
            }},
            "choices": [
                "선택지 1",
                "선택지 2",
                "선택지 3"
            ]
        }}
        """
        message = sendMessage(self.prompt2)
        self.move_prompt2 = re.sub(r'```json\s*|\s*```', '', message.content[0].text)
        self.move_prompt2 = json.loads(self.move_prompt2)
        # print(self.move_prompt2)
        return self.move_prompt2
    
# A = ActionClassifier.ActionClassifier()  
# while True: 
#     string = input("text : ")
#     act = A.classify(string, "고블린")
#     act['res'] = action(act)
#     print(act)