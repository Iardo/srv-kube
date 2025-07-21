from source.head.color import *


class string:
    @staticmethod
    def to_bool(text: str):
        bool = text.lower()
        bool = True if bool == "true" else False
        return bool

    @staticmethod
    def color(text: str, fore: str = None, back: str = None, bold: bool = False, underline: bool = False):
        value_text = text if text else ''
        value_fore = fore if fore else ''
        value_back = back if back else ''
        value_bold = color.text["bold"] if bold else ''
        value_underline = color.text["underline"] if underline else ''
        value_reset = color.text["reset"]

        return(
            f'{value_bold}'
            f'{value_underline}'
            f'{value_back}'
            f'{value_fore}'
            f'{value_text}'
            f'{value_reset}'
        )
