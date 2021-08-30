from abc import abstractclassmethod


class InteractiveObject:
    def __init__(self):
        self._interactiveText = None

    @abstractclassmethod
    def Get_Text(self):
        return None


class GoldenCoin(InteractiveObject):
    def __init__(self, point):
        super().__init__()
        self.point = point
        self.name = "Golden Coin"

    def Get_Text(self):
        if self._interactiveText is None:
            self._interactiveText = "ERROR"
        else:
            self._interactiveText = "SCORE: " + str(self.point)


class SilverCoin(GoldenCoin):
    def __init__(self, point):
        super().__init__(point)
        self.name = "Silver Coin"

    def Get_Text(self):
        if self._interactiveText is None:
            self._interactiveText = "ERROR"
        else:
            self._interactiveText = "SCORE: " + str(self.point)