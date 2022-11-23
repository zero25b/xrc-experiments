from xrc_utils.digishield import target_to_bits, get_targetDigishield, bits_to_target, \
    read_header


if __name__ == '__main__':

    assert target_to_bits(get_targetDigishield(154999)) == read_header(154999)['bits']
    assert target_to_bits(get_targetDigishield(155100)) == read_header(155100)['bits']
    assert target_to_bits(get_targetDigishield(155200)) == read_header(155200)['bits']

    assert get_targetDigishield(154999) == bits_to_target(read_header(154999)['bits'])
    assert get_targetDigishield(155100) == bits_to_target(read_header(155100)['bits'])
    assert get_targetDigishield(155200) == bits_to_target(read_header(155200)['bits'])
