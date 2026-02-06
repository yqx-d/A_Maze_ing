from typing import Any


class Parser:

    @staticmethod
    def get_type_config(
        key: str,
        str_value: str
    ) -> Any:

        if key == "SEED":
            if str_value == "None":
                return None
            return int(str_value)

        if key in ("WIDTH", "HEIGHT"):
            value = int(str_value)
            if value < 0:
                raise ValueError(f"{key} has negative values.")
            return value

        if key in ("ENTRY", "EXIT"):
            value = tuple(map(int, str_value.split(",")))
            if len(value) != 2:
                raise ValueError(
                    f"Invalid format for {key}: "
                    f"expected x,y got '{str_value}'"
                )
            x, y = value
            if x < 0 or y < 0:
                raise ValueError(f"{key} has negative values.")
            return value

        if key == "PERFECT":
            if str_value.lower() == "true":
                return True
            if str_value.lower() == "false":
                return False
            raise ValueError(
                f"Invalid format for {key}: "
                f"expected true or false got '{str_value}'"
            )

        return str_value

    @staticmethod
    def parse_config(
        path: str
    ) -> dict[str, Any]:

        config: dict[str, Any] = {}
        key_required: list[str] = [
            "WIDTH", "HEIGHT",
            "ENTRY", "EXIT",
            "OUTPUT_FILE",
            "PERFECT"
        ]

        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                try:
                    key, str_value = map(str.strip, line.split("=", 1))
                    config[key] = Parser.get_type_config(key, str_value)
                except ValueError as e:
                    raise ValueError(
                        f"Invalid line in config: {line}\nError: {e}")

        if "SEED" not in config:
            config['SEED'] = None

        for key in key_required:
            if key not in config:
                raise KeyError(f"{key} not found in {path}.")

        if config["ENTRY"] == config["EXIT"]:
            raise ValueError(
                "ENTRY and EXIT must be different coordinates.")

        return config
