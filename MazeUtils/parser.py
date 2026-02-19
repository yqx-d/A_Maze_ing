from typing import Any


class Parser:
    """Parse and validate maze configuration files."""

    @staticmethod
    def get_type_config(
        key: str,
        str_value: str
    ) -> Any:
        """
        Parse and convert a configuration value based on its key.

        Args:
            key: Configuration key (WIDTH, HEIGHT, ENTRY, EXIT,
                PERFECT, SEED, OUTPUT_FILE).
            str_value: String value to parse.

        Returns:
            Parsed value with appropriate type (int, bool, tuple,
            str, or None).

        Raises:
            ValueError: If value format is invalid for the key.
        """
        if key == "SEED":
            if str_value == "None":
                return None
            try:
                return int(str_value)

            except ValueError:
                raise ValueError("SEED must be None or integer.")

        if key in ("WIDTH", "HEIGHT"):
            return_value = int(str_value)
            if return_value < 0:
                raise ValueError(f"{key} has negative values.")
            return return_value

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
        """
        Parse a maze configuration file.

        Reads and validates all configuration parameters from a file.
        Lines starting with '#' are treated as comments and ignored.

        Args:
            path: Path to the configuration file.

        Returns:
            Dictionary containing all parsed configuration parameters.

        Raises:
            ValueError: If configuration format or values are invalid.
            KeyError: If a required configuration key is missing.
        """
        config: dict[str, Any] = {}
        key_required: list[str] = [
            "WIDTH", "HEIGHT",
            "ENTRY", "EXIT",
            "OUTPUT_FILE",
            "PERFECT"
        ]

        try:
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

        except PermissionError as e:
            raise PermissionError(e)

        except FileNotFoundError as e:
            raise FileNotFoundError(e)

        except Exception as e:
            raise Exception(e)

        if "SEED" not in config:
            config['SEED'] = None

        for key in key_required:
            if key not in config:
                raise KeyError(f"{key} not found in {path}.")

        if config["ENTRY"] == config["EXIT"]:
            raise ValueError(
                "ENTRY and EXIT must be different coordinates.")

        entry_x, entry_y = config["ENTRY"]
        exit_x, exit_y = config["EXIT"]

        if (entry_x >= config["WIDTH"] or exit_x >= config["WIDTH"] or
                entry_y >= config["HEIGHT"] or exit_y >= config["HEIGHT"]):
            raise ValueError(
                "One of the entry or exit coordinates exceeds the maze.")

        if config["WIDTH"] < 11 or config["HEIGHT"] < 8:
            raise ValueError(
                "The labyrinth is too small for size forty-two.\n"
                "Min WIDTH: 11 - Min HEIGHT: 8")

        return config
