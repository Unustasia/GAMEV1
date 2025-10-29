class HanoiGame:
    def __init__(self):
        self.poles = [[3, 2, 1], [], []]  # начальное состояние
        self.moves = 0
        self.selected_pole = None
        self.target_pole = None

    def select_pole(self, pole_index):
        if self.selected_pole is None:
            self.selected_pole = pole_index
        else:
            self.target_pole = pole_index

    def move_ring(self):
        if self.selected_pole is None:
            return False, "Выберите исходный столб!"
        if self.target_pole is None:
            return False, "Выберите целевой столб!"
        if not self.poles[self.selected_pole]:
            return False, "На этом столбе нет колец!"
        ring = self.poles[self.selected_pole][-1]
        if (self.poles[self.target_pole] and 
                self.poles[self.target_pole][-1] < ring):
            return False, "Нельзя положить большее кольцо на меньшее!"
        self.poles[self.target_pole].append(ring)
        self.poles[self.selected_pole].pop()
        self.moves += 1
        self.selected_pole = None
        self.target_pole = None
        return True, "Ход выполнен!"


    def is_won(self):
        return self.poles[2] == [3, 2, 1]

    def reset(self):
        self.poles = [[3, 2, 1], [], []]
        self.moves = 0
        self.selected_pole = None
        self.target_pole = None
