class GlobalException(Exception):

    def __init__(self, code):
        self.code = code
        super().__init__("")
