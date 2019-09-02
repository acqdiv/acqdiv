import re


def unify_timestamp(timestamp_raw):
    """Unify the time stamp.

    Takes the time position in the session recording in the format
    `HH:MM:SS.mmmm` and returns the equivalent in seconds and
    milliseconds.

    Args:
        timestamp_raw (str): The original timestamp of an utterance.

    Returns:
        str: The timestamp in seconds and milliseconds.
    """
    if not timestamp_raw:
        return ''
    times = re.match(r'(\d+):(\d+):(\d+)\.?(\d+)?', timestamp_raw)
    if times:
        fields = times.lastindex
        if fields == 4:
            seconds = int(
                        times.group(1)) * 3600 \
                      + int(times.group(2)) * 60 \
                      + int(times.group(3))
            msecs = times.group(4)
            return "{0}.{1}".format(seconds, msecs)
        elif fields == 3:
            times = re.match(r'(\d+):(\d+):(\d+)', timestamp_raw)
            if times:
                seconds = int(
                            times.group(1)) * 3600 \
                          + int(times.group(2)) * 60 \
                          + int(times.group(3))
                return "{0}.000".format(seconds)
        else:
            return ''
    else:
        return timestamp_raw
