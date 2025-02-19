from travertino.size import at_least

from ..libs.android.view import View__MeasureSpec
from ..libs.android.widget import (
    CompoundButton__OnCheckedChangeListener,
    Switch as A_Switch,
)
from .label import TextViewWidget


class OnCheckedChangeListener(CompoundButton__OnCheckedChangeListener):
    def __init__(self, impl):
        super().__init__()
        self._impl = impl

    def onCheckedChanged(self, _button, _checked):
        self._impl.interface.on_change(None)


class Switch(TextViewWidget):
    focusable = False

    def create(self):
        self.native = A_Switch(self._native_activity)
        self.native.setOnCheckedChangeListener(OnCheckedChangeListener(self))
        self.cache_textview_defaults()

    def get_text(self):
        return str(self.native.getText())

    def set_text(self, text):
        # When changing the text, Android needs a `setSingleLine(False)` call in order
        # to be willing to recompute the width of the text. Without the call, it will
        # constrain the new text to have the same line width as the old text, resulting
        # in unnecessary creation of new lines. In other words, `setSingleLine(False)`
        # is required to get the text to truly **use** one single line!
        self.native.setSingleLine(False)
        self.native.setText(str(text))

    def get_value(self):
        return self.native.isChecked()

    def set_value(self, value):
        self.native.setChecked(bool(value))

    def rehint(self):
        if not self.native.getLayoutParams():
            return
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
