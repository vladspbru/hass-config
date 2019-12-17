"""
Support for the RHVoice tts  service.
"""
import asyncio
import logging

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.components.tts import Provider, PLATFORM_SCHEMA, CONF_LANG
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv


_LOGGER = logging.getLogger(__name__)

SUPPORT_VOICES = [
    'aleksandr', 'anna', 'elena', 'irina', # Russian
    'alan', 'bdl', 'clb', 'slt', # English
    'spomenka', # Esperanto
    'natia', # Georgian
    'azamat', 'nazgul', # Kyrgyz
    'talgat', # Tatar
    'anatol' # Ukrainian
]

CONF_VOICE = 'voice'
CONF_API_URL = 'url'

DEFAULT_VOICE = 'anna'
DEFAULT_LANG = 'ru-RU'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_URL): cv.string,
    vol.Optional(CONF_VOICE, default=DEFAULT_VOICE): vol.In(SUPPORT_VOICES)
})

SUPPORT_LANGUAGES = [
    'ru-RU'
]


SUPPORTED_OPTIONS = [
    CONF_VOICE
]


@asyncio.coroutine
def async_get_engine(hass, config):
    """Set up RHVoice speech component."""
    return RHVoiceProvider(hass, config)


class RHVoiceProvider(Provider):
    """RHVoice speech api provider."""

    def __init__(self, hass, conf):
        """Init RHVoice TTS service."""
        self.hass = hass
        self._url = conf.get(CONF_API_URL)
        self._voice = conf.get(CONF_VOICE)
        self._language = DEFAULT_LANG
        self._codec = 'mp3'
        self.name = 'RHVoice'

    @property
    def default_language(self):
        """Return the default language."""
        return self._language

    @property
    def supported_languages(self):
        """Return list of supported languages."""
        return SUPPORT_LANGUAGES

    @property
    def supported_options(self):
        """Return list of supported options."""
        return SUPPORTED_OPTIONS

    @asyncio.coroutine
    def async_get_tts_audio(self, message, language, options=None):
        """Load TTS from RHVoice."""
        websession = async_get_clientsession(self.hass)
        options = options or {}

        try:
            with async_timeout.timeout(10, loop=self.hass.loop):
                url_param = {
                    'text': message,
                    'voice': options.get(CONF_VOICE, self._voice)
                }

                request = yield from websession.get(
                    self._url, params=url_param)

                if request.status != 200:
                    _LOGGER.error("Error %d on load URL %s",
                                  request.status, request.url)
                    return (None, None)
                data = yield from request.read()

        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for RHVoice API")
            return (None, None)

        return (self._codec, data)