from collections import defaultdict
from typing import Optional
import enum

import pandas as pd

from adt.singleton import Singleton
from scraper.scraper import Scraper


class SuffixEnum(enum.StrEnum):
    ...


class Job(metaclass=Singleton):
    def __init__(
        self,
        name: str,
        base_url: str,
        filter_field: str,
        flag_dynamic_content: bool = False,
    ) -> None:
        self.name = name
        self.base_url = base_url
        self.filter_field = filter_field
        self.scrapper: Scraper = Scraper()
        self.flag_dynamic_content = flag_dynamic_content
        self.result_data = defaultdict(list)

    def parse_job(self, suffix: SuffixEnum) -> None:
        raise NotImplementedError

    def _get_content_from_page(self, jobs) -> None:
        raise NotImplementedError

    def _type_of_content(self):
        return (
            self.scrapper.get_dynamic_page_content
            if self.flag_dynamic_content
            else self.scrapper.get_static_page_content
        )

    def to_csv(self, filename: Optional[str] = None, extension: str = ".csv") -> None:
        filename = filename or self.name.replace(".", "")
        pd.DataFrame(self.result_data).to_csv(filename + extension, index=False)

    def get_dict_result(self) -> defaultdict:
        return self.result_data

    def get_df_result(self) -> pd.DataFrame:
        return pd.DataFrame(self.result_data)
