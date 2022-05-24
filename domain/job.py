import re

from attr import attr, attrs
from spiders.base_requests_spider import ItemBean


@attrs
class Job(ItemBean):
    """
    职位的实体类。
    属性主要包括：公司名称、公司地址、职位名称、最低薪资、最高薪资（以月为单位）。
    """
    company = attr(type=str, converter=lambda x: x.strip())
    location = attr(type=str, converter=lambda x: x.strip())
    job_name = attr(type=str, converter=lambda x: x.strip())

    lower_salary = attr(type=float, init=False, default=-1)
    higher_salary = attr(type=float, init=False, default=-1)

    low_k = high_k = (1000, 10000, 835, 30, 30, 240, 1000)
    patterns = [
        '([0-9.]+)-([0-9.]+)千/月', '([0-9.]+)-([0-9.]+)万/月', '([0-9.]+)-([0-9.]+)万/年',
        '([0-9.]+)-([0-9.]+)元/天', '(([0-9.]+))元/天', '(([0-9.]+))元/小时', '(([0-9.]+))千以下/月'
    ]

    def set_salary(self, salary):
        for i, pattern in enumerate(self.patterns):
            result = re.match(pattern, salary)
            if not result: continue
            low, high = float(result.group(1)), float(result.group(2))
            self.lower_salary = low * self.low_k[i]
            self.higher_salary = high * self.high_k[i]
            break
        if self.lower_salary < 0:
            self._write_log(f'({self.lower_salary}, {self.higher_salary}) => {salary}')
        if self.lower_salary > 10_0000:
            self._write_log(f'({self.lower_salary}, {self.higher_salary}) => {salary}')
        return self

    @staticmethod
    def _write_log(string):
        log_path = '/Users/luyan/Desktop/log.txt'
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f'{string}\n')

    @classmethod
    def new_job(cls, company, location, job_name, salary):
        return cls(company, location, job_name).set_salary(salary)


def main():
    job = Job.new_job('xxx公司', 'xxx街道', '搬砖工', '100-200元/天')
    print(job)


if __name__ == '__main__':
    main()
