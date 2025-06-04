import time
import schedule

from .derived_measure import calculate_measures

def main():
    calculate_measures()

schedule.every(1).hours.do(main)

# TODO Ejecutar en segundo plano &
if __name__ == '__main__':
    main()
    while True:
        schedule.run_pending()
        time.sleep(60)