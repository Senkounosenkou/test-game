import pygame  # Pygameライブラリのインポート
import sys     # システム終了用
import random  # ランダム処理用
from setting import*  # 設定ファイルから定数などをインポート
from player import*   # プレイヤークラスをインポート
from alien import*    # エイリアンクラスをインポート


# メインループ
def main():
    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode((600, 600))  # 画面サイズ設定
    pygame.display.set_caption("Space Invaders")  # ウィンドウタイトル設定
    font = pygame.font.SysFont(None, 55)  # フォント設定
    all_sprites = pygame.sprite.Group()  # 全スプライト管理グループ
    aliens = pygame.sprite.Group()       # エイリアン管理グループ
    bullets = pygame.sprite.Group()      # プレイヤー弾管理グループ
    alien_bullets = pygame.sprite.Group()# エイリアン弾管理グループ
    player = Player()                    # プレイヤーインスタンス生成
    all_sprites.add(player)              # プレイヤーを全スプライトに追加
    score = 0                            # スコア初期化
    running = True                       # ゲームループ継続フラグ
    game_over = False                    # ゲームオーバーフラグ
    game_clear = False                   # ゲームクリアフラグ
    game_started = False                 # ゲーム開始フラグ
    gameplay_sound_played = False        # ゲームプレイBGMが再生済みかどうかのフラグ
    shoot_sound = pygame.mixer.Sound(SHOOT_SOUND_PATH)  # プレイヤー弾発射音の読み込み
    hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH)      # エイリアン撃破音の読み込み
    clear_sound = pygame.mixer.Sound(CLEAR_SOUND_PATH)  # ゲームクリア時の効果音の読み込み
    gameover_sound = pygame.mixer.Sound(GAMEOVER_SOUND_PATH)  # ゲームオーバー時の効果音の読み込み
    gameplay_sound = pygame.mixer.Sound(GAMEPLAY_SOUND_PATH)  # ゲームプレイBGMの読み込み
    
    shoot_sound.set_volume(0.2)  # 弾発射音の音量を調整
    hit_sound.set_volume(0.2)    # ヒット音の音量を調整
    for i in range(10):  # 横方向に10体のエイリアンを配置
        for j in range(3):  # 縦方向に3列のエイリアンを配置
            alien = Alien(50 + i * 50, 70 + j * 80, all_sprites, alien_bullets)  # エイリアンインスタンス生成（座標・グループ指定）
            all_sprites.add(alien)  # 全スプライトグループにエイリアンを追加
            aliens.add(alien)       # エイリアングループにも追加

    while running:  # ゲームループ開始
        if not gameplay_sound_played and not game_over and not game_clear and game_started:
            gameplay_sound.play(-1)  # ゲームプレイBGMをループ再生
            gameplay_sound_played = True  # 再生済みフラグを立てる

        for event in pygame.event.get():  # イベント（キー入力やウィンドウ操作）を取得
            if event.type == pygame.QUIT:  # ウィンドウの×ボタンが押された場合
                running = False           # ゲームループ終了
            elif event.type == pygame.KEYDOWN:  # キーが押された場合
                if event.key == pygame.K_SPACE and not game_over:  # スペースキーで弾発射（ゲームオーバーでないとき）
                    shoot_sound.play()  # 弾発射音を再生
                    bullet = Bullet(player.rect.centerx, player.rect.top)  # 弾インスタンス生成
                    all_sprites.add(bullet)  # 弾を全スプライトに追加
                    bullets.add(bullet)      # 弾を弾グループに追加
                if event.key == pygame.K_s:  # Sキーでゲーム開始
                    game_started = True
                if game_over and event.key == pygame.K_r:  # Rキーでリスタート（ゲームオーバー時）
                    main()  # main関数を再呼び出し（再スタート）

        if not game_over and game_started:  # ゲーム中かつ開始済みの場合
            all_sprites.update()  # 全スプライトの状態を更新
            hits = pygame.sprite.groupcollide(bullets, aliens, True, True)  # プレイヤーの弾とエイリアンの衝突判定（両方消す）
            if hits:  # 衝突があった場合
                hit_sound.play()  # エイリアン撃破音を再生
                score += 10  # スコアを加算
            player_hits = pygame.sprite.spritecollide(player, alien_bullets, True)  # プレイヤーとエイリアン弾の衝突判定（弾を消す）
            if player_hits:  # 衝突があった場合
                gameover_sound.play()  # ゲームオーバー音を再生
                game_over = True  # ゲームオーバーフラグを立てる
            for alien in aliens:  # 全エイリアンについて
                if alien.rect.bottom >= player.rect.top:  # エイリアンがプレイヤーの位置まで到達したか判定
                    gameover_sound.play()  # ゲームオーバー音を再生
                    game_over = True  # ゲームオーバーフラグを立てる
            if not aliens and not game_clear:  # エイリアンが全滅し、まだクリアしていない場合
                clear_sound.play()  # クリア音を再生
                game_clear = True  # ゲームクリアフラグを立てる

        screen.fill(DARK_GREEN)  # 画面をダークグリーンで塗りつぶす
        all_sprites.draw(screen)  # 全スプライトを画面に描画
        score_text = font.render(f"Score: {score}", True, WHITE)  # スコア表示用テキストを作成
        screen.blit(score_text, (10, 10))  # スコアを画面左上に描画
        if game_over:  # ゲームオーバー時の処理
            gameplay_sound.stop()  # ゲームプレイBGMを停止
            game_over_text = font.render("GAME OVER - Press 'R' to Restart", True, WHITE)  # ゲームオーバーテキスト作成
            screen.blit(game_over_text, (150, 250))  # ゲームオーバーテキストを画面に描画
            all_sprites.empty()  # 全スプライトをクリア
            aliens.empty()       # エイリアングループをクリア
            bullets.empty()      # 弾グループをクリア
            alien_bullets.empty()# エイリアン弾グループをクリア
        if game_clear:  # ゲームクリア時の処理
            gameplay_sound.stop()  # ゲームプレイBGMを停止
            game_clear_text = font.render("GAME CLEAR", True, WHITE)  # ゲームクリアテキスト作成
            # ゲームクリアテキストを画面中央に配置するためにテキストサイズを取得し、中央座標を計算
            text_rect = game_clear_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(game_clear_text, text_rect)  # ゲームクリアテキストを画面中央に描画
            all_sprites.empty()  # 全スプライトをクリア
            aliens.empty()       # エイリアングループをクリア
            bullets.empty()      # 弾グループをクリア
            alien_bullets.empty()# エイリアン弾グループをクリア

        pygame.display.flip()  # 画面更新
        pygame.time.Clock().tick(60)  # フレームレートを60FPSに固定

    pygame.quit()  # Pygameの終了処理
    sys.exit()     # プログラム終了

if __name__ == "__main__":  # このファイルが直接実行された場合
    main()  # main関数を実行