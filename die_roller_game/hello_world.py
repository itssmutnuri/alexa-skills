## Import statements
from random import randint

from ask_sdk_core.skill_builder import SkillBuilder

from ask_sdk_core.utils import is_request_type
from ask_sdk_model.ui import SimpleCard

from ask_sdk_core.utils import is_intent_name

## Instantiate Skill Builder object
sb = SkillBuilder()

## The following functions are implemented using decorators
## Reference: https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/DEVELOPING_YOUR_FIRST_SKILL.html#option-2-implementation-using-decorators

## Create LaunchRequest Handler
@sb.request_handler(can_handle_func = is_request_type('LaunchRequest'))
def launch_request_handler(handler_input):
    speech_text = 'Welcome to Dice Roller. You can roll a die or roll two dice.'

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard('Hello', speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response

## Create Request Handler for rolling one die.
@sb.request_handler(can_handle_func = is_intent_name('RollDieIntent'))
def roll_die_intent_handler(handler_input):
    speech_text = '<p>Rolling the die! </p>'

    result = randint(1,6)
    res_string = '<p>And it is a ' + str(result) + '!</p> Chance goes to the next player.'

    card_title = 'Rolling one die.'
    card_result = 'And it is a ' + str(result) + '! Chance goes to the next player.'

    handler_input.response_builder.speak(speech_text + res_string).set_card(
        SimpleCard(card_title, card_result)).set_should_end_session(
        False)
    return handler_input.response_builder.response

## Create Request Handler for rolling two dice.
@sb.request_handler(can_handle_func = is_intent_name('RollDiceIntent'))
def roll_dice_intent_handler(handler_input):
    speech_text = '<p>Rolling two dice! </p>'

    result = randint(2,12)
    res_string = '<p>And it is a ' + str(result) + '! </p>'

    card_title = 'Rolling two dice.'
    card_result = 'And it is a ' + str(result) + '! '

    if result in (2, 4, 6, 8, 10, 12):
        res_string = res_string + '<emphasis level="strong">Wow!</emphasis> Both the die got the same number. Roll again!'
        card_result += 'Wow! Both the die got the same number. Roll again!'
    else:
        res_string = res_string + 'Chance goes to the next player.'
        card_result += 'Chance goes to the next player.'

    handler_input.response_builder.speak(speech_text + res_string).set_card(
        SimpleCard(card_title, card_result)).set_should_end_session(
        False)
    return handler_input.response_builder.response

## Create HelpIntent Handler
@sb.request_handler(can_handle_func = is_intent_name('AMAZON.HelpIntent'))
def help_intent_handler(handler_input):
    #speech_text = 'You can ask me to either roll a die or roll two dice.'
    #speech_text = '''To roll one die, you can tell roll one or roll a die.
    #To roll two dice, you can tell roll two or roll two dice.
    #'''

    speech_text = 'You can ask me to roll one, roll two dice or roll a die. ' + \
    'Would you like to roll a die or two ?'

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard('Help', speech_text)).set_should_end_session(
        False)

    return handler_input.response_builder.response

## Create CancelAndStopIntent Handler
@sb.request_handler(
    can_handle_func = lambda input:
        is_intent_name('AMAZON.CancelIntent')(input) or
        is_intent_name('AMAZON.StopIntent')(input))
def cancel_and_stop_intent_handler(handler_input):
    speech_text = 'Goodbye! See you again for another match.'

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(speech_text))
    return handler_input.response_builder.response

## Create SessionEndedRequest Handler
@sb.request_handler(can_handle_func = is_request_type('SessionEndedRequest'))
def session_ended_handler(handler_input):

    return handler_input.response_builder.response

## Create Exception Handler
@sb.exception_handler(can_handle_func = lambda i, e: True)
def all_exception_handler(handler_input, exception):
    print(exception)

    speech = 'Sorry, I didn\' get that. Could you please say it again!'
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response

## Create lambda handler
handler = sb.lambda_handler()
