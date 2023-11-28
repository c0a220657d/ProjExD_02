import random
import sys
import pygame as pg

WIDTH, HEIGHT = 1600, 900
delta = {
        pg.K_UP: (0,-5),
        pg.K_DOWN: (0,5),
        pg.K_LEFT: (-5,0),
        pg.K_RIGHT: (5,0)
    }
kk_rot = {  # こうかとんの向き(移動量):(角度,反転)
        (0,-5):(-90,True),
        (5,-5):(-45,True),
        (5,0):(0,True),
        (5,5):(45,True),
        (0,5):(90,True),
        (-5,5):(45,False),
        (-5,0):(0,False),
        (-5,-5):(-45,False),
        (0,0):None
    }
accs = [i for i in range(1,11)]

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_out = kk_img  # こうかとん初期画像 
    kk_rct = kk_img_out.get_rect()  # こうかとんSurfaceからRect 
    kk_rct.center = 900,400
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))  # 黒部分を透明に 
        bb_imgs.append(bb_img)
    bb_rct = bb_imgs[0].get_rect()
    bbpos_x = random.randint(0,WIDTH)  # 爆弾の中心座標
    bbpos_y = random.randint(0,HEIGHT)
    bb_rct.centerx = bbpos_x  # 初期座標設定 
    bb_rct.centery = bbpos_y
    bb_rct_now = bb_rct
    accs = [i for i in range(1,11)] 
    vx = +5 # 爆弾の速度 
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct_now):
            print("Game Over")
            kk_img = pg.image.load("ex02/fig/8.png")
            kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img,kk_rct)
            pg.display.update()
            pg.time.wait(600)
            return
        
        avx,avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct_now = bb_img.get_rect()  # 爆弾Surfaceからrect抽出 
        bb_rct_now.centerx = bbpos_x  #中心座標適用
        bb_rct_now.centery = bbpos_y
        key_lst = pg.key.get_pressed()
        sum_mv = [0,0]
        for key,tpl in delta.items():
            if key_lst[key]:  # キーが押されたら 
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rotval = kk_rot[(sum_mv[0],sum_mv[1])]
        if kk_rotval is not None:
            kk_img_out = pg.transform.flip(pg.transform.rotozoom(kk_img, kk_rotval[0], 1.0),kk_rotval[1],False)  # kk_rotvalから回転量、反転を取得、反映
        kk_rct.move_ip(sum_mv[0],sum_mv[1])
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img_out, kk_rct)
        bb_rct_now.move_ip(avx,avy)
        yoko,tate = check_bound(bb_rct_now)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img,bb_rct_now)
        bbpos_x = bb_rct_now.centerx  # 中心座標の更新
        bbpos_y = bb_rct_now.centery
        pg.display.update()
        tmr += 1
        clock.tick(100)


def check_bound(rct:pg.Rect) -> tuple:
    """
    オブジェクトが画面内or画面外を判定、bool値tupleで返す
    引数 rct:判定したいオブジェクトのRect
    return (横方向,縦方向) 画面内True,画面外False
    """
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()