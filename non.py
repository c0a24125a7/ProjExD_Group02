import pygame
import random
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# --- 1. 設定とクラス定義 ---

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 100, 100)

pygame.mixer.init()
snd = pygame.mixer.Sound("./ccs.wav")
pygame.mixer.music.load("./future.mp3")
pygame.mixer.music.play(-1)


class Unit:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack
        self.defense_power = defense

    def is_alive(self):
        """生きているかどうかの判定"""
        return self.hp > 0

    def attack(self, target):
        """targetに対して攻撃し、ダメージ計算結果とメッセージを返す"""
        
        # ダメージ計算式： (自分の攻撃力 - 相手の防御力) + 乱数(-3〜+3)
        base_damage = self.attack_power - target.defense_power
        variance = random.randint(-3, 3) 
        damage = base_damage + variance

        # ダメージは最低でも1入るようにする（0やマイナスを防ぐ）
        if damage < 1:
            damage = 1

        # 相手のHPを減らす
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0

        # 攻撃音を再生
        snd.play()
        # ログ用のメッセージを作成して返す
        return f"{self.name}の攻撃！ {target.name}に {damage} のダメージ！"

# --- 2. Pygame初期化 ---
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("テキストバトル RPG")

# 日本語フォントの設定（環境に合わせてフォントを探します）
font_name = pygame.font.match_font('meiryo', 'yu gothic', 'hiragino maru gothic pro')
font = pygame.font.Font(font_name, 24)

# --- 3. ゲームデータの準備 ---
hero = Unit(name="勇者", hp=100, attack=30, defense=10)
demon = Unit(name="魔王", hp=250, attack=25, defense=5)

# 戦闘ログ（画面に表示するテキストのリスト）
battle_logs = ["スペースキーを押してバトル開始！"]

turn = "PLAYER" # どちらのターンか
game_over = False

# --- 4. メインループ ---
# モード管理：選択中(SELECT) と バトル中(BATTLE)
stage = None
mode = 'SELECT'  # 'SELECT' or 'BATTLE'

# 戦闘ログを初期化（ステージ選択を促す）
battle_logs = ["1/2/3キーでステージを選択してください。"]

running = True
while running:
    screen.fill(BLACK) # 画面をリセット

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # ステージ選択モード
        if mode == 'SELECT':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    stage = 1
                    # ステージ1の敵ステータス
                    demon.max_hp = 150
                    demon.hp = demon.max_hp
                    demon.attack_power = 20
                    demon.defense_power = 5
                    hero.hp = hero.max_hp  # ヒーローを回復して開始
                    battle_logs.append("ステージ1を選択しました（易しい）")
                    mode = 'BATTLE'
                elif event.key == pygame.K_2:
                    stage = 2
                    demon.max_hp = 250
                    demon.hp = demon.max_hp
                    demon.attack_power = 25
                    demon.defense_power = 10
                    hero.hp = hero.max_hp
                    battle_logs.append("ステージ2を選択しました（普通）")
                    mode = 'BATTLE'
                elif event.key == pygame.K_3:
                    stage = 3
                    demon.max_hp = 400
                    demon.hp = demon.max_hp
                    demon.attack_power = 35
                    demon.defense_power = 15
                    hero.hp = hero.max_hp
                    battle_logs.append("ステージ3を選択しました（難しい）")
                    mode = 'BATTLE'

        # バトルモード
        elif mode == 'BATTLE':
            # スペースキーが押されたらターンを進める
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not game_over:
                    if turn == "PLAYER":
                        # 勇者の攻撃処理
                        msg = hero.attack(demon)
                        battle_logs.append(msg) # ログに追加

                        if not demon.is_alive():
                            battle_logs.append("魔王を倒した！")
                            game_over = True
                        else:
                            turn = "ENEMY" # 相手のターンへ

                    elif turn == "ENEMY":
                        # 魔王の攻撃処理
                        msg = demon.attack(hero)
                        battle_logs.append(msg)

                        if not hero.is_alive():
                            battle_logs.append("勇者は力尽きた...")
                            game_over = True
                        else:
                            turn = "PLAYER" # プレイヤーのターンへ
                else:
                    # ゲームオーバー後の案内（再選択できるようにする）
                    battle_logs.append("ゲーム終了。Rキーで最初に戻り、ステージ選択")
            # ゲームオーバー後にRでリトライ（ステージ選択に戻る）
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                mode = 'SELECT'
                game_over = False
                turn = 'PLAYER'
                battle_logs.append("ステージ選択に戻りました。1/2/3キーで選んでください。")

    # --- 描画処理 ---
    
    # 1. ヘッダー/モード表示
    if mode == 'SELECT':
        title_text = font.render("ステージ選択: 1=易 2=普 3=難", True, RED)
        screen.blit(title_text, (20, 20))

        # 選択肢の説明
        info1 = font.render("1: 魔王(HP150, 攻20, 防5)", True, WHITE)
        info2 = font.render("2: 魔王(HP250, 攻25, 防10)", True, WHITE)
        info3 = font.render("3: 魔王(HP400, 攻35, 防15)", True, WHITE)
        screen.blit(info1, (50, 80))
        screen.blit(info2, (50, 120))
        screen.blit(info3, (50, 160))

    else: # BATTLE
        hero_text = font.render(f"{hero.name} HP: {hero.hp}/{hero.max_hp}", True, WHITE)
        demon_text = font.render(f"{demon.name} HP: {demon.hp}/{demon.max_hp}", True, RED)
        stage_text = font.render(f"STAGE: {stage}", True, RED)
        screen.blit(hero_text, (50, 50))
        screen.blit(demon_text, (400, 50))
        screen.blit(stage_text, (250, 20))

    # 2. ログの表示（最新の5行だけ表示する）
    recent_logs = battle_logs[-5:]
    y = 260 if mode == 'SELECT' else 150 # 選択画面は下寄せで表示
    for log in recent_logs:
        text_surface = font.render(log, True, WHITE)
        screen.blit(text_surface, (50, y))
        y += 40 # 行間をあける

    # 3. 操作ガイド
    if mode == 'BATTLE' and not game_over:
        guide_text = font.render("[SPACE]でターンを進める", True, (100, 255, 100))
        screen.blit(guide_text, (200, 400))
    elif mode == 'BATTLE' and game_over:
        guide_text = font.render("Rでステージ選択に戻る", True, (255, 200, 100))
        screen.blit(guide_text, (200, 400))

    pygame.display.flip()

pygame.quit()
sys.exit()