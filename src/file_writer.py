import sys


def file_writer(filename: str):
    print(f'name: {filename}')


file_writer('E001')


print(os.environ.get('TYPE'))