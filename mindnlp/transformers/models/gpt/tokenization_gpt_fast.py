# coding=utf-8
# Copyright 2018 The Open AI Team Authors and The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Fast Tokenization classes for OpenAI GPT."""


from typing import Optional, Tuple

from mindnlp.utils import logging
from ...tokenization_utils_fast import PreTrainedTokenizerFast
from .tokenization_gpt import GPTTokenizer


logger = logging.get_logger(__name__)

VOCAB_FILES_NAMES = {"vocab_file": "vocab.json", "merges_file": "merges.txt", "tokenizer_file": "tokenizer.json"}

PRETRAINED_VOCAB_FILES_MAP = {
    "vocab_file": {"openai-gpt": "https://hf-mirror.com/openai-gpt/resolve/main/vocab.json"},
    "merges_file": {"openai-gpt": "https://hf-mirror.com/openai-gpt/resolve/main/merges.txt"},
    "tokenizer_file": {"openai-gpt": "https://hf-mirror.com/openai-gpt/resolve/main/tokenizer.json"},
}

PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES = {
    "openai-gpt": 512,
}


class GPTTokenizerFast(PreTrainedTokenizerFast):
    """
    Construct a "fast" GPT Tokenizer (backed by HuggingFace's *tokenizers* library). Based on Byte-Pair-Encoding with
    the following peculiarities:

    - lower case all inputs
    - uses BERT's BasicTokenizer for pre-BPE tokenization

    This tokenizer inherits from [`PreTrainedTokenizerFast`] which contains most of the main methods. Users should
    refer to this superclass for more information regarding those methods.

    Args:
        vocab_file (`str`):
            Path to the vocabulary file.
        merges_file (`str`):
            Path to the merges file.
        unk_token (`str`, *optional*, defaults to `"<unk>"`):
            The unknown token. A token that is not in the vocabulary cannot be converted to an ID and is set to be this
            token instead.
    """
    vocab_files_names = VOCAB_FILES_NAMES
    pretrained_vocab_files_map = PRETRAINED_VOCAB_FILES_MAP
    max_model_input_sizes = PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES
    model_input_names = ["input_ids", "attention_mask"]
    slow_tokenizer_class = GPTTokenizer

    def __init__(self, vocab_file=None, merges_file=None, tokenizer_file=None, unk_token="<unk>", **kwargs):
        """
        Initialize a GPTTokenizerFast object.

        Args:
            vocab_file (str): Path to the vocabulary file. Default is None.
            merges_file (str): Path to the merges file. Default is None.
            tokenizer_file (str): Path to the tokenizer file. Default is None.
            unk_token (str): The token to represent unknown words. Default is '<unk>'.
            **kwargs: Additional keyword arguments.

        Returns:
            None.

        Raises:
            None.
        """
        super().__init__(vocab_file, merges_file, tokenizer_file=tokenizer_file, unk_token=unk_token, **kwargs)

    @property
    def do_lower_case(self):
        """
        Method 'do_lower_case' in the class 'GPTTokenizerFast'.

        Args:
            self: This parameter refers to the instance of the class itself.
                It is required for accessing the object's attributes and methods.

        Returns:
            True: This method always returns a boolean value of True indicating that lowercasing is enabled.

        Raises:
            None.
        """
        return True

    def save_vocabulary(self, save_directory: str, filename_prefix: Optional[str] = None) -> Tuple[str]:
        """
        Save the vocabulary files generated by the GPTTokenizerFast instance to the specified directory.

        Args:
            self (GPTTokenizerFast): The GPTTokenizerFast instance.
            save_directory (str): The directory where the vocabulary files will be saved.
            filename_prefix (Optional[str]): An optional prefix to be added to the filenames of the vocabulary files.
                Default is None.

        Returns:
            Tuple[str]: A tuple containing the filenames of the saved vocabulary files.

        Raises:
            None.

        This method saves the vocabulary files generated by the GPTTokenizerFast instance to the specified directory.
        The save_directory parameter should be a valid directory path. If filename_prefix is provided,
        it will be added as a prefix to the filenames of the vocabulary files.
        The method returns a tuple containing the filenames of the saved vocabulary files.
        """
        files = self._tokenizer.model.save(save_directory, name=filename_prefix)
        return tuple(files)

__all__ = ['GPTTokenizerFast']
