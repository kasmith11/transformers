# coding=utf-8
# Copyright 2022 The Fairseq Authors, Microsoft Research, and The HuggingFace Inc. team. All rights reserved.
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
""" SpeechT5 model configuration"""

import functools
import operator

from ...configuration_utils import PretrainedConfig
from ...utils import logging


logger = logging.get_logger(__name__)

SPEECHT5_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "TODO": "https://huggingface.co/TODO/resolve/main/config.json",
}


class SpeechT5Config(PretrainedConfig):
    r"""
    This is the configuration class to store the configuration of a [`SpeechT5Model`]. It is used to instantiate an
    SpeechT5 model according to the specified arguments, defining the model architecture. Instantiating a configuration
    with the defaults will yield a similar configuration to that of the SpeechT5 [TODO](https://huggingface.co/TODO)
    architecture.

    Configuration objects inherit from [`PretrainedConfig`] and can be used to control the model outputs. Read the
    documentation from [`PretrainedConfig`] for more information.


    Args:
        vocab_size (`int`, *optional*, defaults to 81):
            Vocabulary size of the SpeechT5 model. Defines the number of different tokens that can be represented by
            the `inputs_ids` passed to the forward method of [`SpeechT5Model`].
        hidden_size (`int`, *optional*, defaults to 768):
            Dimensionality of the encoder layers and the pooler layer.
        encoder_layers (`int`, *optional*, defaults to 12):
            Number of hidden layers in the Transformer encoder.
        encoder_attention_heads (`int`, *optional*, defaults to 12):
            Number of attention heads for each attention layer in the Transformer encoder.
        encoder_ffn_dim (`int`, *optional*, defaults to 3072):
            Dimensionality of the "intermediate" (i.e., feed-forward) layer in the Transformer encoder.
        encoder_layerdrop (`float`, *optional*, defaults to 0.1):
            The LayerDrop probability for the encoder. See the [LayerDrop paper](see https://arxiv.org/abs/1909.11556)
            for more details.
        decoder_layers (`int`, *optional*, defaults to 6):
            Number of decoder layers.
        decoder_attention_heads (`int`, *optional*, defaults to 12):
            Number of attention heads for each attention layer in the Transformer decoder.
        decoder_ffn_dim (`int`, *optional*, defaults to 3072):
            Dimensionality of the "intermediate" (often named feed-forward) layer in decoder.
        decoder_layerdrop (`float`, *optional*, defaults to 0.1):
            The LayerDrop probability for the decoder. See the [LayerDrop paper](see https://arxiv.org/abs/1909.11556)
            for more details.
        hidden_act (`str` or `function`, *optional*, defaults to `"gelu"`):
            The non-linear activation function (function or string) in the encoder and pooler. If string, `"gelu"`,
            `"relu"`, `"selu"` and `"gelu_new"` are supported.
        positional_dropout (`float`, *optional*, defaults to 0.1):
            The dropout probability for the text position encoding layers.
        hidden_dropout (`float`, *optional*, defaults to 0.1):
            The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.
        attention_dropout (`float`, *optional*, defaults to 0.1):
            The dropout ratio for the attention probabilities.
        activation_dropout (`float`, *optional*, defaults to 0.1):
            The dropout ratio for activations inside the fully connected layer.
        final_dropout (`float`, *optional*, defaults to 0.1):
            The dropout probability for the final projection layer of [`SpeechT5ForCTC`].
        initializer_range (`float`, *optional*, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        layer_norm_eps (`float`, *optional*, defaults to 1e-5):
            The epsilon used by the layer normalization layers.
        scale_embedding (`bool`, *optional*, defaults to `False`):
            Scale embeddings by diving by sqrt(d_model).
        feat_extract_norm (`str`, *optional*, defaults to `"group"`):
            The norm to be applied to 1D convolutional layers in the speech encoder pre-net. One of `"group"` for group
            normalization of only the first 1D convolutional layer or `"layer"` for layer normalization of all 1D
            convolutional layers.
        feat_proj_dropout (`float`, *optional*, defaults to 0.0):
            The dropout probability for output of the speech encoder pre-net.
        feat_extract_activation (`str, `optional`, defaults to `"gelu"`):
            The non-linear activation function (function or string) in the 1D convolutional layers of the feature
            extractor. If string, `"gelu"`, `"relu"`, `"selu"` and `"gelu_new"` are supported.
        conv_dim (`Tuple[int]` or `List[int]`, *optional*, defaults to `(512, 512, 512, 512, 512, 512, 512)`):
            A tuple of integers defining the number of input and output channels of each 1D convolutional layer in the
            speech encoder pre-net. The length of *conv_dim* defines the number of 1D convolutional layers.
        conv_stride (`Tuple[int]` or `List[int]`, *optional*, defaults to `(5, 2, 2, 2, 2, 2, 2)`):
            A tuple of integers defining the stride of each 1D convolutional layer in the speech encoder pre-net. The
            length of *conv_stride* defines the number of convolutional layers and has to match the length of
            *conv_dim*.
        conv_kernel (`Tuple[int]` or `List[int]`, *optional*, defaults to `(10, 3, 3, 3, 3, 3, 3)`):
            A tuple of integers defining the kernel size of each 1D convolutional layer in the speech encoder pre-net.
            The length of *conv_kernel* defines the number of convolutional layers and has to match the length of
            *conv_dim*.
        conv_bias (`bool`, *optional*, defaults to `False`):
            Whether the 1D convolutional layers have a bias.
        num_conv_pos_embeddings (`int`, *optional*, defaults to 128):
            Number of convolutional positional embeddings. Defines the kernel size of 1D convolutional positional
            embeddings layer.
        num_conv_pos_embedding_groups (`int`, *optional*, defaults to 16):
            Number of groups of 1D convolutional positional embeddings layer.
        apply_spec_augment (`bool`, *optional*, defaults to `True`):
            Whether to apply *SpecAugment* data augmentation to the outputs of the speech encoder pre-net. For
            reference see [SpecAugment: A Simple Data Augmentation Method for Automatic Speech
            Recognition](https://arxiv.org/abs/1904.08779).
        mask_time_prob (`float`, *optional*, defaults to 0.05):
            Percentage (between 0 and 1) of all feature vectors along the time axis which will be masked. The masking
            procecure generates ''mask_time_prob*len(time_axis)/mask_time_length'' independent masks over the axis. If
            reasoning from the propability of each feature vector to be chosen as the start of the vector span to be
            masked, *mask_time_prob* should be `prob_vector_start*mask_time_length`. Note that overlap may decrease the
            actual percentage of masked vectors. This is only relevant if `apply_spec_augment is True`.
        mask_time_length (`int`, *optional*, defaults to 10):
            Length of vector span along the time axis.
        mask_time_min_masks (`int`, *optional*, defaults to 2),:
            The minimum number of masks of length `mask_feature_length` generated along the time axis, each time step,
            irrespectively of `mask_feature_prob`. Only relevant if ''mask_time_prob*len(time_axis)/mask_time_length <
            mask_time_min_masks''
        mask_feature_prob (`float`, *optional*, defaults to 0.0):
            Percentage (between 0 and 1) of all feature vectors along the feature axis which will be masked. The
            masking procecure generates ''mask_feature_prob*len(feature_axis)/mask_time_length'' independent masks over
            the axis. If reasoning from the propability of each feature vector to be chosen as the start of the vector
            span to be masked, *mask_feature_prob* should be `prob_vector_start*mask_feature_length`. Note that overlap
            may decrease the actual percentage of masked vectors. This is only relevant if `apply_spec_augment is
            True`.
        mask_feature_length (`int`, *optional*, defaults to 10):
            Length of vector span along the feature axis.
        mask_feature_min_masks (`int`, *optional*, defaults to 0),:
            The minimum number of masks of length `mask_feature_length` generated along the feature axis, each time
            step, irrespectively of `mask_feature_prob`. Only relevant if
            ''mask_feature_prob*len(feature_axis)/mask_feature_length < mask_feature_min_masks''
        num_mel_bins (`int`, *optional*, defaults to 80):
            Number of mel features used per input features. Used by the speech decoder pre-net.
            Should correspond to the value used in the `SpeechT5Processor` class.
        speech_decoder_prenet_units (`int`, *optional*, defaults to 256):
            Dimensionality of the layers in the speech decoder pre-net.
        speech_decoder_prenet_dropout (`float`, *optional*, defaults to 0.5):
            The dropout probability for the speech decoder pre-net layers.
        speaker_embedding_dim (`int`, *optional*, defaults to 512):
            Dimensionality of the *XVector* embedding vectors.
        max_speech_positions (`int`, *optional*, defaults to 4000):
            The maximum sequence length of speech features that this model might ever be used with.
        max_text_positions (`int`, *optional*, defaults to 450):
            The maximum sequence length of text features that this model might ever be used with.
        encoder_max_relative_position (`int`, *optional*, defaults to 160):
            Maximum distance for relative position embedding in the encoder.
        decoder_max_relative_position (`int`, *optional*, defaults to 160):
            Maximum distance for relative position embedding in the dencoder.
        ctc_loss_reduction (`str`, *optional*, defaults to `"sum"`):
            Specifies the reduction to apply to the output of `torch.nn.CTCLoss`. Only relevant when training an
            instance of [`SpeechT5ForCTC`].
        ctc_zero_infinity (`bool`, *optional*, defaults to `False`):
            Whether to zero infinite losses and the associated gradients of `torch.nn.CTCLoss`. Infinite losses mainly
            occur when the inputs are too short to be aligned to the targets. Only relevant when training an instance
            of [`SpeechT5ForCTC`].
        use_cache (`bool`, *optional*, defaults to `True`):
            Whether or not the model should return the last key/values attentions (not used by all models).

    Example:

    ```python
    >>> from transformers import SpeechT5Model, SpeechT5Config

    >>> # Initializing a SpeechT5 TODO style configuration
    >>> configuration = SpeechT5Config()

    >>> # Initializing a model from the TODO style configuration
    >>> model = SpeechT5Model(configuration)

    >>> # Accessing the model configuration
    >>> configuration = model.config
    ```"""
    model_type = "speecht5"

    def __init__(
        self,
        vocab_size=81,
        hidden_size=768,
        encoder_layers=12,
        encoder_attention_heads=12,
        encoder_ffn_dim=3072,
        encoder_layerdrop=0.1,
        decoder_layers=6,
        decoder_ffn_dim=3072,
        decoder_attention_heads=12,
        decoder_layerdrop=0.1,
        hidden_act="gelu",
        positional_dropout=0.1,
        hidden_dropout=0.1,
        attention_dropout=0.1,
        activation_dropout=0.1,
        final_dropout=0.1,
        initializer_range=0.02,
        layer_norm_eps=1e-5,
        scale_embedding=False,
        feat_extract_norm="group",
        feat_proj_dropout=0.0,
        feat_extract_activation="gelu",
        conv_dim=(512, 512, 512, 512, 512, 512, 512),
        conv_stride=(5, 2, 2, 2, 2, 2, 2),
        conv_kernel=(10, 3, 3, 3, 3, 2, 2),
        conv_bias=False,
        num_conv_pos_embeddings=128,
        num_conv_pos_embedding_groups=16,
        apply_spec_augment=True,
        mask_time_prob=0.05,
        mask_time_length=10,
        mask_time_min_masks=2,
        mask_feature_prob=0.0,
        mask_feature_length=10,
        mask_feature_min_masks=0,
        pad_token_id=1,
        bos_token_id=0,
        eos_token_id=2,
        decoder_start_token_id=2,
        num_mel_bins=80,
        speech_decoder_prenet_units=256,
        speech_decoder_prenet_dropout=0.5,
        speaker_embedding_dim=512,
        max_speech_positions=4000,
        max_text_positions=450,
        encoder_max_relative_position=160,
        decoder_max_relative_position=160,
        ctc_loss_reduction="sum",
        ctc_zero_infinity=False,
        use_cache=True,
        is_encoder_decoder=True,
        **kwargs
    ):
        super().__init__(
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            is_encoder_decoder=is_encoder_decoder,
            decoder_start_token_id=decoder_start_token_id,
            **kwargs,
        )

        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.encoder_layers = encoder_layers
        self.encoder_ffn_dim = encoder_ffn_dim
        self.encoder_attention_heads = encoder_attention_heads
        self.encoder_layerdrop = encoder_layerdrop
        self.decoder_layers = decoder_layers
        self.decoder_ffn_dim = decoder_ffn_dim
        self.decoder_attention_heads = decoder_attention_heads
        self.decoder_layerdrop = decoder_layerdrop
        self.hidden_act = hidden_act
        self.positional_dropout = positional_dropout
        self.hidden_dropout = hidden_dropout
        self.attention_dropout = attention_dropout
        self.activation_dropout = activation_dropout
        self.final_dropout = final_dropout
        self.initializer_range = initializer_range
        self.layer_norm_eps = layer_norm_eps
        self.scale_embedding = scale_embedding

        self.feat_extract_norm = feat_extract_norm
        self.feat_proj_dropout = feat_proj_dropout
        self.feat_extract_activation = feat_extract_activation
        self.conv_dim = list(conv_dim)
        self.conv_stride = list(conv_stride)
        self.conv_kernel = list(conv_kernel)
        self.conv_bias = conv_bias
        self.num_conv_pos_embeddings = num_conv_pos_embeddings
        self.num_conv_pos_embedding_groups = num_conv_pos_embedding_groups
        self.num_feat_extract_layers = len(self.conv_dim)

        if (
            (len(self.conv_stride) != self.num_feat_extract_layers)
            or (len(self.conv_kernel) != self.num_feat_extract_layers)
            or (len(self.conv_dim) != self.num_feat_extract_layers)
        ):
            raise ValueError(
                "Configuration for convolutional layers is incorrect. It is required that `len(config.conv_dim)` =="
                " `len(config.conv_stride)` == `len(config.conv_kernel)`, but is `len(config.conv_dim) ="
                f" {len(self.conv_dim)}`, `len(config.conv_stride) = {len(self.conv_stride)}`,"
                f" `len(config.conv_kernel) = {len(self.conv_kernel)}`."
            )

        # fine-tuning config parameters for SpecAugment: https://arxiv.org/abs/1904.08779
        self.apply_spec_augment = apply_spec_augment
        self.mask_time_prob = mask_time_prob
        self.mask_time_length = mask_time_length
        self.mask_time_min_masks = mask_time_min_masks
        self.mask_feature_prob = mask_feature_prob
        self.mask_feature_length = mask_feature_length
        self.mask_feature_min_masks = mask_feature_min_masks

        self.num_mel_bins = num_mel_bins
        self.speech_decoder_prenet_units = speech_decoder_prenet_units
        self.speech_decoder_prenet_dropout = speech_decoder_prenet_dropout
        self.speaker_embedding_dim = speaker_embedding_dim

        # ctc loss
        self.ctc_loss_reduction = ctc_loss_reduction
        self.ctc_zero_infinity = ctc_zero_infinity

        self.max_speech_positions = max_speech_positions
        self.max_text_positions = max_text_positions
        self.encoder_max_relative_position = encoder_max_relative_position
        self.decoder_max_relative_position = decoder_max_relative_position
        self.use_cache = use_cache
        self.is_encoder_decoder = is_encoder_decoder

    def inputs_to_logits_ratio(self):
        return functools.reduce(operator.mul, self.conv_stride, 1)