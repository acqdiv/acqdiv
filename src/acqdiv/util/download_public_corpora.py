import io
import shutil
import zipfile
from pathlib import Path
import requests

corpora_dir = Path('corpora')
if corpora_dir.exists():
    shutil.rmtree(corpora_dir)

corpora_dir.mkdir()

tmp_dir = corpora_dir / 'downloaded'

childes_corpora_links = {
    'Cree': 'https://phonbank.talkbank.org/data/Other/Cree/CCLAS.zip',
    'English_Manchester1': 'https://childes.talkbank.org/data/Eng-UK/Manchester.zip',
    'Japanese_MiiPro': 'https://childes.talkbank.org/data/Japanese/MiiPro.zip',
    'Japanese_Miyata': 'https://childes.talkbank.org/data/Japanese/Miyata.zip',
    'Nungon': 'https://childes.talkbank.org/data/Other/Nungon/Sarvasy.zip',
    'Sesotho': 'https://childes.talkbank.org/data/Other/Sesotho/Demuth.zip'
}

for corpus, childes_corpus_link in childes_corpora_links.items():
    print(f'Downloading {corpus}...')

    # where the data is downloaded to
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir()

    # where the corpus data is placed
    corpus_dir = corpora_dir / corpus
    corpus_dir.mkdir()
    cha_dir = corpus_dir / 'cha'
    cha_dir.mkdir()

    # download zip file
    response = requests.get(childes_corpus_link)
    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall(path=tmp_dir)

    downloaded_corpus_dir = tmp_dir / Path(childes_corpus_link).with_suffix('').name

    for tc_name_dir in downloaded_corpus_dir.iterdir():
        if tc_name_dir.is_dir():
            for cha_file in tc_name_dir.glob('*.cha'):
                shutil.copyfile(
                    cha_file,
                    cha_dir / f'{tc_name_dir.name}_{cha_file.name}'
                )

shutil.rmtree(tmp_dir)
