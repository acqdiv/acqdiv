

class CHAT:

    def __init__(self):
        """
        date (str): The value at @Date.
        participants (Dict[str, acqdiv.parsers.chat.model.Participant]):
            The participants as read from @Participants, @ID, @Birth of.
        pid (str): The value at @PID.
        media_filename (str): The filename at @Media.
        media_format (str): The format at @Media.
        media_comment (str): The comment at @Media.
        records (List[acqdiv.parsers.chat.model.Record]): The records.
        """
        self.date = ''
        self.participants = {}
        self.pid = ''
        self.media_filename = ''
        self.media_format = ''
        self.media_comment = ''
        self.records = []
