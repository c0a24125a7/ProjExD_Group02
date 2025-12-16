import pygame
import random
import sys

# --- 1. 設定とクラス定義 ---

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
GREEN = (100, 255, 100) # 回復や防御のガイド用

class Unit:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack
        self.defense_power = defense
        self.is_defending = False # 防御状態フラグを追加

    def is_alive(self):
        """生きているかどうかの判定"""
        return self.hp > 0

    def attack(self, target):
        """targetに対して攻撃し、ダメージ計算結果とメッセージを返す"""
        
        # ダメージ計算式： (自分の攻撃力 - 相手の防御力) + 乱数(-3〜+3)
        base_damage = self.attack_power - target.defense_power
        variance = random.randint(-3, 3) 
        damage = base_damage + variance

        # **防御状態のターゲットへのダメージ軽減**
        if target.is_defending:
            damage = max(1, damage // 2) # ダメージを半減し、最低1は保証
            
        # ダメージは最低でも1入るようにする（0やマイナスを防ぐ）
        if damage < 1:
            damage = 1

        # 相手のHPを減らす
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0

        # 防御フラグをリセット（防御は1ターンのみ有効）
        target.is_defending = False

        # ログ用のメッセージを作成して返す
        return f"{self.name}の攻撃！ {target.name}に {damage} のダメージ！"

    # --- 回復処理 ---
    def heal(self):
        """ランダムな量だけHPを回復し、メッセージを返す"""
        heal_amount = random.randint(self.max_hp // 10, self.max_hp // 5) 
        
        self.hp += heal_amount
        if self.hp > self.max_hp:
            heal_amount -= (self.hp - self.max_hp) 
            self.hp = self.max_hp
            
        self.is_defending = False
        
        return f"{self.name}は休憩した。HPが {heal_amount} 回復！"
    
    # --- 防御処理 ---
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
battle_logs = ["A: 攻撃, H: 回復, D: 防御 を選択！"]

turn = "PLAYER" # どちらのターンか
game_over = False

# --- 4. メインループ ---
running = True
while running:
    screen.fill(BLACK) # 画面をリセット

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        
        # キーが押されたらターンを進める/アクションを実行する
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
                        turn = "ENEMY" # 相手のターンへ
                        
                # Hキーで回復 (Heal)
                elif event.key == pygame.K_h:
                    msg = hero.heal()
                    battle_logs.append(msg)
                    turn = "ENEMY" # 相手のターンへ

                # Dキーで防御 (Defend)
                elif event.key == pygame.K_d:
                    msg = hero.defend()
                    battle_logs.append(msg)
                    turn = "ENEMY" # 相手のターンへ
            
    # --- ENEMYのターン処理 ---
    # プレイヤーの行動選択後、ターンがENEMYに切り替わったら自動で行動する
    if turn == "ENEMY" and not game_over:
        
        action_performed = False
        while not action_performed:
            
            # 0から99の乱数を生成
            roll = random.randint(0, 99)
            
            # 魔王の行動ロジック
            
            # 1. 回復 (HPが半分以下 and 20%の確率)
            if demon.hp < demon.max_hp / 2 and roll < 20:
                msg = demon.heal()
                action_performed = True
                
            # 2. 防御 (20%以上 and 10%の確率) - (100% - 70% - 20% = 10% だったが、回復条件があるため20~30%あたりに設定)
            # ここではシンプルに roll が 20から30未満なら防御 (10%の確率)
            elif roll >= 20 and roll < 30: 
                msg = demon.defend()
                action_performed = True
                
            # 3. 攻撃 (それ以外、または優先行動ができなかった場合)
            else:
                msg = demon.attack(hero)
                action_performed = True
        
        # ログに追加
        battle_logs.append(msg)

        # 次のターンの判定
        if not hero.is_alive():
            battle_logs.append("勇者は力尽きた...")
            game_over = True
        else:
            turn = "PLAYER" # プレイヤーのターンへ
        
    # --- 描画処理 ---
    
    # 1. ステータス表示（画面上部）
    # 勇者の状態（防御中なら色を変えるなど）
    hero_status_color = GREEN if hero.is_defending else WHITE
    hero_text = font.render(f"{hero.name} HP: {hero.hp}/{hero.max_hp}" + (" (防御中)" if hero.is_defending else ""), True, hero_status_color)
    # 魔王の状態
    demon_status_color = (255, 100, 100) # 通常はRED
    if demon.is_defending:
         demon_status_color = (150, 50, 255) # 魔王の防御中は紫っぽい色
    
    demon_text = font.render(f"{demon.name} HP: {demon.hp}/{demon.max_hp}" + (" (防御中)" if demon.is_defending else ""), True, demon_status_color)
    screen.blit(hero_text, (50, 50))
    screen.blit(demon_text, (400, 50))

    # 2. ログの表示（最新の5行だけ表示する）
    recent_logs = battle_logs[-5:] 
    
    y = 150 # テキストを表示し始めるY座標
    for log in recent_logs:
        text_surface = font.render(log, True, WHITE)
        screen.blit(text_surface, (50, y))
        y += 40 # 行間をあける

    # 3. 操作ガイド
    if not game_over and turn == "PLAYER":
        guide_text = font.render("[A]: 攻撃 | [H]: 回復 | [D]: 防御", True, GREEN)
        screen.blit(guide_text, (150, 400))
    elif not game_over and turn == "ENEMY":
        guide_text = font.render("... 魔王の行動中 ...", True, RED)
        screen.blit(guide_text, (200, 400))
    elif game_over:
        guide_text = font.render("ゲーム終了。閉じるボタンで終了してください。", True, WHITE)
        screen.blit(guide_text, (100, 400))

    pygame.display.flip()

pygame.quit()
sys.exit()