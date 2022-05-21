from retrying import retry


@retry(stop_max_attempt_number=3,
       retry_on_result=lambda e: True)
def main():
    print('s')


if __name__ == '__main__':
    main()
