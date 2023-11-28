import random
import sys
import pygame as pg

WIDTH, HEIGHT = 1600, 900


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()  # こうかとんSurfaceからRect 
    kk_rct.center = 900,400
    bb_img = pg.Surface((20,20))  # 爆弾用Surface 
    bb_img.set_colorkey((0,0,0))  # 黒部分を透明に 
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)  # 半径10の赤い円 
    bb_rct = bb_img.get_rect() # 爆弾Surfaceからrect抽出 
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    vx = +5 # 爆弾の速度 
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    delta = {
        pg.K_UP: (0,-5),
        pg.K_DOWN: (0,5),
        pg.K_LEFT: (-5,0),
        pg.K_RIGHT: (5,0)
    }


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        key_lst = pg.key.get_pressed()
        sum_mv = [0,0]
        for key,tpl in delta.items():
            if key_lst[key]:  # キーが押されたら 
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv[0],sum_mv[1])
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


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