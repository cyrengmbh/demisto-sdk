from demisto_sdk.commands.common.content import PackMetaData, ContentObjectFacotry

import pytest


@pytest.mark.parametrize(argnames="file", argvalues=["pack_metadata.json"])
def test_objects_factory(datadir, file: str):
    obj = ContentObjectFacotry.from_path(datadir[file])
    assert isinstance(obj, PackMetaData)


@pytest.mark.parametrize(argnames="file", argvalues=["pack_metadata.json"])
def test_prefix(datadir, file: str):
    obj = PackMetaData(datadir[file])
    assert obj._normalized_file_name() == "pack_metadata.json"
