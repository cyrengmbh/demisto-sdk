from pathlib import Path

from demisto_sdk.commands.common.content.content.objects.pack_objects import Integration
from demisto_sdk.commands.common.content.content.objects_factory import ContentObjectFacotry


class TestNotUnifiedIntegration:
    def test_objects_factory(self, datadir):
        obj = ContentObjectFacotry.from_path(datadir["sample.yml"])
        assert isinstance(obj, Integration)

    def test_prefix(self, datadir):
        obj = Integration(datadir["sample.yml"])
        assert obj._normalized_file_name() == "integration-sample.yml"

    def test_files_detection(self, datadir):
        obj = Integration(datadir["sample.yml"])
        assert obj.readme.path == Path(datadir["README.md"])
        assert obj.code_path == Path(datadir["sample.py"])
        assert obj.changelog.path == Path(datadir["CHANGELOG.md"])
        assert obj.description_path == Path(datadir["sample_description.md"])
        assert obj.png_path == Path(datadir["sample_image.png"])

    def test_is_unify(self, datadir):
        obj = Integration(datadir["sample.yml"])
        assert not obj.is_unify()


class TestUnifiedIntegration:
    def test_objects_factory(self, datadir):
        obj = ContentObjectFacotry.from_path(datadir["integration-sample.yml"])
        assert isinstance(obj, Integration)

    def test_prefix(self, datadir):
        obj = Integration(datadir["integration-sample.yml"])
        assert obj._normalized_file_name() == "integration-sample.yml"

    def test_files_detection(self, datadir):
        obj = Integration(datadir["integration-sample.yml"])
        assert obj.readme.path == Path(datadir["integration-sample_README.md"])
        assert obj.changelog.path == Path(datadir["integration-sample_CHANGELOG.md"])

    def test_is_unify(self, datadir):
        obj = Integration(datadir["integration-sample.yml"])
        assert obj.is_unify()