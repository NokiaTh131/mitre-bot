from app.tools.retrieval import retrieve_context
from pprint import pprint


def main():
    pprint(retrieve_context("download malware"))


if __name__ == "__main__":
    main()
