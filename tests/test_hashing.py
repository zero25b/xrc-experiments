from xrc_experiments.x11 import get_pow_hash_x11
from xrc_experiments.x13 import get_pow_hash_x13


def test_x11_hashing():
    assert get_pow_hash_x11(bytes('a' * 79, 'utf-8')).raw.hex() \
           == '2472e1a45e73061ab866536c8d0ceac8a84809b0f64f08d8fd0ade485c090491'

    assert get_pow_hash_x11(bytes('a' * 90, 'utf-8')).raw.hex()\
           == 'ea2d4e0a8b1bdab2cb9cfe29e60f66e4c8b7558d23854bb08a1ab56152ead1f1'


def test_x13_hashing():
    assert get_pow_hash_x13(bytes('a'*79, 'utf-8')).raw.hex()\
           == 'efb3a4dca8092b22a3785b11e105b9b87fac69b575782a82a96ad790786fa3f2'

    assert get_pow_hash_x13(bytes('a'*90, 'utf-8')).raw.hex() \
           == 'e202a3eb42ed84f1322025e782d3479adc3c3001226654e020bc0c50e2fc0708'
