class Hour:
    def __init__(self, hour: int, minute: int):
        self.hour: str = None
        self.minute: str = None

        self.__init_hours(hour, minute)

    def __init_hours(self, hour: int, minute: int):
        if 10 > hour >= 0:
            self.hour = f"0{hour}"
        elif 10 <= hour < 25:
            self.hour = f"{hour}"
        elif hour == 0:
            self.hour = '00'

        if 0 < minute < 10:
            self.minute = f"0{minute}"
        else:
            self.minute = f"{minute}"

    def increment(self):
        integerhour: int = int(self.hour)

        if integerhour == 24:
            self.hour = f'00'
        elif 9 > integerhour >= 0:
            integerhour = integerhour + 1
            self.hour = f"0{integerhour}"
        else:
            integerhour = integerhour + 1
            self.hour = f'{integerhour}'

    def decrement(self) -> str:
        integerhour: int = int(self.hour)

        if integerhour == 0:
            return '24'
        elif 10 > integerhour > 0:
            integerhour = integerhour - 1
            return f'0{integerhour}'
        else:
            integerhour = integerhour - 1
            return str(integerhour)
