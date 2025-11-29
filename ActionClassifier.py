

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

"""2단계 분류"""
class ActionClassifier:
    def __init__(self):
        self.model = SentenceTransformer(
            'distiluse-base-multilingual-cased-v2'
        )
        
        # 1단계: 액션 분류
        self.action_templates = {
            "hack_and_slash": [
                "오크를 검으로 공격한다",
                "적의 목을 향해 벤다",
                "단검으로 찌른다",
                "도끼를 내리친다",
                "몽둥이로 때린다",
                "검을 휘두른다",
                "적을 가격한다",
                "망치로 친다",
                "고블린을 향해 칼을 휘두른다",
                "적의 약점을 노려 찌른다",
                "전력을 다해 내리친다",
                "연속으로 베어낸다",
                "괴물을 향해 검을 내리친다",
                "급소를 노려 단검을 찌른다",
                "도끼를 크게 휘두른다",
                "트롤의 다리를 벤다",
                "머리를 향해 내리친다",
                "검으로 적을 가격한다",
                "창으로 찌른다",
                "전투 도끼를 휘두른다",
            ],
            "volley": [
                "활을 쏜다",
                "오크에게 화살을 쏜다",
                "석궁으로 발사한다",
                "단검을 던진다",
                "창을 투척한다",
                "화살을 날린다",
                "적에게 화살을 쏜다",
                "멀리서 활을 당긴다",
                "표적을 향해 투척한다",
                "정확히 조준해서 쏜다",
                "먼 거리에서 활시위를 당긴다",
                "움직이는 표적을 향해 쏜다",
                "도끼를 던져 공격한다",
                "화살을 연속으로 발사한다",
                "수리검을 던진다",
                "장거리에서 쏜다",
            ],
            "defy_danger": [
                "불덩이를 피한다",
                "함정을 뛰어넘는다",
                "절벽을 기어오른다",
                "적에게서 달아난다",
                "공격을 굴러서 피한다",
                "독가스를 버틴다",
                "고통을 견딘다",
                "불길을 통과한다",
                "장애물을 넘어간다",
                "강을 건너간다",
                "화살 공격을 몸을 굴려 피한다",
                "무너지는 천장 아래에서 벗어난다",
                "떨어지는 바위를 재빠르게 피한다",
                "무너지는 다리를 건너 뛴다",
                "독을 의지로 견뎌낸다",
                "벼랑 끝에서 균형을 잡는다",
                "빠르게 달려 나간다",
                "질주해서 빠져나간다"
            ],
            "defend": [
                "동료를 지킨다",
                "방패로 막는다",
                "적의 공격을 방어한다",
                "약한 동료를 보호한다",
                "마법사를 지켜준다",
                "문을 가로막는다",
                "검으로 공격을 막아낸다",
                "몸으로 동료를 감싼다",
                "방패를 들어 지킨다",
                "적의 검격을 방패로 막아낸다",
                "동료 앞을 가로막고 선다",
                "화살 세례로부터 일행을 지킨다",
                "입구를 막아선다",
                "일행을 보호한다",
            ],
            "spout_lore": [
                "이 몬스터에 대해 기억한다",
                "고대 유물에 대해 안다",
                "이 장소에 대해 들어본 적이 있다",
                "옛날에 배운적이 있다",
                "그 전설을 알고있다",
                "이 문양을 아는 것 같다",
                "전에 본적이 있다",
                "책에서 읽은 내용을 기억한다",
                "드래곤의 약점을 알고있다",
                "이 유적에 대한 지식을 떠올린다",
                "과거에 들었던 전설을 기억해낸다",
                "고대 문자를 해독할 수 있다",
                "이 마법에 대해 아는 바가 있다",
                "역사책에서 본 적이 있다"
            ],
            "discern_realities": [
                "주변을 살핀다",
                "방을 조사한다",
                "함정이 있는지 확인한다",
                "천천히 둘러본다",
                "숨겨진 문을 찾는다",
                "시체를 뒤진다",
                "주의깊게 살펴본다",
                "적의 움직임을 관찰한다",
                "지형을 꼼꼼히 살핀다",
                "숨겨진 통로가 있는지 살핀다",
                "몬스터의 약점을 찾기 위해 관찰한다",
                "보물이 어디 있는지 뒤진다",
                "주변 환경을 조사한다",
                "단서를 찾아본다",
            ],
            "parley": [
                "적을 설득한다",
                "협상을 시도한다",
                "거래를 제안한다",
                "도움을 부탁한다",
                "오크와 대화한다",
                "상인에게 말을건다",
                "가격 인하를 요청한다",
                "평화적 해결을 제안한다",
                "정보를 얻기 위해 협상한다",
                "금화를 주고 정보를 얻으려 협상한다",
                "적에게 항복을 권유한다",
                "마을 사람들을 설득해 도움을 요청한다",
                "거래 조건을 제시한다",
                "회유한다",
            ],
            "aid_or_interfere": [
                "동료의 공격을 돕는다",
                "마법사의 주문을 거든다",
                "적의 행동을 방해한다",
                "오크의 공격을 막는다",
                "팀원과 협력한다",
                "치료를 지원한다",
                "적의 시야를 가린다",
                "친구의 공격이 성공하도록 돕는다",
                "적의 주의를 끌어 동료를 지원한다",
                "마법 의식을 방해하려 시도한다",
                "동료에게 힘을 보탠다",
                "적의 발목을 잡는다",
            ],
            "free_action": [
                "천천히 걷는다",
                "바닥에 앉는다",
                "상인에게 인사한다",
                "멀리 보이는 탑을 본다",
                "동료에게 말을 건넨다",
                "상냥하게 미소짓는다",
                "다음 행동을 기다린다",
                "문을 열고 들어간다",
                "물건을 집어든다",
                "복도를 따라 천천히 걷는다",
                "지도를 펼쳐본다",
                "모닥불 옆에 앉아 쉰다",
                "주위를 둘러본다",
                "물을 마신다",
            ]
        }
        
        # 2단계: 능력치 분류 (defy_danger용)
        self.stat_templates = {
            "STR": [
                "힘으로", "밀어붙인다", "부순다", "들어올린다",
                "밀친다", "끌어당긴다", "꺾는다"
            ],
            "CON": [
                "버틴다", "견딘다", "참는다", "이겨낸다",
                "저항한다", "끈기있게"
            ],
            "DEX": [
                "피한다", "재빠르게", "날렵하게", "민첩하게",
                "몸을피해", "굴러서", "뛰어서"
            ],
            "INT": [
                "생각해서", "계획을세워", "재치있게", "머리를써서",
                "꾀를부려", "지혜롭게", "계산해서"
            ],
            "WIS": [
                "집중해서", "침착하게", "의지로", "정신력으로",
                "마음을다잡고", "명상하듯"
            ],
            "CHA": [
                "말로", "설득해서", "매력으로", "카리스마로",
                "사교술로", "친근하게"
            ]
        }
        
        # 임베딩 계산
        self._compute_embeddings()

    def _compute_embeddings(self):
        """임베딩 미리 계산"""
        self.action_embeddings = {}
        for action, examples in self.action_templates.items():
            self.action_embeddings[action] = \
                self.model.encode(examples)
        
        self.stat_embeddings = {}
        for stat, examples in self.stat_templates.items():
            self.stat_embeddings[stat] = \
                self.model.encode(examples)

    def classify(self, player_input, context):
        """
        2단계 분류
        
        Returns:
            {
                "move": "defy_danger",
                "stat": "DEX",
                "confidence": 0.89
            }
        """
        # 1단계: 액션 분류
        action, action_conf = self._classify_action(player_input)
        
        # 확신도 낮으면 None
        if action_conf < 0.6:
            return None
        
        # 2단계: 능력치 분류 (defy_danger만)
        if action == "defy_danger":
            stat, stat_conf = self._classify_stat(
                player_input, 
                context
            )
        else:
            stat = self._get_default_stat(action)
            stat_conf = 1.0
        
        return {
            "move": action,
            "stat": stat,
            "player_input" : player_input,
            "confidence": min(action_conf, stat_conf)
        }

    def _classify_action(self, player_input):
        """액션 분류"""
        input_emb = self.model.encode(player_input)
        
        best_action = None
        best_score = 0
        
        for action, embeddings in self.action_embeddings.items():
            similarities = cosine_similarity(
                input_emb.reshape(1, -1),
                embeddings
            )
            max_sim = similarities.max()
            
            if max_sim > best_score:
                best_score = max_sim
                best_action = action
        
        return best_action, best_score

    def _classify_stat(self, player_input, context):
        """능력치 분류 (defy_danger용)"""
        input_emb = self.model.encode(player_input)
        
        best_stat = None
        best_score = 0
        
        for stat, embeddings in self.stat_embeddings.items():
            similarities = cosine_similarity(
                input_emb.reshape(1, -1),
                embeddings
            )
            max_sim = similarities.max()
            
            if max_sim > best_score:
                best_score = max_sim
                best_stat = stat
        
        # 확신도 낮으면 기본값 (DEX)
        if best_score < 0.4:
            best_stat = "DEX"
            best_score = 0.6
        
        return best_stat, best_score

    def _get_default_stat(self, action):
        """액션별 기본 능력치"""
        default_stats = {
            "hack_and_slash": "STR",
            "volley": "DEX",
            "defend": "CON",
            "spout_lore": "INT",
            "discern_realities": "WIS",
            "parley": "CHA",
            "aid_or_interfere": None,  # Bond 사용
            "free_action": None
        }
        return default_stats.get(action)