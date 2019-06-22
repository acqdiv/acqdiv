from acqdiv.parsers.chat.cleaners.BaseCHATCleaner import BaseCHATCleaner


class ArabicKuwaitiCleaner(BaseCHATCleaner):

    @classmethod
    def clean_speaker_metadata(
            cls, session_filename, label, name, role,
            age, gender, language, birth_date, target_child):

        name = cls.correct_name(session_filename, name, label)

        return label, name, role, age, gender, language, birth_date

    @classmethod
    def correct_name(cls, session_filename, name, label):
        """Give target children with same name a unique name."""
        if label == 'CHI':
            err_msg = 'Filename unknown: {} - ' \
                      'check if filename has changed in Phonbank!'

            if name == 'Abdulrahman':
                if session_filename == '0104-0107_001-Abdulrahman.cha':
                    return name + '1'
                elif session_filename == '0204-0207_086-Abdulrahman.cha':
                    return name + '2'
                elif session_filename == '0304-0307_173-Abdulrahman.cha':
                    return name + '3'
                else:
                    raise ValueError(err_msg.format(session_filename))
            elif name == 'Fahad':
                if session_filename == '0104-0107_004-Fahad.cha':
                    return name + '1'
                elif session_filename == '0208-0211_116-Fahad.cha':
                    return name + '2'
                else:
                    ValueError(err_msg.format(session_filename))
            elif name == 'Omar':
                if session_filename == '0108-0111_031-Omar.cha':
                    return name + '1'
                elif session_filename == '0204-0207_085-Omar.cha':
                    return name + '2'
                else:
                    ValueError(err_msg.format(session_filename))
            elif name == 'Fatema':
                if session_filename == '0108-0111_043-Fatema.cha':
                    return name + '1'
                elif session_filename == '0300-0303_160-Fatema.cha':
                    return name + '2'
                else:
                    ValueError(err_msg.format(session_filename))
            elif name == 'Abdulaziz':
                if session_filename == '0200-0203_061-Abdulaziz.cha':
                    return name + '1'
                elif session_filename == '0300-0303_144-Abdulaziz.cha':
                    return name + '2'
                else:
                    ValueError(err_msg.format(session_filename))
            elif name == 'Yousef':
                if session_filename == '0204-0207_087-Yousef.cha':
                    return name + '1'
                elif session_filename == '0204-0207_089-Yousef.cha':
                    return name + '2'
                elif session_filename == '0300-0303_141-Yousef.cha':
                    return name + '3'
                else:
                    ValueError(err_msg.format(session_filename))

        return name
