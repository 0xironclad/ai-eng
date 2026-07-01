class Microwave:
    def __init__(self, brand: str) -> None:
        self.brand = brand
        self.is_on = False
    
    def turn_on(self) -> None:
        self.is_on = True
    
    def turn_off(self) -> None:
        self.is_on = False

    def __str__(self) -> str:
        return f"{self.brand} - {self.is_on}"

    def __repr__(self) -> str:
        return f"Microwave({self.brand}, {self.is_on})"


