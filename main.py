import collections
import random
import pygame, sys
import cv2
import numpy as np
import autogui
pygame.init()

pygame.display.set_caption('menu game')
screen_menu = pygame.display.set_mode((1000, 600))
bg_menu = pygame.image.load('image/bg_menu.jpg')
scale_bg = pygame.transform.scale(bg_menu, (1000, 600))

font = pygame.font.Font('font_chu/ShortBaby-Mg2w.ttf',30)
def check_collision(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    rect1_tl = (x1, y1)
    rect1_br = (x1 + w1, y1 + h1)
    rect2_tl = (x2, y2)
    rect2_br = (x2 + w2, y2 + h2)
    if rect1_br[0] >= rect2_tl[0] and rect1_tl[0] <= rect2_br[0] and \
            rect1_br[1] >= rect2_tl[1] and rect1_tl[1] <= rect2_br[1]:
        return True
    return False
def game():
    pygame.display.set_caption('game')
    mang = 3
    diem = 0
    tocdo_chim = 1
    daix = 1000
    rongy = 600
    dai_chim = 170
    rong_chim = 170
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    # khai báo
    screen = pygame.display.set_mode((daix, rongy))
    clock = pygame.time.Clock()
    bg = pygame.image.load('image/bg.jpg')
    chim = pygame.image.load('image/chim.png')
    scale_chim = pygame.transform.scale(chim, (dai_chim, rong_chim))
    rec_chim = scale_chim.get_rect()
    rec_chim.centerx = random.randrange(0 + rong_chim, 1000 - dai_chim)
    rec_chim.centery = 600 + rong_chim
    cap = cv2.VideoCapture('1')
    while True:
        # sự kiện game
        ret, frame = cap.read()
        frame = cv2.resize(frame,(daix,rongy))
        cv2.imshow("cam", frame)
        frame = cv2.resize(frame, (daix, rongy))
        tl = [0, 0]
        bl = [0, 600]
        tr = [800, 0]
        br = [800, 600]
        pts1 = np.float32([tl, bl, tr, br])
        pts2 = np.float32([[0, 0], [0, rongy], [daix, 0], [daix, rongy]])
        maxtrix = cv2.getPerspectiveTransform(pts1, pts2)
        tran_frame = cv2.warpPerspective(frame, maxtrix, (daix, rongy))
        a, b, c = tran_frame.shape
        tran_frame = tran_frame[int(0.1 * a):a, 0:b]
        gray_fram = cv2.cvtColor(tran_frame, cv2.COLOR_BGR2GRAY)
        blur_frame = cv2.GaussianBlur(gray_fram, (5, 5), 5, 0)
        canny_frame = cv2.Canny(blur_frame, 50, 100)
        kernel = np.ones((5, 5), np.uint8)
        frame_1 = cv2.dilate(canny_frame, kernel)
        h, w = frame_1.shape
        imgControur = np.zeros((h, w, 3), np.uint8)
        contours, _ = cv2.findContours(frame_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area > 1000 and area < 100000:
                print(area)
                x, y, h, w = cv2.boundingRect(cnt)
                cv2.drawContours(imgControur, contours, i, (255, 0, 255), 2)
                collections.append((x, y, h, w))
        for i in range(len(collections)):
            for j in range(i + 1, len(collections)):
                rect1 = collections[i]
                rect2 = collections[j]
                if check_collision(rect1, rect2):
                    rec_chim.centery = 600 + rong_chim
                    rec_chim.centerx = random.randrange(0 + rong_chim, 1000 - dai_chim)
                    diem = diem + 1
                    tocdo_chim = tocdo_chim + 0.1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                chuot = pygame.mouse.get_pos()
                if rec_chim.collidepoint(chuot):
                    rec_chim.centery = 600 + rong_chim
                    rec_chim.centerx = random.randrange(0 + rong_chim, 1000 - dai_chim)
                    diem = diem + 1
                    tocdo_chim = tocdo_chim + 0.01
        # logic game
        if mang > 0:
            screen.blit(bg, (0, 0))
            screen.blit(scale_chim, rec_chim)
            rec_chim.centery = rec_chim.centery - tocdo_chim
            if rec_chim.centery <= -rong_chim:
                rec_chim.centery = 600 + rong_chim
                rec_chim.centerx = random.randrange(0 + rong_chim, 1000 - dai_chim)
                mang = mang - 1
            pygame.draw.rect(screen, BLACK, (0, 0, 250, 50), 2)
            txt_diem = font.render("Score: " + str(diem), True, BLACK)
            screen.blit(txt_diem, (10, 10))
            pygame.draw.rect(screen, (0, 0, 0), (daix - 200, 0, 200, 50), 2)
            txt_mang = font.render("Heart: " + str(mang), True, BLACK)
            screen.blit(txt_mang, (daix - 190, 10))

        if mang <= 0:
            break
        pygame.display.update()
    cap.release()
    cv2.destroyAllWindows()
button_play = pygame.draw.rect(screen_menu, (0, 0, 0), (0, 0, 200, 50))
txt_play = font.render("Play", True, (255, 255, 255))
play_rect = txt_play.get_rect()
play_rect.center = button_play.center
button_exit = pygame.draw.rect(screen_menu, (0, 0, 0), (0, 100, 200, 50))
txt_exit = font.render("Exit", True, (255, 255, 255))
exit_rect = txt_exit.get_rect()
exit_rect.center = button_exit.center
while True:
    screen_menu.blit(scale_bg, (0, 0))
    # nut choi
    screen_menu.blit(txt_play, play_rect)
    # nut thoat
    screen_menu.blit(txt_exit, (exit_rect))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            chuot = pygame.mouse.get_pos()
            if button_exit.collidepoint(chuot):
                pygame.quit()
                sys.exit()
            if button_play.collidepoint(chuot):
                game()