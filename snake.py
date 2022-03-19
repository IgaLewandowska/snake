import time

import pygame
import random
import datetime

pygame.init()

szer = 800
wys = 600
okno = pygame.display.set_mode((szer, wys))
pygame.display.set_caption("SNAKE")

niebieski = (0, 0, 255)
zielony = (20, 255, 80)
bialy = (255, 255, 255)
zolty = (255, 255, 105)
czarny = (0, 0, 0)

czas = pygame.time.Clock()
wymiary_snake = 20

czcionka = pygame.font.SysFont("markerfelt", 20)

def odczytywanie_z_pliku():
    global lista, naj_wynik
    with open("wyniki.txt", newline="", encoding="utf-8") as plik:
        zawartosc = plik.read().split()
        lista = []
        for i in zawartosc:
            lista.append(int(i))
    naj_wynik = max(lista)

def najwyzszy_wynik(naj_wynik):
    wynik = czcionka.render("Najwyższy wynik to: " + str(naj_wynik), True, bialy)
    miejsce = wynik.get_rect(center=(szer/2, 70))
    okno.blit(wynik, miejsce)


def zapisywanie_do_pliku(t, dlugosc_snake):
    if (dlugosc_snake - 1) > naj_wynik:
        wiadomosc(f"Gratulacje! Masz najlepszy wynik {dlugosc_snake - 1}", zolty, 130)
    with open("wyniki.txt", mode="a", newline="", encoding="utf-8") as plik:
        plik.write(t+"\n")


def wyniki(wynik):
    wartosc = czcionka.render("Wynik: " + str(wynik), True, bialy)
    miejsce = wartosc.get_rect(center=(szer/2, 20))
    okno.blit(wartosc, miejsce)


def wiadomosc(wiadomosc, kolor, gdzie):
    napis = czcionka.render(wiadomosc, True, kolor)
    miejsce = napis.get_rect(center=(szer/2, gdzie))
    okno.blit(napis, miejsce)


def rysuj(wymiary_snake, rozmiar):
    for i in rozmiar:
        pygame.draw.rect(okno, bialy, [i[0], i[1], wymiary_snake, wymiary_snake])

def jedzenie():
    x_jedzenie = round(random.randrange(0, szer - wymiary_snake) / 20.0) * 20.0
    y_jedzenie = round(random.randrange(0, wys - wymiary_snake) / 20.0) * 20.0
    czas_jedzenia = time.time()
    return x_jedzenie, y_jedzenie, czas_jedzenia


def main():
    start = False
    koniec = False

    x = szer / 2
    y = wys / 2

    x_zmiana = 0
    y_zmiana = 0

    x_jedzenie, y_jedzenie, czas_jedzenia = jedzenie()

    rozmiar_snake = []
    dlugosc_snake = 1
    predkosc_snake = 10

    while not start:
        odczytywanie_z_pliku()

        while koniec == True:
            wiadomosc("Przegrałeś! Q-wyjście R-zagraj jeszcze raz", zielony, 100)
            wyniki(dlugosc_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_r:
                        main()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_zmiana = wymiary_snake
                    y_zmiana = 0
                elif event.key == pygame.K_LEFT:
                    x_zmiana = -wymiary_snake
                    y_zmiana = 0
                elif event.key == pygame.K_UP:
                    x_zmiana = 0
                    y_zmiana = -wymiary_snake
                elif event.key == pygame.K_DOWN:
                    x_zmiana = 0
                    y_zmiana = wymiary_snake

        x += x_zmiana
        y += y_zmiana
        okno.fill(czarny)
        pygame.draw.rect(okno, niebieski, [x_jedzenie, y_jedzenie, wymiary_snake, wymiary_snake])
        glowa = []
        glowa.append(x)
        glowa.append(y)
        rozmiar_snake.append(glowa)
        if len(rozmiar_snake) > dlugosc_snake:
            del rozmiar_snake[0]

        for i in rozmiar_snake[:-1]:
            if i == glowa:
                zapisywanie_do_pliku(str(dlugosc_snake - 1), dlugosc_snake)
                koniec = True

        if x >= szer or x < 0 or y >= wys or y < 0:
            zapisywanie_do_pliku(str(dlugosc_snake - 1), dlugosc_snake)
            koniec = True

        if x == x_jedzenie and y == y_jedzenie:
            x_jedzenie, y_jedzenie, czas_jedzenia = jedzenie()
            dlugosc_snake += 1
            predkosc_snake += 1

        if czas_jedzenia + 10 < time.time():
            x_jedzenie, y_jedzenie, czas_jedzenia = jedzenie()

        rysuj(wymiary_snake, rozmiar_snake)
        wyniki(dlugosc_snake - 1)
        wiadomosc(f"Najwyższy wynik: {naj_wynik}", bialy, 60)
        czas.tick(predkosc_snake)
        pygame.display.update()

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()
