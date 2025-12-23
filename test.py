# # import pygame
# # import random
# # import sys
# # import os
# # import time  # 追加
# # os.chdir(os.path.dirname(os.path.abspath(__file__)))
# # # --- 1. 設定とクラス定義 ---

# # # 色の定義
# # WHITE = (255, 255, 255)
# # BLACK = (0, 0, 0)
# # RED   = (255, 100, 100)

# # class Unit:
# #     def __init__(self, name, hp, attack, defense):
# #         self.name = name
# #         self.max_hp = hp
# #         self.hp = hp
# #         self.attack_power = attack
# #         self.defense_power = defense

# #     def is_alive(self):
# #         """生きているかどうかの判定"""
# #         return self.hp > 0

# #     def attack(self, target):
# #         """targetに対して攻撃し、ダメージ計算結果とメッセージを返す"""
        
# #         # ダメージ計算式： (自分の攻撃力 - 相手の防御力) + 乱数(-3〜+3)
# #         base_damage = self.attack_power - target.defense_power
# #         variance = random.randint(-3, 3) 
# #         damage = base_damage + variance

# #         # ダメージは最低でも1入るようにする（0やマイナスを防ぐ）
# #         if damage < 1:
# #             damage = 1

# #         # 相手のHPを減らす
# #         target.hp -= damage
# #         if target.hp < 0:
# #             target.hp = 0

# #         # ログ用のメッセージを作成して返す
# #         return f"{self.name}の攻撃！ {target.name}に {damage} のダメージ！"

# # # --- 2. Pygame初期化 ---
# # pygame.init()
# # screen = pygame.display.set_mode((640, 480))
# # pygame.display.set_caption("テキストバトル RPG")

# # # 背景画像のロード
# # bg_img = pygame.image.load("fig/nohara.jpg")
# # bg_img = pygame.transform.scale(bg_img, (640, 480))  # 画面サイズに合わせる
# # bg_img2 = pygame.image.load("fig/mori2.jpg")
# # bg_img2 = pygame.transform.scale(bg_img2, (640, 480))
# # bg_img3 = pygame.image.load("fig/maou.jpg")
# # bg_img3 = pygame.transform.scale(bg_img3, (640, 480)) 
# # # 日本語フォントの設定（ドラクエ風にMS Gothicを使用）
# # font_name = pygame.font.match_font('msgothic', 'meiryo', 'yu gothic')
# # font = pygame.font.Font(font_name, 20)
# # small_font = pygame.font.Font(font_name, 14)  # 小さいフォント

# # # --- 3. ゲームデータの準備関数 ---
# # def init_game():
# #     global hero, demon, battle_logs, turn, game_over, game_over_time
# #     hero = Unit(name="勇者", hp=100, attack=30, defense=10)
# #     demon = Unit(name="魔王", hp=250, attack=25, defense=5)
# #     battle_logs = ["スペースキーを押してバトル開始！"]
# #     turn = "PLAYER"
# #     game_over = False
# #     game_over_time = None

# # init_game()  # 初期化

# # # --- 4. メインループ ---
# # while True:
# #     # ゲームオーバー時は3秒後に終了
# #     if game_over and game_over_time and time.time() - game_over_time > 1:
# #         break

# #     screen.blit(bg_img3, [0, 0])  # 背景画像を描画

# #     # イベント処理
# #     for event in pygame.event.get():
# #         if event.type == pygame.QUIT:
# #             break
        
# #         # スペースキーが押されたらターンを進める
# #         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
# #             if not game_over:
# #                 if turn == "PLAYER":
# #                     # 勇者の攻撃処理
# #                     msg = hero.attack(demon)
# #                     battle_logs.append(msg) # ログに追加
                    
# #                     if not demon.is_alive():
# #                         battle_logs.append("魔王を倒した！")
# #                         game_over = True
# #                         game_over_time = time.time()
# #                     else:
# #                         turn = "ENEMY" # 相手のターンへ
                
# #                 elif turn == "ENEMY":
# #                     # 魔王の攻撃処理
# #                     msg = demon.attack(hero)
# #                     battle_logs.append(msg)
                    
# #                     if not hero.is_alive():
# #                         battle_logs.append("勇者は力尽きた...")
# #                         game_over = True
# #                         game_over_time = time.time()
# #                     else:
# #                         turn = "PLAYER" # プレイヤーのターンへ

# #     # --- 描画処理 ---
# #     if game_over:
# #         screen.fill(BLACK)  # ゲームオーバー時は黒背景
# #         # ゲームオーバー画面
# #         gameover_text = font.render("GAME OVER", True, RED)
# #         screen.blit(gameover_text, (250, 200))
# #     else:
# #         screen.blit(bg_img3, [0, 0])  # 通常時は背景画像
# #         # 通常の描画
# #         # 1. ステータス表示（画面上部）
# #         hero_text = font.render(f"{hero.name} HP: {hero.hp}/{hero.max_hp}", True, WHITE)
# #         demon_text = font.render(f"{demon.name} HP: {demon.hp}/{demon.max_hp}", True, RED)
# #         screen.blit(hero_text, (50, 50))
# #         screen.blit(demon_text, (400, 50))

# #         # 2. ログの表示（ドラクエ風ウィンドウ内、画面下部）
# #         # ウィンドウの背景と枠を描画
# #         window_rect = pygame.Rect(50, 250, 540, 200)  # 下部に移動
# #         pygame.draw.rect(screen, BLACK, window_rect)  # 背景黒
# #         pygame.draw.rect(screen, WHITE, window_rect, 2)  # 白い枠
        
# #         # 最新の5行を表示
# #         recent_logs = battle_logs[-5:]
# #         y = 270  # ウィンドウ内の開始Y座標
# #         for log in recent_logs:
# #             text_surface = font.render(log, True, WHITE)
# #             screen.blit(text_surface, (70, y))
# #             y += 35  # 行間

# #         # 3. 操作ガイド（右下に小さく表示）
# #         guide_text = small_font.render("[SPACE]でターンを進める", True, (100, 255, 100))
# #         screen.blit(guide_text, (450, 450))  # 右下に移動

# #     pygame.display.flip()

# # if __name__ == "__main__":
# #     pygame.init()
# #     pygame.quit()
# #     sys.exit()

# import pygame
# import random
# import sys
# import os
# import time

# # 絶対パスを取得し、カレントディレクトリを変更
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# # --- 1. 設定とクラス定義 ---

# # 色の定義
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 100, 100)
# GREEN = (100, 255, 100) # 操作ガイドの色

# class Unit:
#     def __init__(self, name, hp, attack, defense):
#         self.name = name
#         self.max_hp = hp
#         self.hp = hp
#         self.attack_power = attack
#         self.defense_power = defense

#     def is_alive(self):
#         """生きているかどうかの判定"""
#         return self.hp > 0

#     def attack(self, target):
#         """targetに対して攻撃し、ダメージ計算結果とメッセージを返す"""
        
#         # ダメージ計算式： (自分の攻撃力 - 相手の防御力) + 乱数(-3〜+3)
#         base_damage = self.attack_power - target.defense_power
#         variance = random.randint(-3, 3) 
#         damage = base_damage + variance

#         # ダメージは最低でも1入るようにする（0やマイナスを防ぐ）
#         if damage < 1:
#             damage = 1

#         # 相手のHPを減らす
#         target.hp -= damage
#         if target.hp < 0:
#             target.hp = 0

#         # ログ用のメッセージを作成して返す
#         return f"{self.name}の攻撃！ {target.name}に {damage} のダメージ！"

# # --- 2. Pygame初期化 ---
# pygame.init()
# screen = pygame.display.set_mode((640, 480))
# pygame.display.set_caption("テキストバトル RPG")

# # **背景画像データの準備**
# # ファイル名リスト。ステージ1: nohara.jpg, ステージ2: mori2.jpg, ステージ3: maou.jpg
# bg_file_names = ["fig/nohara.jpg", "fig/mori2.jpg", "fig/maou.jpg"]
# bg_images = []
# for file_name in bg_file_names:
#     try:
#         img = pygame.image.load(file_name)
#         img = pygame.transform.scale(img, (640, 480)) # 画面サイズに合わせる
#         bg_images.append(img)
#     except pygame.error as e:
#         print(f"背景画像のロードに失敗しました: {file_name}")
#         # ロード失敗時はダミーの真っ黒な画像を追加
#         dummy_surface = pygame.Surface((640, 480))
#         dummy_surface.fill(BLACK)
#         bg_images.append(dummy_surface)
        
# # **ステージの総数**
# MAX_STAGE = len(bg_images)

# # 日本語フォントの設定（ドラクエ風にMS Gothicを使用）
# font_name = pygame.font.match_font('msgothic', 'meiryo', 'yu gothic')
# font = pygame.font.Font(font_name, 20)
# small_font = pygame.font.Font(font_name, 14) # 小さいフォント

# # --- 3. ゲームデータの準備関数 ---
# def init_game(stage=1):
#     """
#     ゲームデータを初期化する。ステージレベルに応じて敵のステータスを変更。
#     :param stage: 開始するステージのレベル (1, 2, 3...)
#     """
#     global hero, demon, battle_logs, turn, game_over, game_clear, game_over_time, stage_level
    
#     stage_level = stage
#     game_over = False
#     game_clear = False
#     game_over_time = None
    
#     # 勇者は固定
#     hero = Unit(name="勇者", hp=100, attack=30, defense=10)
    
#     # ステージレベルに応じた魔王（敵）のステータス設定
#     if stage_level == 1:
#         demon = Unit(name="スライム魔王", hp=30, attack=10, defense=5)
#         battle_logs = [f"ステージ {stage_level}：{demon.name} が現れた！", "スペースキーを押してバトル開始！"]
#     elif stage_level == 2:
#         demon = Unit(name="ドラゴン魔王", hp=100, attack=20, defense=8)
#         battle_logs = [f"ステージ {stage_level}：{demon.name} が現れた！", "スペースキーを押してバトル開始！"]
#     elif stage_level == 3:
#         demon = Unit(name="真の魔王", hp=250, attack=30, defense=10)
#         battle_logs = [f"ステージ {stage_level}：{demon.name} が現れた！", "スペースキーを押してバトル開始！"]
#     else:
#         # 予期せぬステージレベルの場合は終了処理へ
#         game_clear = True
#         game_over = True
#         battle_logs = ["すべての魔王を打ち破った！"]


#     turn = "PLAYER"

# # 最初の初期化（ステージ1から開始）
# init_game(stage=1)

# # --- 4. メインループ ---
# while True:
#     # ゲームオーバー/ゲームクリア時は3秒後に終了
#     if (game_over or game_clear) and game_over_time and time.time() - game_over_time > 3:
#         # 全ステージクリア時はここでブレイクしない
#         if stage_level > MAX_STAGE or not hero.is_alive():
#             break
        
#         # ステージクリアで次のステージがある場合
#         if stage_level < MAX_STAGE and hero.is_alive():
#             init_game(stage=stage_level + 1)
#             continue # ループの最初に戻って新しいステージを開始

#     # イベント処理
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
        
#         # スペースキーが押されたらターンを進める
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#             # ゲームオーバーやステージクリア判定後、次のステージへの移行中は操作を受け付けない
#             if not game_over and not game_clear:
                
#                 if turn == "PLAYER":
#                     # 勇者の攻撃処理
#                     msg = hero.attack(demon)
#                     battle_logs.append(msg) # ログに追加
                    
#                     if not demon.is_alive():
#                         battle_logs.append(f"ステージ {stage_level} の魔王を倒した！")
#                         # 最終ステージでなければステージクリア
#                         if stage_level < MAX_STAGE:
#                             battle_logs.append(f"ステージ {stage_level+1} へ進む準備中...")
#                             game_clear = True
#                         else:
#                             battle_logs.append("すべての魔王を打ち破った！勇者の勝利！")
#                             game_clear = True
                        
#                         game_over = True # ステージクリアも一旦 game_over=True で時間経過を制御
#                         game_over_time = time.time()
#                     else:
#                         turn = "ENEMY" # 相手のターンへ
                
#                 elif turn == "ENEMY":
#                     # 魔王の攻撃処理
#                     msg = demon.attack(hero)
#                     battle_logs.append(msg)
                    
#                     if not hero.is_alive():
#                         battle_logs.append("勇者は力尽きた...")
#                         game_over = True
#                         game_over_time = time.time()
#                     else:
#                         turn = "PLAYER" # プレイヤーのターンへ

#     # --- 描画処理 ---
#     screen.fill(BLACK) # 背景を一旦黒でクリア
    
#     # 描画する背景画像を選択（リストのインデックスは stage_level - 1）
#     if 1 <= stage_level <= MAX_STAGE:
#         screen.blit(bg_images[stage_level - 1], [0, 0])
    
#     if game_over and not hero.is_alive():
#         # 勇者が負けた場合
#         # ゲームオーバー画面
#         gameover_text = font.render("GAME OVER", True, RED)
#         screen.blit(gameover_text, (250, 200))
#         # ログ表示ウィンドウはそのまま残す
        
#     elif game_clear:
#         # 勇者が勝った場合（最終ステージクリア、または次のステージへの移行待ち）
#         if stage_level >= MAX_STAGE:
#             # 完全勝利
#             clear_text = font.render("全ステージクリア！", True, GREEN)
#             screen.blit(clear_text, (230, 200))
#         else:
#             # ステージクリア
#             clear_text = font.render(f"ステージ {stage_level} CLEAR！", True, GREEN)
#             screen.blit(clear_text, (230, 200))
#             next_text = small_font.render(f"ステージ {stage_level+1} へ...", True, WHITE)
#             screen.blit(next_text, (260, 250))
        
#     else:
#         # 通常の描画
#         # 1. ステータス表示（画面上部）
#         hero_text = font.render(f"{hero.name} HP: {hero.hp}/{hero.max_hp}", True, WHITE)
#         demon_text = font.render(f"{demon.name} HP: {demon.hp}/{demon.max_hp}", True, RED)
#         stage_text = font.render(f"STAGE {stage_level}", True, WHITE)
#         screen.blit(hero_text, (50, 50))
#         screen.blit(demon_text, (400, 50))
#         screen.blit(stage_text, (280, 10))

#         # 2. ログの表示（ドラクエ風ウィンドウ内、画面下部）
#         # ウィンドウの背景と枠を描画
#         window_rect = pygame.Rect(50, 300, 540, 150) # サイズと位置を調整
#         pygame.draw.rect(screen, BLACK, window_rect) # 背景黒
#         pygame.draw.rect(screen, WHITE, window_rect, 2) # 白い枠
        
#         # 最新の4行を表示
#         recent_logs = battle_logs[-4:]
#         y = 310 # ウィンドウ内の開始Y座標
#         for log in recent_logs:
#             text_surface = font.render(log, True, WHITE)
#             screen.blit(text_surface, (70, y))
#             y += 30 # 行間

#         # 3. 操作ガイド（右下に小さく表示）
#         guide_text = small_font.render("[SPACE]でターンを進める", True, GREEN)
#         screen.blit(guide_text, (450, 460)) # 右下に移動

#     pygame.display.flip()

# # メインループ終了後の処理
# pygame.quit()
# sys.exit()

import pygame
import random
import sys
import os
import time

# 絶対パスを取得し、カレントディレクトリを変更
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass

# --- 1. 設定とクラス定義 ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
GOLD = (255, 215, 0)

pygame.init()
pygame.mixer.init()

# 音声ファイルの読み込み（ファイルがない場合はスキップ）
def load_sound(file):
    try:
        return pygame.mixer.Sound(file)
    except:
        return None

snd_attack = load_sound("./ccs.wav")

def play_bgm(file):
    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)
    except:
        print(f"BGM {file} が見つかりません")

class Unit:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack
        self.defense_power = defense

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        base_damage = self.attack_power - target.defense_power
        variance = random.randint(-3, 3) 
        damage = max(1, base_damage + variance)
        target.hp = max(0, target.hp - damage)
        
        if snd_attack:
            snd_attack.play()
        return f"{self.name}の攻撃！ {target.name}に {damage} のダメージ！"

# --- 2. 画面とフォントの設定 ---
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("テキストバトル RPG 統合版")

font_name = pygame.font.match_font('msgothic', 'meiryo', 'yu gothic')
font = pygame.font.Font(font_name, 20)
small_font = pygame.font.Font(font_name, 14)
big_font = pygame.font.Font(font_name, 48)

# 背景画像の読み込み
bg_file_names = ["fig/nohara.jpg", "fig/mori2.jpg", "fig/maou.jpg"]
bg_images = []
for file_name in bg_file_names:
    try:
        img = pygame.image.load(file_name)
        img = pygame.transform.scale(img, (640, 480))
        bg_images.append(img)
    except:
        surf = pygame.Surface((640, 480))
        surf.fill((30, 30, 30))
        bg_images.append(surf)

# --- 3. ゲーム管理変数 ---
hero = Unit(name="勇者", hp=100, attack=30, defense=10)
demon = None
battle_logs = []
mode = 'SELECT' # 'SELECT', 'BATTLE', 'CLEAR'
turn = "PLAYER"
game_over = False
current_stage = 1
MAX_STAGE = 5

def init_battle(stage_num):
    global demon, mode, turn, game_over, current_stage, battle_logs
    current_stage = stage_num
    game_over = False
    turn = "PLAYER"
    mode = 'BATTLE'
    
    # ステージごとの敵設定
    if stage_num == 1:
        demon = Unit("スライム", 150, 15, 5)
    elif stage_num == 2:
        demon = Unit("ゴブリン", 250, 25, 10)
    elif stage_num == 3:
        demon = Unit("キメラ", 500, 40, 15)
    elif stage_num == 4:
        demon = Unit("ゴーレム", 1000, 60, 30)
    elif stage_num == 5:
        demon = Unit("魔王", 5000, 100, 50)
    
    battle_logs = [f"ステージ {stage_num}：{demon.name} が現れた！"]
    play_bgm("./honey.mp3")

# 初期状態
play_bgm("./future.mp3")
battle_logs = ["1-5キーでステージを選択してください。"]

# --- 4. メインループ ---
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            # --- ステージ選択モード ---
            if mode == 'SELECT':
                if event.key == pygame.K_1: init_battle(1)
                elif event.key == pygame.K_2: init_battle(2)
                elif event.key == pygame.K_3: init_battle(3)
                elif event.key == pygame.K_4: init_battle(4)
                elif event.key == pygame.K_5: init_battle(5)
            
            # --- バトルモード ---
            elif mode == 'BATTLE':
                if not game_over:
                    if event.key == pygame.K_SPACE:
                        if turn == "PLAYER":
                            msg = hero.attack(demon)
                            battle_logs.append(msg)
                            if not demon.is_alive():
                                battle_logs.append(f"{demon.name}を倒した！")
                                # 成長システム
                                hero.max_hp += 20
                                hero.hp = hero.max_hp
                                hero.attack_power += 5
                                hero.defense_power += 2
                                battle_logs.append("勇者のレベルが上がった！")
                                
                                if current_stage == 5:
                                    mode = 'CLEAR'
                                    play_bgm("./ccs.wav")
                                else:
                                    game_over = True # Rで戻るか次への待機
                            else:
                                turn = "ENEMY"
                        
                        elif turn == "ENEMY":
                            msg = demon.attack(hero)
                            battle_logs.append(msg)
                            if not hero.is_alive():
                                battle_logs.append("勇者は力尽きた...")
                                mode = "gameover"
                            else:
                                turn = "PLAYER"
                
                # ゲームオーバー/勝利後の操作
                if game_over and event.key == pygame.K_r:
                    mode = 'SELECT'
                    play_bgm("./future.mp3")
                    battle_logs.append("ステージ選択に戻りました。")

            # --- クリアモード ---
            elif mode == 'CLEAR':
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    running = False

    if mode == 'gameover':
        gameover_text = font.render("GAME OVER", True, RED)
        screen.blit(gameover_text, (250, 200))
        

    # --- 描画セクション ---
    if mode == 'SELECT':
        title = font.render("【 ステージ選択 】", True, RED)
        screen.blit(title, (20, 20))
        opts = [
            "1: スライム (Easy)",
            "2: ゴブリン (Normal)",
            "3: キメラ (Hard)",
            "4: ゴーレム (Very Hard)",
            "5: 魔王 (Hell)"
        ]
        for i, opt in enumerate(opts):
            screen.blit(font.render(opt, True, WHITE), (50, 80 + i*30))
        
        # 勇者の現在ステータス表示
        status = font.render(f"勇者 HP:{hero.max_hp} ATK:{hero.attack_power} DEF:{hero.defense_power}", True, GREEN)
        screen.blit(status, (50, 300))

    elif mode == 'BATTLE':
        # 背景（3ステージ目までは画像、それ以降は最後の画像）
        if current_stage==1:
            bg_idx = 0
        elif current_stage==2:
            bg_idx = 0
        elif current_stage==3:
            bg_idx = 1
        elif current_stage==4:
            bg_idx = 1
        else:
            bg_idx = 2
        screen.blit(bg_images[bg_idx], (0, 0))
        
        # ステータス表示
        pygame.draw.rect(screen, BLACK, (40, 40, 220, 40))
        pygame.draw.rect(screen, BLACK, (380, 40, 220, 40))
        hero_txt = font.render(f"{hero.name} HP: {hero.hp}/{hero.max_hp}", True, WHITE)
        demon_txt = font.render(f"{demon.name} HP: {demon.hp}/{demon.max_hp}", True, RED)
        screen.blit(hero_txt, (50, 50))
        screen.blit(demon_txt, (390, 50))
        
        # ログウィンドウ
        win_rect = pygame.Rect(50, 300, 540, 150)
        pygame.draw.rect(screen, BLACK, win_rect)
        pygame.draw.rect(screen, WHITE, win_rect, 2)
        
        recent_logs = battle_logs[-4:]
        for i, log in enumerate(recent_logs):
            screen.blit(font.render(log, True, WHITE), (70, 310 + i*30))
    

    elif mode == 'CLEAR':
        screen.fill(BLACK)
        txt = big_font.render("ALL STAGE CLEAR!", True, GOLD)
        sub = font.render("Good Morning, Hero... (Qで終了)", True, WHITE)
        screen.blit(txt, (txt.get_rect(center=(320, 200))))
        screen.blit(sub, (sub.get_rect(center=(320, 280))))

    pygame.display.flip()
    clock.tick(30)

    if mode == 'gameover':
        time.sleep(2)
        break

pygame.quit()
sys.exit()