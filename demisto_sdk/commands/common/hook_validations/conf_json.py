import json

from demisto_sdk.commands.common.constants import CONF_PATH
from demisto_sdk.commands.common.errors import Errors
from demisto_sdk.commands.common.hook_validations.base_validator import \
    BaseValidator


class ConfJsonValidator(BaseValidator):
    """ConfJsonValidator has been designed to make sure we are following the standards for the conf.json file.

    Attributes:
        _is_valid (bool): Whether the conf.json file current state is valid or not.
        conf_data (dict): The data from the conf.json file in our repo.
    """
    CONF_PATH = "./Tests/conf.json"

    def __init__(self, ignored_errors=None, print_as_warnings=False, suppress_print=False):
        super().__init__(ignored_errors=ignored_errors, print_as_warnings=print_as_warnings,
                         suppress_print=suppress_print)
        self._is_valid = True
        self.conf_data = self.load_conf_file()

    def load_conf_file(self):
        with open(self.CONF_PATH) as data_file:
            return json.load(data_file)

    def is_valid_conf_json(self):
        """Validate the fields skipped_tests, skipped_integrations and unmockable_integrations in conf.json file."""
        print('\nValidating conf.json')
        skipped_tests_conf = self.conf_data['skipped_tests']
        skipped_integrations_conf = self.conf_data['skipped_integrations']
        unmockable_integrations_conf = self.conf_data['unmockable_integrations']

        self.is_valid_description_in_conf_dict(skipped_tests_conf)
        self.is_valid_description_in_conf_dict(skipped_integrations_conf)
        self.is_valid_description_in_conf_dict(unmockable_integrations_conf)

        return self._is_valid

    def is_valid_description_in_conf_dict(self, checked_dict):
        """Validate that the checked_dict has description for all it's fields.

        Args:
            checked_dict (dict): Dictionary from conf.json file.
        """
        problematic_instances = []
        for instance, description in checked_dict.items():
            if description == "":
                problematic_instances.append(instance)

        if problematic_instances:
            error_message, error_code = Errors.description_missing_from_conf_json(problematic_instances)
            if self.handle_error(error_message, error_code, file_path=CONF_PATH):
                self._is_valid = False

        return self._is_valid

    def is_test_in_conf_json(self, file_id):
        """Check if the file_id(We get this ID only if it is a test) is located in the tests section in conf.json file.

        Args:
            file_id (string): the ID of the test we are looking for in the conf.json file.

        Returns:
            bool. Whether the test as been located in the conf.json file or not.
        """
        conf_tests = self.conf_data['tests']
        for test in conf_tests:
            playbook_id = test['playbookID']
            if file_id == playbook_id:
                return True

        error_message, error_code = Errors.test_not_in_conf_json(file_id)
        if self.handle_error(error_message, error_code, file_path=CONF_PATH):
            return False
        return True
