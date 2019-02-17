class Validation:

    @staticmethod
    def is_empty(string):
        if len(string.strip()) == 0:
            return True
        return False