from app.tools.retrieval import AttackPatternsTool
from pprint import pprint


def main():
    tool = AttackPatternsTool()
    pprint(tool.retrieve_context("download malware"))


if __name__ == "__main__":
    main()
