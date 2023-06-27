import time

from .base_job import Job, SuffixEnum


class SuffixJobCZEnum(SuffixEnum):
    SUFFIX_WITH_SALARY = "/nabidky/vyvoj?pouze-s-odmenou=1"


class JobCZ(Job):
    def __init__(
        self,
        name: str,
        filter_field: str,
        base_url: str = "https://www.startupjobs.cz",
        flag_dynamic_content: bool = False,
    ) -> None:
        super().__init__(name, base_url, filter_field, flag_dynamic_content)

    def parse_job(self, suffix: SuffixJobCZEnum):
        full_url = self.base_url + suffix.value
        content = self._type_of_content()(full_url)
        soup = self.scrapper.searcher(content)
        pages = soup.find(
            "div", class_="bg-lightergeneral text-primary py-2 px-3 leading-5 z-0"
        ).text.strip()[-1]

        for page in range(int(pages)):
            time.sleep(0.3)
            if page == 0:
                jobs = soup.find_all(
                    "article", class_="border-0 border-solid border-b border-sjgray-200"
                )
            else:
                content = self._type_of_content()(
                    f"{self.base_url}/nabidky/vyvoj/strana-{page+1}?pouze-s-odmenou=1"
                )
                soup = self.scrapper.searcher(content)
                jobs = soup.find_all(
                    "article", class_="border-0 border-solid border-b border-sjgray-200"
                )
            self._get_content_from_page(jobs)

    def _get_content_from_page(self, jobs):
        for j in jobs:
            title_flagactivity = [
                i.strip()
                for i in j.find("h3", class_="text-base sm:text-lg font-normal").text.split("\n")
                if i
            ]
            job_desc = [
                i.strip().strip("\xa0\xa0")
                for i in j.find(
                    "div", class_="text-lightsecondary text-sm sm:text-base mr-1"
                ).text.split("●")
                if i
            ]
            job_detail_link = self.base_url + j.find("a").get("href")
            content = self._type_of_content()(job_detail_link)
            soup = self.scrapper.searcher(content)
            salary_stacktech = [
                i.find("dd").text
                for i in soup.find_all(
                    "div", class_="col-span-2 md:col-span-1 p-2 shadow-md rounded-md"
                )[:2]
                if i
            ]
            if title_flagactivity[-1] == "HOT" or title_flagactivity[-1] == "TOP":
                if (
                    (title_flagactivity[0] not in self.result_data["title"])
                    and (self.filter_field in title_flagactivity[0].lower())
                    and (self.filter_field in salary_stacktech[-1].lower())
                ):
                    self.result_data["title"].append(title_flagactivity[0])
                    self.result_data["company"].append(job_desc[0])
                    self.result_data["place"].append(job_desc[1])
                    self.result_data["type"].append(job_desc[2])
                    self.result_data["salary"].append(salary_stacktech[0])
                    self.result_data["skills"].append(salary_stacktech[-1])
                    self.result_data["link"].append(job_detail_link)
                else:
                    continue
            else:
                return
