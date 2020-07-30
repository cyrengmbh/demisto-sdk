from pathlib import Path

from demisto_sdk.commands.common.content.content.objects.abstract_objects import YAMLContentObject
from demisto_sdk.commands.common.tools import path_test_files

TEST_DATA = path_test_files()
TEST_CONTENT_REPO = TEST_DATA / 'content_slim'
TEST_YAML_NO_FROM_VERSION = TEST_CONTENT_REPO / 'Packs' / 'Sample01' / 'Scripts' / 'script-sample_new.yml'
TEST_YAML_NO_TO_VERSION = TEST_CONTENT_REPO / 'Packs' / 'Sample01' / 'Scripts' / 'script-sample_packs.yml'


def test_from_version_no_to_version(datadir):
    from packaging.version import parse
    obj = YAMLContentObject(TEST_YAML_NO_TO_VERSION, "script")
    assert obj.from_version == parse("6.0.0")
    assert obj.to_version == parse("99.99.99")


def test_to_version_no_from_version(datadir):
    from packaging.version import parse
    obj = YAMLContentObject(TEST_YAML_NO_FROM_VERSION, "script")
    assert obj.from_version == parse("0.0.0")
    assert obj.to_version == parse("5.0.0")


class TestFileWithStem:
    def test_with_readme_change_log(self):
        obj = YAMLContentObject(TEST_YAML_NO_FROM_VERSION, "script")

        assert obj.readme is not None
        assert obj.changelog is not None

    def test_without_readme_changelog(self):
        obj = YAMLContentObject(TEST_YAML_NO_TO_VERSION, "script")

        assert obj.readme is None
        assert obj.changelog is None
