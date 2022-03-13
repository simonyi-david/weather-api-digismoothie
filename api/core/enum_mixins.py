

class GetEnumByLabelMixin:

    @classmethod
    def get_by_label(cls, label):
        try:
            attr = getattr(cls, label).value
            return attr
        except AttributeError:
            raise NotImplementedError(f"Missing definition for label: {label}")
