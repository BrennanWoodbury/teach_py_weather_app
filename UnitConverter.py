class UnitConverter:
    def __init__(self, value_to_convert: float):
        self.value_to_convert = value_to_convert

    def mm_to_inches(self) -> float:
        inches = round((self.value_to_convert / 25.4), 3)
        return inches

    def cm_to_inches(self) -> float:
        inches = round((self.value_to_convert / 2.54), 3)
        return inches
