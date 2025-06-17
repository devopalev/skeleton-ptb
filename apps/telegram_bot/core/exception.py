class AppError(Exception):
    pass


class EnvRequiredError(AppError):
    def __init__(self, var_name: str):
        self.add_note(f'Environment variable <{var_name}> is required!')
