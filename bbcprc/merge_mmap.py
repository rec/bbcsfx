"""
Merges many .WAV files into one great big one and keeps track of the sample
offset for each one.
"""

import numpy as np, yaml
from pathlib import Path
from . elapsed_bar import ElapsedBar
from . import constants, wave_to_numpy
from numpy.lib.format import open_memmap

STOP_AFTER = None or 5
TOTAL_FRAMES = 76522480090


def merge_to_mmap(mmap, files, total_frames):
    shape = total_frames, 2
    writer = open_memmap(mmap, mode='w+', dtype='int16', shape=shape)
    bar = ElapsedBar(max=len(files))
    frames = 0

    for f in files:
        yield f, frames
        bar.next_item(Path(f).name)
        reader = wave_to_numpy.reader(f)
        nsamples, nchannels = reader.shape
        if nchannels == 1:
            reader = np.repeat(reader, 2, axis=1)
        elif nchannels != 2:
            raise ValueError
        writer[frames:frames + nsamples] = reader
        frames += nsamples

    yield '(END)', frames
    bar.finish()


def sorted_files():
    def g():
        for i, f in enumerate(yaml.safe_load_all(open('results/census.yml'))):
            yield f['nframes'], f['filename']

    return [f for (_, f) in sorted(g())][:STOP_AFTER]


def merge():
    results = merge_to_mmap(constants.CORPUS, sorted_files(), TOTAL_FRAMES)
    with open(constants.CORPUS_INDEX, 'w') as out:
        yaml.safe_dump_all(results, out)


if __name__ == '__main__':
    merge()
