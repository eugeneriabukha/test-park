class CustomException(Exception):
    def __init__(self, sName):
        # Set some exception infomation
        self.name = sName
