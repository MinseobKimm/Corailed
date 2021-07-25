import cv2
import numpy as np
from colorama import init, Fore, Back, Style

from detection import axe, pickaxe, trees, player, rock, blackrock, river, terrain, green


def test(im, game):
    set_array_from_bin(game, im)

def set_array_from_bin(game, im):
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    bin_player = player.get_bin(im, im_hsv)
    arrplayer = element(game, bin_player, bin_player, 3)

    bin_green = green.get_bin(im, im_hsv)
    bin_trees = trees.get_bin(im, im_hsv)
    bin_rocks = rock.get_bin(im, im_hsv)
    bin_black = blackrock.get_bin(im, im_hsv)
    bin_river = river.get_bin(im, im_hsv)
    bin_terrain = terrain.get_bin(im, im_hsv)

    axe_pos = axe.get_axe_minimap(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    pickaxe_pos = pickaxe.get_axe_minimap(im,
                                          cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))

    arrtree = element(game, bin_trees, bin_trees, 3)
    arrrock = element(game, bin_rocks, bin_rocks, 5)
    arrblack = element(game, bin_black, bin_black, 3)
    arrriver = element(game, bin_river, bin_river, 3)
    arrmain = element(game, bin_green, bin_green, 3)

    arrout = element(game, bin_terrain, bin_terrain, 6)

    unpack_array(arrrock, 'K', game)
    unpack_array(arrmain, 'M', game)
    unpack_array(arrriver, 'R', game)
    unpack_array(arrblack, 'B', game)
    unpack_array(arrtree, 'T', game)
    unpack_array(arrout, '0', game)

    unpack_array(arrplayer, 'P', game, (0, -1))

    if pickaxe_pos != None:
        for i in range(len(axe_pos)):
            axe_pos[i] = (axe_pos[i][0] // 22, axe_pos[i][1] // 16)
            unpack_array(axe_pos, 'A', game, (0, -1))

    if pickaxe_pos != None:
        for i in range(len(pickaxe_pos)):
            pickaxe_pos[i] = (pickaxe_pos[i][0] // 22, pickaxe_pos[i][1] // 16)
            unpack_array(pickaxe_pos, 'I', game, (0, -1))

    game.replace_letter('t', 'M', 'T')
    game.replace_letter('k', 'M', 'K')

    for i in range(2):
        for j in range(20):
            game.matrix_add(i, j, '0')
    for j in range(20):
        game.matrix_add(35, j, '0')


def element(game, bin, im, nb):
    result = []
    for x in range(22, 810, 22):
        for y in range(0, 320, 16):
            arr0 = get_pixel_color(bin, x - 10, y)
            arr1 = get_pixel_color(bin, x - 5, y)
            arr2 = get_pixel_color(bin, x + 0, y)

            arr3 = get_pixel_color(bin, x - 10, y + 12)
            arr4 = get_pixel_color(bin, x - 5, y + 12)
            arr5 = get_pixel_color(bin, x + 0, y + 12)

            arr6 = get_pixel_color(bin, x - 10, y + 7)
            arr7 = get_pixel_color(bin, x - 5, y + 7)
            arr8 = get_pixel_color(bin, x + 0, y + 7)

            arrE = [arr0, arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8]
            somme = 0
            for i in range(len(arrE)):
                somme += (arrE[i][0] != 0 and arrE[i][1] != 0
                          and arrE[i][2] != 0)
            if somme >= nb:
                result.append([x // 22 - 1,
                               y // 16])  # minus one because magic

    return result


def unpack_array(arr, vall, game, offset=(0, 0)):
    for e in arr:
        pass
        if e[0] - offset[0] > 0 and e[0] - offset[0] < len(game.matrix[0]) \
        and e[1] - offset[1] > 0 and e[1] - offset[1] < len(game.matrix):

            game.matrix_add(e[0] - offset[0], e[1] - offset[1], vall)


def draw(im):
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    player.draw_contours_return_bin(im, im_hsv)
    axe.draw_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    pickaxe.draw_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    green.draw_contours_return_bin(im, im_hsv)
    trees.draw_contours_return_bin(im, im_hsv)
    rock.draw_contours_return_bin(im, im_hsv)
    blackrock.draw_contours_return_bin(im, im_hsv)
    river.draw_contours_return_bin(im, im_hsv )
    terrain.draw_contours_return_bin(im, im_hsv )


def cut(im):
    im = rotate(im, -8)
    x, y = 0, 125
    h, w = 320, 800
    im = im[y:y + h, x:x + w]

    rows, cols = im.shape[:-1]

    a, b, c = [382, 52], [500, 50], [400, 200]
    offsetx = 20
    d, e, f = [382 + offsetx, 52], [500 + offsetx, 50], [400, 200]

    pts1 = np.float32([a, b, c])
    pts2 = np.float32([d, e, f])

    dst = im  # Uh Oh

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(im, M, (cols, rows))

    return dst


def grid(im):
    tiny_offset = 0

    for x in range(5, 900, 22):
        tiny_offset += 0.1
        for y in range(0, 400):
            im = set_pixel_color(im, x + int(tiny_offset), y, (100, 0, 100))

    for y in range(0, 400, 16):
        for x in range(0, 900):
            im = set_pixel_color(im, x, y, (100, 0, 100))


def rotate(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image,
                            rot_mat,
                            image.shape[1::-1],
                            flags=cv2.INTER_LINEAR)
    return result


def get_pixel_color(im, x, y):
    """get the pixel color"""
    rows, cols = im.shape[:-1]
    if x < 0 and y < 0:
        raise Exception("get pixel: coordinates need to be positive!")
    if x < cols and y < rows:
        return im[y, x]
    raise Exception("get pixel: x and y out of range!")


def set_pixel_color(im, x, y, color):
    """set the pixel color"""
    rows, cols = im.shape[:-1]
    if x < 0 and y < 0:
        raise Exception("get pixel: coordinates need to be positive!")
    if x < cols and y < rows:
        im[y, x] = color
        return im
    return im