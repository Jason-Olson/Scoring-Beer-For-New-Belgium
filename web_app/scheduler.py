import time
import schedule

from data import get_data, add_data


def job():
    data = get_data()
    if data:
        add_data(data)
        print("I'm working...")


schedule.every(1).minutes.do(job)


def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
