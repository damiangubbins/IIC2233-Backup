# pylint: disable=missing-docstring


class Logger:

    @staticmethod
    def first_line():
        print("\n"*3)
        Logger.log("User", "Request", "Action", "Detail")

    @staticmethod
    def log(user: str, request: str, action: str, detail: str):
        print(f"""\
{user:^20}|{request:^20}|{action:^20}|{detail:^25}
{'-' * 87}""")


if __name__ == "__main__":
    pass
