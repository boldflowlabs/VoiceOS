"""Tests for Rumik TTS configuration registration and service factory."""

from types import SimpleNamespace
from api.services.configuration.registry import (
    RumikTTSConfiguration,
    ServiceProviders,
    RUMIK_TTS_MODELS,
    RUMIK_TTS_VOICES,
)
from api.services.pipecat.service_factory import create_tts_service


def test_rumik_tts_configuration_defaults():
    config = RumikTTSConfiguration()
    assert config.provider == ServiceProviders.RUMIK
    assert config.model == "mulberry"
    assert config.voice == "Emma"
    assert config.description is None
    assert RUMIK_TTS_MODELS == ["mulberry", "muga"]
    assert "Emma" in RUMIK_TTS_VOICES


def test_create_rumik_tts_service_passes_parameters(monkeypatch):
    monkeypatch.setenv("RUMIK_API_KEY", "test-rumik-key")
    user_config = SimpleNamespace(
        tts=RumikTTSConfiguration(
            model="muga",
            voice="Mia",
            description="Warm friendly voice",
            f0_up_key=2,
            temperature=0.7,
        )
    )

    service = create_tts_service(user_config, audio_config=None)
    assert service is not None
    assert service._api_key == "test-rumik-key"
    assert service._settings.model == "muga"
    assert service._settings.voice == "Mia"
    assert service._settings.description == "Warm friendly voice"
    assert service._settings.f0_up_key == 2
    assert service._settings.temperature == 0.7
    print("All Rumik TTS tests passed successfully!")


if __name__ == "__main__":
    test_rumik_tts_configuration_defaults()
    test_create_rumik_tts_service_passes_parameters(
        type("MonkeyPatch", (), {"setenv": lambda self, k, v: __import__("os").environ.update({k: v})})()
    )

