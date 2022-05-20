import re

from attr import attr, attrs


@attrs
class BaseJob(object):
    """
    Base class for Job.
    """
    company = attr(type=str, converter=lambda x: x.strip())
    location = attr(type=str, converter=lambda x: x.strip())
    job_name = attr(type=str, converter=lambda x: x.strip())

    lower_salary = attr(type=float, init=False, default=-1)
    higher_salary = attr(type=float, init=False, default=-1)

    low_k = high_k = [1000, 10000, 835, 30]
    patterns = [
        '([0-9.]+)-([0-9.]+)千/月', '([0-9.]+)-([0-9.]+)万/月', '([0-9.]+)-([0-9.]+)万/年',
        '([0-9.]+)-([0-9.]+)元/天'
    ]

    def set_salary(self, salary):
        for i, pattern in enumerate(self.patterns):
            result = re.match(pattern, salary)
            if not result: continue
            low, high = float(result.group(1)), float(result.group(2))
            self.lower_salary = low * self.low_k[i]
            self.higher_salary = high * self.high_k[i]
            break
        return self

    @classmethod
    def new_job(cls, company, location, job_name, salary):
        return cls(company, location, job_name).set_salary(salary)


def main():
    job = BaseJob.new_job('xxx公司', 'xxx街道', '搬砖工', '100-200元/天')
    print(job)


if __name__ == '__main__':
    main()