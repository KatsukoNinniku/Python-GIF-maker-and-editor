import subprocess


def GifsicleLinuxCheck():
    try:
        result = subprocess.run(["gifsicle", "--version"])
        return 0
    except FileNotFoundError:
        return 1
    except subprocess.CalledProcessError as e:
        return 2

print(GifsicleLinuxCheck())