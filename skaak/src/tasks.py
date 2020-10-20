import cffi
import invoke
import pathlib


def print_banner(msg):
    print("=" * 30)
    print(f"= {msg}")


@invoke.task
def build(c):
    print_banner("Building C Library")
    invoke.run("g++ -c -fPIC lib.cpp -o lib.o")
    invoke.run("g++ -shared -Wl,-soname,lib.so -o lib.so lib.o")
    print("* Complete")
