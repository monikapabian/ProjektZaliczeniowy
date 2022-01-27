import tkinter as tk
from random import randint, choice

# Wartości stałe
SPEED = 400
WIDTH_SIZE = 720
HEIGHT_SIZE = 720


class Score:    # Klasa przetrzymująca aktualny wynik i czas
    def __init__(self):
        self.score_value = 0
        self.time = 100

    def give_curr_score(self):  # Metoda zwracająca aktualny wynik
        return self.score_value

    def change_score(self, value):  # Metoda zmieniająca wartość wyniku o podaną wartość
        self.score_value += value

    def minus_time(self):   # Metoda odliczająca czas
        self.time -= 1


curr_score = Score()


class Entity:   # Klasa nadrzędna opisująca istotę (przycisk)
    def __init__(self):
        self.x = 0
        self.y = 0
        self.life = randint(4, 9)   # Długość życia
        self.score_value = 20 - self.life    # Wartość punktowa (zależna od długości życia)
        self.button = None
        self.color = 'white'

    def positive_score(self, event):    # Metoda dodająca punkty
        curr_score.change_score(self.score_value)

        self.button.place(x=-100, y=-100)

    def negative_score(self, event):    # Metoda odejmująca punkty
        curr_score.change_score(0-self.score_value)

        self.button.place(x=-100, y=-100)

    def update(self):   # Metoda aktualizująca wygląd przycisku
        self.button.configure(text=f'{self.life}')
        if self.life == 1:
            self.button.configure(bg='#41424f')

    def draw(self, root):   # Metoda tworząca istotę (przycisk) w losowym miejscu w polu gry
        self.x = randint(60, WIDTH_SIZE-80)
        self.y = randint(20, HEIGHT_SIZE-120)
        # target = area.create_rectangle(self.x, self.y, self.x+20, self.y+20, fill='red')
        target = tk.Button(root, width=2, bg=self.color, text=f'{self.life}')
        target = self.bind_button(target)
        target.place(x=self.x, y=self.y)
        self.button = target

    def bind_button(self, target):  # Metoda przypisująca wynik do akcji
        target.bind('<Button-1>', self.positive_score)
        target.bind('<Button-3>', self.negative_score)
        return target

    def kill(self, root):   # Metoda usuwająca istotę (przycisk) z planszy
        # self.button.destroy()
        self.button.place(x=-100, y=-100)


class Ally(Entity):     # Klasa Przyjaciel - zielony przycisk (LPM)
    def __init__(self):
        super().__init__()
        self.color = 'green'

    def bind_button(self, target):
        target.bind('<Button-1>', self.positive_score)
        target.bind('<Button-3>', self.negative_score)
        return target


class Enemy(Entity):    # Klasa Przeciwnik - czerwony przycisk (PPM)
    def __init__(self):
        super().__init__()
        self.color = 'red'

    def bind_button(self, target):
        target.bind('<Button-1>', self.negative_score)
        target.bind('<Button-3>', self.positive_score)
        return target


def loop(root, area, targets, label_score, label_time, start_button):   # Funkcja pętli
    start_button.destroy()

    obj = choice([Ally(), Enemy()])
    obj.draw(root)
    targets.append(obj)
    for target in targets:
        target.life -= 1
        target.update()
        if target.life == 0:
            target.kill(root)

    curr_score.change_score(-1)
    curr_score.minus_time()

    label_score.config(text=f'PUNKTY: {curr_score.give_curr_score()}')
    label_time.config(text=f'{curr_score.time}')

    if curr_score.time == 0:
        label_final_score = tk.Label(root, text=f'TWÓJ WYNIK TO:\n{curr_score.give_curr_score()}', font=('consolas', 18), bg='black', fg='green')
        label_final_score.place(x=265, y=300)
    else:
        root.after(SPEED, loop, root, area, targets, label_score, label_time, start_button)


def game():     # Główna funkcja gry

    # Inicjacja okna gry:

    root = tk.Tk()
    root.title('Gra - Test zręcznościowy')
    root.geometry(f'{WIDTH_SIZE}x{HEIGHT_SIZE}')
    root.configure(bg='black')
    root.resizable(False, False)

    # Rysowanie planszy:

    area = tk.Canvas(root, width=WIDTH_SIZE-100, height=HEIGHT_SIZE-100)
    area.create_rectangle(0, 0, WIDTH_SIZE, HEIGHT_SIZE, fill='#361559', outline='white')
    area.pack(pady=20)

    # Dodawanie opisów:

    label_score = tk.Label(root, text=f'PUNKTY: 0', font=('consolas', 18), bg='black', fg='white')
    label_score.pack()

    label_time = tk.Label(root, text=f'{curr_score.time}', font=('consolas', 10), bg='black', fg='white')
    label_time.pack()

    label_ally = tk.Label(root, text=f'LPM by ratować zielonych', font=('consolas', 10), bg='black', fg='green')
    label_ally.place(x=50, y=650)

    label_enemy = tk.Label(root, text=f'PPM by zaatakować czerownych', font=('consolas', 10), bg='black', fg='red')
    label_enemy.place(x=465, y=650)

    label_names = tk.Label(root, text=f'Monika Pabian  Wojciech Mleczak', font=('consolas', 8), bg='black', fg='#a3a3a3')
    label_names.place(x=510, y=700)

    targets = []    # Lista przechowywująca cele (przyciski)

    # Przycisk startu:

    start_button = tk.Button(root, text='START', font=('consolas', 30), bg='black', fg='white', command=lambda: loop(root, area, targets, label_score, label_time, start_button))
    start_button.place(x=300, y=300)

    # loop(root, area, targets, label_score, label_time)

    root.mainloop()


if __name__ == '__main__':
    game()
