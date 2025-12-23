import pygame
import random
import sys

# --- 1. 設定とクラス定義 ---

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE_GUIDE = (100, 100, 255) # 逃走ガイド用

class Unit:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack
        self.defense_power = defense
        self.is_defending = False 

    def is_alive(self):
        """生きているかどうかの判定"""
        return self.hp > 0

    def attack(self, target):
        """targetに対して攻撃し、ダメージ計算結果とメッセージを返す"""
        
        base_damage = self.attack_power - target.defense_power
        variance = random.randint(-3, 3) 
        damage = base_damage + variance

        if target.is_defending:
            damage = max(1, damage // 2) 
            
        if damage < 1:
            damage = 1

        target.hp -= damage
        if target.hp < 0:
            target.hp = 0

        target.is_defending = False

        return f"{self.name}の攻撃！ {target.name}に {damage} のダメージ！"

    def heal(self):
        """ランダムな量だけHPを回復し、メッセージを返す"""
        heal_amount = random.randint(self.max_hp // 10, self.max_hp // 5) 
        
        self.hp += heal_amount
        if self.hp > self.max_hp:
            heal_amount -= (self.hp - self.max_hp) 
            self.hp = self.max_hp
            
        self.is_defending = False
        
        return f"{self.name}は休憩した。HPが {heal_amount} 回復！"
    
    def defend(self):
        """防御状態に移行し、メッセージを返す"""
        self.is_defending = True 
        return f"{self.name}は身構えた！次のダメージを軽減する！"

# --- 2. Pygame初期化 ---
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("テキストバトル RPG")

# 日本語フォントの設定
font_name = pygame.font.match_font('meiryo', 'yu gothic', 'hiragino maru gothic pro')
font = pygame.font.Font(font_name, 24)

# --- 3. ゲームデータの準備 ---
hero = Unit(name="勇者", hp=100, attack=30, defense=10)
demon = Unit(name="魔王", hp=250, attack=25, defense=5)

# 戦闘ログ（画面に表示するテキストのリスト）
battle_logs = ["A: 攻撃, H: 回復, D: 防御, R: 逃げる を選択！"]

turn = "PLAYER" # どちらのターンか
game_over = False

# --- 4. メインループ ---
running = True
while running:
    screen.fill(BLACK) 

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        
        if event.type == pygame.KEYDOWN and not game_over:
            
            if turn == "PLAYER":
                # プレイヤーの行動選択
                
                # Aキーで攻撃 (Attack)
                if event.key == pygame.K_a:
                    msg = hero.attack(demon)
                    battle_logs.append(msg)
                    
                    if not demon.is_alive():
                        battle_logs.append("魔王を倒した！")
                        game_over = True
                    else:
                        turn = "ENEMY"
                        
                # Hキーで回復 (Heal)
                elif event.key == pygame.K_h:
                    msg = hero.heal()
                    battle_logs.append(msg)
                    turn = "ENEMY"

                # Dキーで防御 (Defend)
                elif event.key == pygame.K_d:
                    msg = hero.defend()
                    battle_logs.append(msg)
                    turn = "ENEMY"
                
                # --- Rキーで逃走 (Run) ---
                elif event.key == pygame.K_r:
                    # 逃走判定 (10% 成功)
                    if random.random() < 0.1: 
                        battle_logs.append("勇者は戦場から逃げ出した！")
                        game_over = True # 成功したらゲーム終了
                    else:
                        battle_logs.append("逃走に失敗した！")
                        turn = "ENEMY" # 失敗したら魔王のターンへ
            
    # --- ENEMYのターン処理 ---
    if turn == "ENEMY" and not game_over:
        
        action_performed = False
        while not action_performed:
            
            roll = random.randint(0, 99)
            
            # 魔王の行動ロジック（攻撃、回復、防御）
            if demon.hp < demon.max_hp / 2 and roll < 20: # 回復
                msg = demon.heal()
                action_performed = True
            elif roll >= 20 and roll < 30: # 防御
                msg = demon.defend()
                action_performed = True
            else: # 攻撃
                msg = demon.attack(hero)
                action_performed = True
        
        battle_logs.append(msg)

        # 敵の攻撃後の勇者の生存判定
        if not hero.is_alive():
            battle_logs.append("勇者は力尽きた...")
            game_over = True
        else:
            turn = "PLAYER" 
        
    # --- 描画処理 ---
    
    # 1. ステータス表示
    hero_status_color = GREEN if hero.is_defending else WHITE
    hero_text = font.render(f"{hero.name} HP: {hero.hp}/{hero.max_hp}" + (" (防御中)" if hero.is_defending else ""), True, hero_status_color)
    
    demon_status_color = (255, 100, 100) 
    if demon.is_defending:
         demon_status_color = (150, 50, 255) 
    
    demon_text = font.render(f"{demon.name} HP: {demon.hp}/{demon.max_hp}" + (" (防御中)" if demon.is_defending else ""), True, demon_status_color)
    screen.blit(hero_text, (50, 50))
    screen.blit(demon_text, (400, 50))

    # 2. ログの表示
    recent_logs = battle_logs[-5:] 
    
    y = 150
    for log in recent_logs:
        text_surface = font.render(log, True, WHITE)
        screen.blit(text_surface, (50, y))
        y += 40

    # 3. 操作ガイド
    if not game_over and turn == "PLAYER":
        guide_text = font.render("[A]: 攻撃 | [H]: 回復 | [D]: 防御 | [R]: 逃げる", True, BLUE_GUIDE)
        screen.blit(guide_text, (50, 400))
    elif not game_over and turn == "ENEMY":
        guide_text = font.render("... 魔王の行動中 ...", True, RED)
        screen.blit(guide_text, (200, 400))
    elif game_over:
        guide_text = font.render("ゲーム終了。閉じるボタンで終了してください。", True, WHITE)
        screen.blit(guide_text, (100, 400))

    pygame.display.flip()

pygame.quit()
sys.exit()