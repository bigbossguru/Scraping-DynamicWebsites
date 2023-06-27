from .base_job import Job, SuffixEnum


class SuffixNofluffEnum(SuffixEnum):
    SUFFIX_CZ_BACKEND = "/cz/backend"


class NofluffJob(Job):
    def __init__(
        self,
        name: str,
        filter_field: str,
        base_url: str = "https://nofluffjobs.com",
        flag_dynamic_content: bool = False,
    ):
        super().__init__(name, base_url, filter_field, flag_dynamic_content)

    def parse_job(self, suffix: SuffixNofluffEnum):
        content = self._type_of_content()(self.base_url + suffix.value)
        soup = self.scrapper.searcher(content)
        jobs = soup.find_all("a", class_="posting-list-item")

        for j in jobs:
            try:
                title = j.find(
                    "h3", class_="posting-title__position text-truncate color-main ng-star-inserted"
                ).text
                company = j.find("span", class_="d-block posting-title__company text-truncate").text
                salary = j.find(
                    "span",
                    class_="text-truncate badgy salary tw-btn tw-btn-secondary-outline tw-btn-xs ng-star-inserted",
                ).text
                place = j.find(
                    "span",
                    class_="tw-text-ellipsis tw-inline-block tw-overflow-hidden tw-whitespace-nowrap lg:tw-max-w-[100px] tw-text-right",
                ).text
                skills = j.find("a", class_="ng-star-inserted").text

                self.result_data["title"].append(title.strip())
                self.result_data["company"].append(company.strip())
                self.result_data["place"].append(place.strip())
                self.result_data["type"].append("B2B")
                self.result_data["salary"].append(salary.replace("\n", ""))
                self.result_data["skills"].append(skills.strip())
                self.result_data["link"].append(self.base_url + j.get("href"))
            except Exception:
                continue
