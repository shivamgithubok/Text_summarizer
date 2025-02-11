import os
from box.exceptions import BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from typing import Any
from pathlib import Path
import yaml
from ensure import ensure_annotations

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> dict:  # Accept both str and Path
    path_to_yaml = Path(path_to_yaml)  # Convert to Path if it's a string

    try:
        with path_to_yaml.open("r") as yaml_file:  # Use Path's open method
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)

    except BoxValueError:
        raise ValueError("YAML file is empty")
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {path_to_yaml}")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directory: list,verbose=True):
    for path in path_to_directory:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")



@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~{size_in_kb} KB"