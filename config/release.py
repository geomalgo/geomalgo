def configure(conf):
    conf.options.install_python_path = True
    conf.options.cython_flags = "-X " + ','.join([
        'boundscheck=False',
        'cdivision=True',
        'wraparound=False',
        'initializedcheck=False',
        'language_level=3',
    ])
