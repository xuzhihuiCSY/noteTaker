from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

KV = """
BoxLayout:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)

    MDLabel:
        text: "[size=50][b]Create Meeting Note[/b][/size]\\n[color=#8E8D8D]Create a meeting summary by recording your meeting audio[/color]"
        halign: "center"
        valign: "middle"
        markup: True
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]

    Widget:
        size_hint_y: None
        height: dp(20)

    BoxLayout:
        orientation: 'horizontal'
        size_hint: (None, None)
        width: self.minimum_width
        height: self.minimum_height
        pos_hint: {"center_x": 0.5}
        spacing: dp(10)

        MDRectangleFlatButton:
            id: record_button
            text: "Start Recording"
            on_release: app.toggle_recording()

    MDLabel:
        text: "Live Transcript:"
        bold: True
        halign: "left"
        pos_hint: {"center_x": 0.5}
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:
        MDLabel:
            id: transcript_label
            text: ""
            halign: "left"
            valign: "top"
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
            padding: dp(10), dp(10)
    
    Widget:
        size_hint_y: None
        height: dp(10)

    MDRectangleFlatButton:
        text: "Summarize"
        pos_hint: {"center_x": 0.5}
        on_release: app.summarize_transcript()

    MDLabel:
        text: "Summary:"
        bold: True
        halign: "left"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:
        MDLabel:
            id: summary_label
            text: ""
            halign: "left"
            valign: "top"
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
            padding: dp(10), dp(10)
            markup: True

    MDLabel:
        text: "Wikipedia Keywords (internet required):"
        bold: True
        halign: "left"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:
        MDLabel:
            id: wiki_label
            text: ""
            halign: "left"
            valign: "top"
            size_hint_y: None
            text_size: self.width, None
            height: self.texture_size[1]
            padding: dp(10), dp(10)
            markup: True
"""

class MainLayout(MDBoxLayout):
    """Any additional UI-related classes can be placed here if needed."""
    pass

def load_interface():
    """Return the Kivy layout to be used in the Kivy App."""
    return Builder.load_string(KV)
