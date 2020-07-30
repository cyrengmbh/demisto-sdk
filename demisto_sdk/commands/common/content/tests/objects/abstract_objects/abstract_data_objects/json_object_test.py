from pathlib import Path
import pytest

from demisto_sdk.commands.common.content.content.objects.abstract_objects import JSONObject
from demisto_sdk.commands.common.tools import path_test_files

TEST_DATA = path_test_files()
TEST_CONTENT_REPO = TEST_DATA / 'content_slim'
TEST_VALID_JSON = TEST_CONTENT_REPO / 'Packs' / 'Sample01' / 'Classifiers' / 'classifier-sample_new.json'
TEST_NOT_VALID_JSON = path_test_files() / 'malformed.json'


class TestValidJSON:
    def test_valid_json_file_path(self):
        from json import load
        obj = JSONObject(TEST_VALID_JSON)

        assert obj.to_dict() == load(TEST_VALID_JSON.open())

    def test_get_item(self):
        from json import load
        obj = JSONObject(TEST_VALID_JSON)

        assert obj["fromVersion"] == load(TEST_VALID_JSON.open())["fromVersion"]

    @pytest.mark.parametrize(argnames="default_value", argvalues=["test_value", ""])
    def test_get(self, default_value: str):
        from json import load
        obj = JSONObject(TEST_VALID_JSON)

        if default_value:
            assert obj.get("no such key", default_value) == default_value
        else:
            assert obj["fromVersion"] == load(TEST_VALID_JSON.open())["fromVersion"]

    def test_dump(self):
        from json import load
        from pathlib import Path
        expected_file = Path(TEST_VALID_JSON).parent / f'prefix-{TEST_VALID_JSON.name}'
        obj = JSONObject(TEST_VALID_JSON, "prefix")
        assert obj.dump()[0] == expected_file
        assert obj.to_dict() == load(expected_file.open())
        expected_file.unlink()


class TestInValidJSON:
    def test_malformed_json_data_file_path(self):
        obj = JSONObject(TEST_NOT_VALID_JSON)
        with pytest.raises(BaseException) as excinfo:
            obj.to_dict()
        assert "is not valid json file, Full error" in str(excinfo)

    def test_malformed_json_path(self):
        with pytest.raises(BaseException) as excinfo:
            JSONObject('Not valid path')

        assert "Unable to find json file in path" in str(excinfo)
