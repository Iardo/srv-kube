from source.globals.color import Color

class Text:
    HOST_SELECTION_TITLE: str = f'{Color.text["underline"]}Host Selection:{Color.text["reset"]}'
    HOST_SELECTION_TEXT: str = f'Which host do you want to select? (Input the number): '
    SCRIPT_DESCRIPTION_INIT: str = f'Initialize a host configuration.'
    SCRIPT_DESCRIPTION_START: str = f'Starts all the host services leveraging docker-compose.'
    SCRIPT_DESCRIPTION_STOPS: str = f'Stops all the host services'
    SCRIPT_ARG_HELP_HOST: str = f'The name of the host.'
    