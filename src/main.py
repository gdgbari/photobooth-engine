from core.runner import Runner


def main():
    runner = Runner()
    runner.prepare()
    while runner.keep_going():
        runner.main_execution()

if __name__ == '__main__':
    main()
