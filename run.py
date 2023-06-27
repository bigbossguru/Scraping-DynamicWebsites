from jobs.jobcz import JobCZ, SuffixJobCZEnum
from jobs.nofluffjobs import NofluffJob, SuffixNofluffEnum


def main():
    task_jobcz = JobCZ("Job.cz", "python", flag_dynamic_content=True)
    task_jobcz.parse_job(SuffixJobCZEnum.SUFFIX_WITH_SALARY)
    task_jobcz.to_csv()

    # task_nofluffjob = NofluffJob("NofluffJobs.cz", "python")
    # task_nofluffjob.parse_job(SuffixNofluffEnum.SUFFIX_CZ_BACKEND)
    # task_nofluffjob.to_csv()


if __name__ == "__main__":
    main()
