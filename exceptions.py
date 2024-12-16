class EndPageException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "End of page"
    