# Ini files

This directory contains the corpus-specific ini configuration files for processing.

It also contains a `role_mapping.ini` file that maps speaker roles to a standardized subset of of roles, e.g. 

Baltazar = Research_Team
Collector/Annotator = Research_Team
Collector/annotator = Research_Team

which we use in postprocessing.

Lastly, we have also have a `session_durations.csv` file that maps session ids and source_ids to session durations, which we generate from corpus media file directly using this script:

https://github.com/uzling/acqdiv-misc/tree/master/scripts/media_metadata

Note that must be updated when new data points are added. To check the deltas in duration:

`select corpus, min(duration), max(duration) from sessions group by corpus`

To eyeball outliers:

`select * from sessions order by duration desc`

Current coverage:

`select corpus, min(duration), max(duration) from sessions group by corpus`

Chintang,473
Indonesian,931
Japanese_MiiPro,148
Japanese_Miyata,76
Russian,437
Sesotho,67
Turkish,370
Yucatec,11