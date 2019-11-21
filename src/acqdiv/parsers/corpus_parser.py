"""Abstract class for corpus parsing."""

import glob
from abc import ABC, abstractmethod

from tqdm import tqdm

from acqdiv.model.corpus import Corpus
from acqdiv.util.uniquespeaker import set_unique_speakers
from acqdiv.util.session_duration import extract_duration


class CorpusParser(ABC):
    """Methods for constructing a corpus instance."""

    def __init__(self, cfg, disable_pbar=False):
        """Initialize config.

        Args:
            cfg (dict): Corpus configuration data.
            disable_pbar (bool): Whether the progressbar should be disabled.
        """
        self.cfg = cfg
        self.disable_pbar = disable_pbar
        tqdm.monitor_interval = 0
        self.corpus = Corpus()

    def parse(self):
        """Get a Corpus instance."""
        corpus = self.corpus
        corpus.iso_639_3 = self.cfg['iso639-3']
        corpus.glottolog_code = self.cfg['glottolog_code']
        corpus.corpus = self.cfg['corpus']
        corpus.language = self.cfg['language']
        corpus.owner = self.cfg['owner']
        corpus.acronym = self.cfg['acronym']
        corpus.name = self.cfg['name']
        corpus.sessions = self.iter_sessions()

        return corpus

    @abstractmethod
    def get_session_parser(self, session_path):
        """Get a session parser.

        Returns:
            acqdiv.parsers.session_parser.SessionParser: The session parser.
        """
        pass

    def iter_sessions(self):
        """Iter the sessions of the corpus.

        Yields:
            acqdiv.parsers.SessionParser: The session parser.
        """
        session_paths = sorted(glob.glob(self.cfg['sessions']))

        with tqdm(session_paths, disable=self.disable_pbar) as pbar:

            for session_path in pbar:
                pbar.set_description(session_path)

                session_parser = self.get_session_parser(session_path)

                if session_parser is not None:

                    session = session_parser.parse()

                    # set unique speakers
                    set_unique_speakers(self.corpus.corpus, session.speakers)

                    # add duration
                    session.duration = extract_duration(self.corpus.corpus,
                                                        session.source_id)

                    # ignore sessions with no utterances
                    if len(session.utterances):
                        if self.disable_pbar:
                            print("\t", session_path)

                        yield session
