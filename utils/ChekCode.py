import base64
import os
import random
import string
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw, ImageFilter

from AIR_System.settings import BASE_DIR


class CheckCode():
    def __init__(self):
        self.font_path = os.path.join(BASE_DIR, "utils", "timesbi.ttf")
        print(self.font_path)
        self.number = 4
        self.size = (100, 30)
        self.backgroundcolor = (255, 255, 255)
        self.fontcolor = (0, 0, 255)
        self.linecolor = (255, 0, 0)
        self.draw_line = True
        self.isTwist = True
        self.line_count = 20
        self.text = ''

    def _generate_text(self):
        source = list(string.ascii_letters)
        for index in range(0, 10):
            source.append(str(index))
        self.text = "".join(random.sample(source, self.number))

    def _gene_line(self, width, height, draw):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=self.linecolor)

    def gene_code(self, imagename_or_io, format):
        width, height = self.size
        img = Image.new("RGBA", (width, height), self.backgroundcolor)
        font = ImageFont.truetype(self.font_path, 25)
        draw = ImageDraw.Draw(img)
        self._generate_text()
        font_width, font_height = font.getsize(self.text)
        draw.text(((width - font_width) / self.number, (height - font_height) / self.number), self.text, font=font,
                  fill=self.fontcolor)
        if self.draw_line:
            for i in range(self.line_count):
                self._gene_line(width, height, draw)
        if self.isTwist:
            img = img.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)
        # this is for make the picture shows fuzzy.
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        if format:
            img.save(imagename_or_io, format=format)
            # print("saved to io%s"%io.getvalue().decode())
        else:
            img.save(imagename_or_io)
        return self.text

    def get_pass_code_base64(self):
        io = BytesIO()
        pass_code = self.gene_code(io, format="PNG")
        base64_data = base64.b64encode(io.getvalue())
        io.close()
        return pass_code, "data:image/png;base64,%s" % base64_data.decode()


if __name__ == '__main__':
    code = CheckCode()
    # print(code.gene_code("x.png"))
    # print(code.get_base64())
