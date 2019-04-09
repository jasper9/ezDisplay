import time
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)

small_font = cwd+"/fonts/Arial-12.bdf"
#medium_font = cwd+"/fonts/Arial-16.bdf"
large_font = cwd+"/fonts/Arial-Bold-24.bdf"
xxl_font = cwd+"/fonts/Helvetica-Bold-100.bdf"

class ezDisplay(displayio.Group):
    def __init__(self, root_group, *, am_pm=True, celsius=True):
        super().__init__(max_size=2)
        self.am_pm = am_pm

        root_group.append(self)
        #self._icon_group = displayio.Group(max_size=1)
        #self.append(self._icon_group)
        self._text_group = displayio.Group(max_size=5)
        self.append(self._text_group)

        #self._icon_sprite = None
        #self._icon_file = None
        #self.set_icon(cwd+"/weather_background.bmp")

        self.small_font = bitmap_font.load_font(small_font)
        # self.medium_font = bitmap_font.load_font(medium_font)
        self.large_font = bitmap_font.load_font(large_font)
        self.xxl_font = bitmap_font.load_font(xxl_font)
        
        glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: °'

        self.small_font.load_glyphs(glyphs)
        #self.medium_font.load_glyphs(glyphs)

        self.large_font.load_glyphs(glyphs)
        self.large_font.load_glyphs(('°',))  # a non-ascii character we need for sure

        self.xxl_font.load_glyphs(glyphs)
        self.xxl_font.load_glyphs(('°',))  # a non-ascii character we need for sure

        #self.city_text = None

        self.time_text = Label(self.large_font, max_glyphs=8)
        self.time_text.x = 200
        self.time_text.y = 24
        self.time_text.color = 0xFFFFFF
        self._text_group.append(self.time_text)

        self.temp_text = Label(self.xxl_font, max_glyphs=6)
        #self.temp_text = Label(self.large_font, max_glyphs=6)
        self.temp_text.x = 40
        self.temp_text.y = 100
        self.temp_text.color = 0xFFFFFF
        self._text_group.append(self.temp_text)

        # self.val2_text = Label(self.large_font, max_glyphs=20)
        # self.val2_text.x = 10
        # self.val2_text.y = 195
        # self.val2_text.color = 0xFFFFFF
        # self._text_group.append(self.val2_text)

        # self.main_text = Label(self.large_font, max_glyphs=20)
        # self.main_text.x = 10
        # self.main_text.y = 195
        # self.main_text.color = 0xFFFFFF
        # self._text_group.append(self.main_text)

        self.description_text = Label(self.small_font, max_glyphs=60)
        self.description_text.x = 10
        self.description_text.y = 225
        self.description_text.color = 0xFFFFFF
        self._text_group.append(self.description_text)

    def display_value(self, value, description, suffix, num_digits):
        self.update_time()
        self.temp_text.text = str(round(float(value), num_digits)) + suffix
        #self.temp_text.text = value
        self.description_text.text = description

    def update_time(self):
        """Fetch the time.localtime(), parse it out and update the display text"""
        now = time.localtime()
        hour = now[3]
        minute = now[4]
        format_str = "%d:%02d"
        if self.am_pm:
            if hour >= 12:
                hour -= 12
                format_str = format_str+" PM"
            else:
                format_str = format_str+" AM"
            if hour == 0:
                hour = 12
        time_str = format_str % (hour, minute)
        print(time_str)
        self.time_text.text = time_str
