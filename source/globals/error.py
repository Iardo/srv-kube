from source.globals.color import Color

class Error:
    INPUT_NAN: str = f'{Color.text["bold"]}{Color.fore["bright"]["red"]}Invalid input. Please enter a valid number.{Color.text["reset"]}'
    SCRIPT_ARG_HOST_NOT_EXIST = f'{Color.text["bold"]}{Color.fore["bright"]["red"]}The host does not exist. Please check for any typo.{Color.text["reset"]}'