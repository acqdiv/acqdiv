""" Post-processing processes on the corpora in the ACQDIV-DB. """

import argparse


class PostProcessor:

    def __init__(self):
        self.engine = None
        self.conn = None

    def postprocess(self, test=False):
        """Global setup and then call post-processes."""
        pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-t', action='store_true')
    args = p.parse_args()

    postprocessor = PostProcessor()
    postprocessor.postprocess(test=args.t)


if __name__ == "__main__":
    main()