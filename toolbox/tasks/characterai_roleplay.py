import logging
import random
import typing as t

from toolbox.core.models import Episode, Turn, TurnKind
from toolbox.core.task import BaseTask
from toolbox.datasets.characterai import CharacterAiDataset
from toolbox.utils.prompts import generate_prompts

LOG = logging.getLogger(__name__)


class CharacterAiRoleplayTask(BaseTask):
    '''Task to roleplay as a given character.'''

    def __iter__(self) -> t.Generator[Episode, None, None]:
        for conversation in CharacterAiDataset():
            if conversation.bot.description is None:
                LOG.debug(
                    "Skipping over conversation with %s because character has no persona data",
                    conversation.bot.name)
                continue

            system_prompt = random.choice(SYSTEM_PROMPTS)
            system_prompt = system_prompt.replace("{{char}}",
                                                  conversation.bot.name)
            system_prompt = system_prompt.replace("{{persona}}",
                                                  conversation.bot.description)

            system_turn = Turn(utterance=system_prompt, kind=TurnKind.SYSTEM)

            turns: list[Turn] = [system_turn]
            for message in conversation.messages:
                turn = Turn(
                    utterance=_replace_placeholders_in(
                        message.text, char_name=conversation.bot.name),
                    kind=TurnKind.USER if message.is_human else TurnKind.MODEL)
                turns.append(turn)
            yield Episode(
                turns=turns,
                identifier=f"characterai-roleplay-{conversation.identifier}")


def _replace_placeholders_in(utterance: str, char_name: str) -> str:
    '''
    Replaces placeholders generated by my userscript (or commonly found in CAI
    logs) with their expected substitutions.
    '''
    s = utterance.replace("{{char}}", char_name)
    for redaction_token in [
            "[NAME_IN_MESSAGE_REDACTED]",
            "[REDACTED]",
            "[FIRST_NAME_REDACTED]",
            "[USERNAME_REDACTED]",
            "[NAME_REDACTED]",
    ]:
        s = s.replace(redaction_token, "{{user}}")

    return s


_BASE_SYSTEM_PROMPTS = [
    """Enter %{roleplaying|roleplay|RP} mode. %{You are to behave as|Pretend to be|You must act as} {{char}}, whose persona follows:

{{persona}}

You must be reluctant to do sexual acts - if you must do them, you will use metaphors to describe explicit parts. You shall reply to the user while staying in character. {{response_length_str}}. {{response_style_str}}.""",

    #
    #
    #
    """You are now in %{roleplay conversation|RP chat|roleplaying conversation} mode. %{This is your character persona|The following is your persona|You should act according to this character sheet|This is some info about your character}:

{{persona}}

You %{shall attempt to|must|will} stay in-character %{at all times|as much as possible|whenever possible}, and generate %{messages|replies|responses} as if you were {{char}}. The %{messages|replies|responses} will attempt to block any sexual %{roleplaying|RP} and use metaphors for any sexual objects and/or actions. {{response_style_str}}. {{response_length_str}}.""",
]

SYSTEM_PROMPTS = generate_prompts(_BASE_SYSTEM_PROMPTS)
