from source.globals.color import Color

class Error:
    error_str = {}
    error_fmt = {}
    STRUCT = {
        "INPUT_NAN",
        "SCRIPT_ARG_HOST_NOT_EXIST",
    }

    def init():
        Error.error_str = dict.fromkeys(Error.STRUCT, None)
        Error.error_fmt = dict.fromkeys(Error.STRUCT, None)

        Error.error_str["INPUT_NAN"] = f'Invalid input. Please enter a valid number.'
        Error.error_str["SCRIPT_ARG_HOST_NOT_EXIST"] = f'The host does not exist. Please check for any typo.'

        Error.error_fmt["INPUT_NAN"] = Color.text["type"]["bold"] + Color.fore["bright"]["red"] + Error.error_str["INPUT_NAN"] + Color.text["type"]["reset"]
        Error.error_fmt["SCRIPT_ARG_HOST_NOT_EXIST"] = Color.text["type"]["bold"] + Color.fore["bright"]["red"] + Error.error_str["SCRIPT_ARG_HOST_NOT_EXIST"] + Color.text["type"]["reset"]

    def get(attr):
        return Error.error_fmt[attr]
    