import pytest
from demisto_sdk.commands.common.content import Classifier, ContentObjectFacotry


@pytest.mark.parametrize(argnames="file", argvalues=["sample.json", "classifier-sample.json"])
def test_objects_factory(datadir, file: str):
    obj = ContentObjectFacotry.from_path(datadir[file])
    assert isinstance(obj, Classifier)


def test_prefix(datadir):
    obj = Classifier(datadir['sample.json'])
    assert obj._normalized_file_name() == "classifier-sample.json"
