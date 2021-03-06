from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import unittest
from unittest import skip

from future import standard_library
from mock.mock import MagicMock
from parameterized import parameterized

from cloudomate.exceptions.vps_out_of_stock import VPSOutOfStockException
from cloudomate.hoster.vps.blueangelhost import BlueAngelHost
from cloudomate.hoster.vps.ccihosting import CCIHosting
from cloudomate.hoster.vps.hostsailor import HostSailor
# from cloudomate.hoster.vps.libertyvps import LibertyVPS
from cloudomate.hoster.vps.libertyvps import LibertyVPS
from cloudomate.hoster.vps.linevast import LineVast
from cloudomate.hoster.vps.orangewebsite import OrangeWebsite
# from cloudomate.hoster.vps.pulseservers import Pulseservers
from cloudomate.hoster.vps.qhoster import QHoster
from cloudomate.hoster.vps.routerhosting import RouterHosting
from cloudomate.hoster.vps.twosync import TwoSync
from cloudomate.hoster.vps.undergroundprivate import UndergroundPrivate
from cloudomate.util.fakeuserscraper import UserScraper
from cloudomate.util.settings import Settings

standard_library.install_aliases()

# Only the ones that currently work are uncommented
providers = [
    #(BlueAngelHost,),
    #(CCIHosting,),
    #(HostSailor,),
    #(LibertyVPS,),
    (LineVast,),
    #(OrangeWebsite,),
    # (Pulseservers,),
    (QHoster,)
    #(RouterHosting,),
    #(TwoSync,),
    #(UndergroundPrivate,),
    # (CrownCloud,), Manually checking orders results in being banned after running tests
    # (UndergroundPrivate,),# find a way to combine the url and the invoice to be able to go to the payment page
]


class TestHosters(unittest.TestCase):
    @parameterized.expand(providers)
    def test_hoster_options(self, hoster):
        options = hoster.get_options()
        self.assertTrue(len(options) > 0)

    @parameterized.expand(providers)
    @unittest.skipIf(len(sys.argv) >= 2 and sys.argv[1] == 'discover', 'Integration tests have to be run manually')
    @skip('These tests relies on webscraping and form filling of vps pages. these pages change and therefore these '
          'tests are currently to unreliable')
    def test_hoster_purchase(self, hoster):
        user_settings = Settings()
        self._merge_random_user_data(user_settings)

        host = hoster(user_settings)
        options = list(host.get_options())[0]
        wallet = MagicMock()
        wallet.pay = MagicMock()

        try:
            host.purchase(wallet, options)
            wallet.pay.assert_called_once()
        except VPSOutOfStockException as exception:
            self.skipTest(exception)

    @staticmethod
    def _merge_random_user_data(user_settings):
        usergenerator = UserScraper()
        randomuser = usergenerator.get_user()
        for section in randomuser.keys():
            for key in randomuser[section].keys():
                user_settings.put(section, key, randomuser[section][key])


if __name__ == '__main__':
    unittest.main()
