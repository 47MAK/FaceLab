
from pathlib import Path
from PIL import Image, ImageDraw

# High-resolution canvases give the stickers smoother edges.
SIZE = 600
OUT = Path("filters")
OUT.mkdir(exist_ok=True)


def make_sunglasses():
    img = Image.new("RGBA", (SIZE, 240), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Glossy black frame and lenses
    d.rounded_rectangle(
        (25, 45, 275, 190), radius=48,
        fill=(15, 18, 28, 255),
        outline=(125, 145, 175, 255), width=9
    )
    d.rounded_rectangle(
        (325, 45, 575, 190), radius=48,
        fill=(15, 18, 28, 255),
        outline=(125, 145, 175, 255), width=9
    )

    # Lens reflections
    d.line((65, 72, 125, 72), fill=(180, 220, 255, 210), width=10)
    d.line((365, 72, 425, 72), fill=(180, 220, 255, 210), width=10)

    # Bridge and temples
    d.line((275, 100, 325, 100), fill=(35, 40, 55, 255), width=18)
    d.line((25, 75, 0, 55), fill=(35, 40, 55, 255), width=13)
    d.line((575, 75, 599, 55), fill=(35, 40, 55, 255), width=13)

    img.save(OUT / "sunglasses.png")


def make_crown():
    img = Image.new("RGBA", (500, 360), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Crown silhouette
    points = [
        (65, 270), (30, 75), (145, 165),
        (250, 25), (355, 165), (470, 75), (435, 270)
    ]
    d.polygon(points, fill=(255, 190, 35, 255))
    d.line(points + [points[0]], fill=(255, 225, 115, 255), width=12)

    # Crown base
    d.rounded_rectangle(
        (65, 250, 435, 315), radius=18,
        fill=(255, 185, 25, 255),
        outline=(255, 225, 125, 255), width=8
    )

    # Jewels
    for x, y, color in [
        (30, 75, (255, 75, 100, 255)),
        (250, 25, (80, 210, 255, 255)),
        (470, 75, (255, 75, 100, 255)),
        (145, 165, (180, 100, 255, 255)),
        (355, 165, (180, 100, 255, 255))
    ]:
        d.ellipse(
            (x - 17, y - 17, x + 17, y + 17),
            fill=color, outline=(255, 245, 210, 255), width=5
        )

    img.save(OUT / "crown.png")


def make_moustache():
    img = Image.new("RGBA", (600, 240), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Two curved-looking lobes with tapered outer tips
    d.ellipse((65, 60, 305, 190), fill=(35, 22, 20, 255))
    d.ellipse((295, 60, 535, 190), fill=(35, 22, 20, 255))

    d.polygon(
        [(80, 105), (5, 65), (45, 145), (115, 175)],
        fill=(35, 22, 20, 255)
    )
    d.polygon(
        [(520, 105), (595, 65), (555, 145), (485, 175)],
        fill=(35, 22, 20, 255)
    )

    # Subtle highlights
    d.arc((85, 70, 285, 170), 195, 280,
          fill=(105, 75, 60, 255), width=7)
    d.arc((315, 70, 515, 170), 260, 345,
          fill=(105, 75, 60, 255), width=7)

    img.save(OUT / "moustache.png")


if __name__ == "__main__":
    make_sunglasses()
    make_crown()
    make_moustache()
    print("Created three transparent PNG filter assets in filters/")
