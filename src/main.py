from core.runner import Runner


'''
This is the main entry point of the application.
It initializes the Runner class and consequently the necessaries management istances.
At the end starts the main execution loop.
'''

def main():
    runner = Runner()
    runner.prepare()
    while runner.keep_going():
        runner.main_execution()

if __name__ == '__main__':
    main()