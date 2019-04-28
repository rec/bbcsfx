import wave, numpy as np

DTYPES = {1: 'int8', 2: 'int16', 3: 'int8', 4: 'int32'}
OFFSET = 44
PARAMS = {'nchannels': 2,
          'sampwidth': 2,
          'framerate': 44100,
          'nframes': 0,
          'comptype': 'NONE',
          'compname': 'not compressed'}


def reader(filename):
    with wave.open(filename) as fp:
        params = fp.getparams()
    shape = _get_shape(params)
    dtype = DTYPES[params.sampwidth]
    return np.memmap(filename, dtype=dtype, offset=OFFSET, shape=shape)


def writer(filename, nframes, dtype='int16', **params):
    with wave.open(filename, mode='wb') as fp:
        params = dict(PARAMS, nframes=nframes, **params)
        max_size = 0x100000000 / params['nchannels'] / params['sampwidth']
        params['nframes'] = min(params['nframes'], int(max_size) - 1)
        wp = wave._wave_params(**params)
        fp.setparams(wp)
        shape = _get_shape(wp)

    return np.memmap(filename, dtype=dtype, offset=OFFSET, shape=shape)
