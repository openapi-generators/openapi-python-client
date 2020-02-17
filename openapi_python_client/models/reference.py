import stringcase


class Reference:
    """ A reference to a class which will be in models """

    def __init__(self, ref: str):
        ref_value = ref.split("/")[-1]  # get the #/schemas/blahblah part off
        self.class_name: str = stringcase.pascalcase(ref_value)
        self.module_name: str = stringcase.snakecase(ref_value)
