from source.globals.color import Color

class Strings:
    text_str = {}
    text_fmt = {}
    STRUCT = {
        "HOST_SELECTION_TITLE",
        "HOST_SELECTION_TEXT",
        "SCRIPT_DESCRIPTION_INIT",
        "SCRIPT_DESCRIPTION_START",
        "SCRIPT_DESCRIPTION_STOPS",
        "SCRIPT_ARG_HELP_HOST",
        "SCRIPT_ARG_HELP_CLEANUP",
    }

    def init():
        Strings.text_str = dict.fromkeys(Strings.STRUCT, None)
        Strings.text_fmt = dict.fromkeys(Strings.STRUCT, None)

        Strings.text_str["HOST_SELECTION_TITLE"] = f'Host Selection: '
        Strings.text_str["HOST_SELECTION_TEXT"] = f'Which host do you want to select? (Input the number): '
        Strings.text_str["SCRIPT_DESCRIPTION_INIT"] = f'Initialize a host configuration.'
        Strings.text_str["SCRIPT_DESCRIPTION_START"] = f'Starts all the host services leveraging docker-compose.'
        Strings.text_str["SCRIPT_DESCRIPTION_STOPS"] = f'Stops all the host services'
        Strings.text_str["SCRIPT_ARG_HELP_HOST"] = f'The name of the host.'
        Strings.text_str["SCRIPT_ARG_HELP_CLEANUP"] = f'Resets the host back to its initial, service-less state.'

        Strings.text_fmt["HOST_SELECTION_TITLE"] = Color.text["type"]["underline"] + Strings.text_str["HOST_SELECTION_TITLE"] + Color.text["type"]["reset"]
        Strings.text_fmt["HOST_SELECTION_TEXT"] = Strings.text_str["HOST_SELECTION_TEXT"]
        Strings.text_fmt["SCRIPT_DESCRIPTION_INIT"] = Strings.text_str["SCRIPT_DESCRIPTION_INIT"]
        Strings.text_fmt["SCRIPT_DESCRIPTION_START"] = Strings.text_str["SCRIPT_DESCRIPTION_START"]
        Strings.text_fmt["SCRIPT_DESCRIPTION_STOPS"] = Strings.text_str["SCRIPT_DESCRIPTION_STOPS"]
        Strings.text_fmt["SCRIPT_ARG_HELP_HOST"] = Strings.text_str["SCRIPT_ARG_HELP_HOST"]
        Strings.text_fmt["SCRIPT_ARG_HELP_CLEANUP"] = Strings.text_str["SCRIPT_ARG_HELP_CLEANUP"]

    def get(attr):
        return Strings.text_fmt[attr]
    