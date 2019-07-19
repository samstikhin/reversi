class ImpossibleAction(Exception):
    def __init__(self, description):
        super(ImpossibleAction, self).__init__()
        self.description = description

    def __str__(self):
        return self.description
