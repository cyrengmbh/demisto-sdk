from __future__ import print_function

from unittest.mock import patch

from demisto_sdk.commands.test_content.mock_server import (AMIConnection,
                                                           clean_filename,
                                                           get_folder_path,
                                                           get_log_file_path,
                                                           get_mock_file_path)


def test_clean_filename():
    assert clean_filename(u'th)))i(s) is a (test8)8   8') == 'th___i_s__is_a__test8_8___8'
    assert clean_filename(u'n&%ew $r#eplac@es', replace='&%$#@') == 'n__ew _r_eplac_es'


def test_get_paths():
    test_playbook_id = u'test_playbook'
    assert get_mock_file_path(test_playbook_id) == 'test_playbook/test_playbook.mock'
    assert get_log_file_path(test_playbook_id) == 'test_playbook/test_playbook_playback.log'
    assert get_log_file_path(test_playbook_id, record=True) == 'test_playbook/test_playbook_record.log'
    assert get_folder_path(test_playbook_id) == 'test_playbook/'


def test_ami():
    with patch('demisto_sdk.commands.test_content.mock_server.AMIConnection.check_output') as mock:
        mock.return_value = b"""
        eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 9001
            inet 2.2.2.2  netmask 255.255.240.0  broadcast 172.31.63.255
            inet6 fe80::c9d:ccff:fe7f:1e91  prefixlen 64  scopeid 0x20<link>
            ether 0e:9d:cc:7f:1e:91  txqueuelen 1000  (Ethernet)
            RX packets 37051  bytes 47117967 (44.9 MiB)
            RX errors 0  dropped 0  overruns 0  frame 0
            TX packets 26025  bytes 28722186 (27.3 MiB)
            TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0"""

        ami = AMIConnection('1.1.1.1')
        assert ami.public_ip == '1.1.1.1'
        assert ami.internal_ip == '2.2.2.2'
