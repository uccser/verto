import sys, unittest, optparse
from collections import defaultdict

from kordac.tests.SmokeTests import SmokeFileTest, SmokeDocsTest
from kordac.tests.ConfigurationTest import ConfigurationTest
from kordac.tests.GlossaryLinkTest import GlossaryLinkTest
from kordac.tests.PanelTest import PanelTest
from kordac.tests.CommentTest import CommentTest
from kordac.tests.HeadingTest import HeadingTest
from kordac.tests.ImageTest import ImageTest
from kordac.tests.VideoTest import VideoTest
from kordac.tests.InteractiveTest import InteractiveTest
from kordac.tests.ButtonLinkTest import ButtonLinkTest
from kordac.tests.BoxedTextTest import BoxedTextTest
from kordac.tests.SaveTitleTest import SaveTitleTest
from kordac.tests.RemoveTitleTest import RemoveTitleTest
from kordac.tests.RelativeLinkTest import RelativeLinkTest

def parse_args():
    opts = optparse.OptionParser(
        usage='Run the command `python -m kordac.tests.start_tests` from the level above the kordac directory.', description="Verifies that Kordac is functional compared to the testing suite.")
    opts.add_option('--travis',
        action='store_true', help='Enables skipping suites on failure. To be used by continuous integration system.', default=False)
    opts.add_option('--no_smoke',
        action='store_true', help='Skips smoke tests, should be used for local development only.', default=False)
    opts.add_option('--no_system',
        action='store_true', help='Skips system tests, should be used for local development only.', default=False)
    opts.add_option('--no_unit',
        action='store_true', help='Skips unit tests, should be used for local development only.', default=False)
    options, arguments = opts.parse_args()

    return options, arguments

def smoke_suite():
    return unittest.TestSuite((
        unittest.makeSuite(SmokeDocsTest),
        unittest.makeSuite(SmokeFileTest),
    ))

def system_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ConfigurationTest)
    ))

def unit_suite():
    # NTS what order should these go in?
    return unittest.TestSuite((
        unittest.makeSuite(SaveTitleTest),
        unittest.makeSuite(RemoveTitleTest),
        # unittest.makeSuite(GlossaryLinkTest), # order of tests by cmp()
        unittest.makeSuite(PanelTest),
        unittest.makeSuite(CommentTest),
        unittest.makeSuite(HeadingTest),
        unittest.makeSuite(ImageTest),
        unittest.makeSuite(RelativeLinkTest),
        # unittest.makeSuite(VideoTest),
        # unittest.makeSuite(InteractiveTest),
        unittest.makeSuite(ButtonLinkTest),
        unittest.makeSuite(BoxedTextTest)
    ))


if __name__ == '__main__':
    options, arguments = parse_args()

    runner = unittest.TextTestRunner()

    smoke_result = None
    if not options.no_smoke:
        print("Running Smoke Tests")
        smoke_result = runner.run(smoke_suite())
        print()

    if options.travis and smoke_result and not smoke_result.wasSuccessful():
        print("Skipping other test-suites.")
        sys.exit(1)
        print()

    system_result = None
    if not options.no_system:
        print("Running System Tests")
        system_result = runner.run(system_suite())
        print()

    unit_result = None
    if not options.no_unit:
        print("Running Unit Tests")
        unit_result = runner.run(unit_suite())
        print()

    if (smoke_result is not None and not system_result.wasSuccessful()) or (system_result is not None and not system_result.wasSuccessful()) or (unit_result is not None and not unit_result.wasSuccessful()):
        sys.exit(1)
