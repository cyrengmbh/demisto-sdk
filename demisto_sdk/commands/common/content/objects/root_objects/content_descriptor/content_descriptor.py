from typing import Union

from demisto_sdk.commands.common.content.objects.base_objects.common import \
    FileDumpMixin
from demisto_sdk.commands.common.content.objects.base_objects.json_file import \
    JsonFile
from wcmatch.pathlib import Path


class ContentDescriptor(JsonFile, FileDumpMixin):
    def __init__(self, path: Union[Path, str]):
        super(JsonFile).__init__(path=path)
