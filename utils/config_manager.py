"""
Locators utility module for managing element selectors and configuration
"""
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manage configuration from a yaml file"""

    def __init__(
        self, config_file: str = "browser.yaml"):
        """
        Initialize the config manager

        Args:
            config_file: filename of the configuration yaml file.
        """
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        config_path = project_root / "config" / self.config_file

        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
