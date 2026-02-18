
from pathlib import Path
from typing import List, Dict, Any
import yaml


class PageManager:
    """Manages locators and configuration from external YAML files"""

    def __init__(self, pages_dir: str = "pages"):
        """
        Initialize the Page Manager

        params: pages_dir: Directory containing page YAML files
        """
        self.pages_dir = pages_dir
        self.pages = self._load_pages()

    def get_combined_locator(self, page: str, section: str, element: str) -> str:
        """
        Get combined locator string for Playwright

        params: page: Page name (e.g., 'home')
        params: section: Section name (e.g., 'google')
        params: element: Element name (e.g., 'cookie_accept_button')

        Returns:
            Combined locator string separated by commas
        """
        locators = self._get_locators(page, section, element)
        if locators:
            return ', '.join(locators)
        return ""

    def _get_locators(self, page: str, section: str, element: str) -> List[str]:
        """
        Get locators list from page YAML

        params page: Page name (yaml filename without extension)
        params section: Section name inside the YAML
        params element: Element name

        Returns:
            List of locators
        """
        return (
            self.pages
                .get(page, {})
                .get(section, {})
                .get(element, [])
        )

    def _load_pages(self) -> Dict[str, Dict[str, Any]]:
        """
        Load all YAML files from pages directory into a dictionary
        Returns:
            Dictionary with page names as keys and their content as values
        """
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        pages_path = project_root / self.pages_dir

        pages: Dict[str, Dict[str, Any]] = {}

        if not pages_path.exists():
            return pages

        for yaml_file in pages_path.glob("*.yaml"):
            with open(yaml_file, "r", encoding="utf-8") as f:
                pages[yaml_file.stem] = yaml.safe_load(f) or {}

        return pages
