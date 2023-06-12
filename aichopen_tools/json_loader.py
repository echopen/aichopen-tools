import json


class JsonLoader:
    @staticmethod
    def load(file_path: str) -> dict:
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def dump(file_path: str, content: dict) -> None:
        with open(file_path, 'w') as file:
            json.dump(content, file)
