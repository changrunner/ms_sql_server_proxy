from subprocess import Popen, PIPE
import platform


def main():
    cmd_suffix = ""
    if platform.system().lower() == 'linux'.lower():
        cmd_suffix = "3"

    p = Popen(f"python{cmd_suffix} -m pip install --upgrade pip".split(" "))
    p.communicate()

    p = Popen(f"pip{cmd_suffix} install pipenv".split(" "))
    p.communicate()

    p = Popen("pipenv --rm".split(" "))
    p.communicate()

    p = Popen("pipenv install".split(" "))
    p.communicate()

    p = Popen("pipenv install --dev".split(" "))
    p.communicate()


if __name__ == '__main__':
    main()

