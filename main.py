# Text Extraction imports
import easyocr
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

# Translation imports
from googletrans import Translator

# Grammar checker imports
import language_tool_python as langtool
from textblob import TextBlob

# AI tools imports
from llm import contextualize_text_snippets

# Other imports
import os
import json
import numpy as np
from enum import Enum
from typing import List, Dict, DefaultDict, Tuple
from collections import defaultdict
from tqdm import tqdm

type BBox = List[List[np.int32, np.int32]]
type InfoItem = BBox | str | np.float64
type ImageInfo = Dict[str, InfoItem]


class Language(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    VIETNAMESE = "vi"
    # Visit https://github.com/JaidedAI/EasyOCR for more details on supported languages


ORIGINAL_IMAGE_PATH = os.path.join(os.getcwd(), "original_images")
TRANSLATED_IMAGE_PATH = os.path.join(os.getcwd(), "translated_images")


class TranslatOCR:
    def __init__(
        self,
        lang_src: str = Language.SPANISH,
        lang_dst: str = Language.ENGLISH,
        font: str = "DejaVuSansMono.ttf",
        font_size: int = 12,
        is_dynamic_font_size: bool = False,
        is_GPU_enabled: bool = True,
    ):
        self.reader = easyocr.Reader(
            [lang_src.value, lang_dst.value], gpu=is_GPU_enabled
        )
        self.translator = Translator()
        self.grammar_checker = langtool.LanguageTool("en-US")
        self.lang_src = lang_src
        self.lang_dst = lang_dst
        self.extracted_info: DefaultDict[str, List[ImageInfo]] = defaultdict(list)
        self.font = font
        self.font_size = font_size
        self.is_dynamic_font_size = is_dynamic_font_size
        self.is_GPU_enabled = is_GPU_enabled

    def process_images(self, file_name: str) -> None:
        file_path = os.path.join(ORIGINAL_IMAGE_PATH, file_name)
        if os.path.isfile(file_path):
            self.extract_image_info(file_name)
        else:
            print(f"{file_name} not found")

    def update_images(self) -> None:
        for image_path, image_info in tqdm(
            self.extracted_info.items(), desc="Updating images"
        ):
            self.draw_translated_text(image_path, image_info)

    def set_language_settings(self, lang_src: Language, lang_dst: Language) -> None:
        self.reader = easyocr.Reader(
            [lang_src.value, lang_dst.value], gpu=self.is_GPU_enabled
        )
        self.lang_src = lang_src
        self.lang_dst = lang_dst

    def extract_image_info(self, file_name: str) -> None:
        image_path = os.path.join(ORIGINAL_IMAGE_PATH, file_name)
        results = self.reader.readtext(image_path)

        for bbox, text, prob in tqdm(results, desc="Extracting text"):
            if text == "" or text is None:
                print("No text found in the image: ", file_name)
                continue

            translated_text = self.translator.translate(
                text, src=self.lang_src.value, dest=self.lang_dst.value
            ).text

            self.extracted_info[file_name].append(
                {
                    "bbox": bbox,
                    "original_text": text,
                    "translated_text": translated_text,
                    "prob": prob,
                }
            )

    def contexualize_files(self) -> Dict[str, str]:
        context = {}
        for file_name, image_info in tqdm(
            self.extracted_info.items(), desc="Contexualizing text"
        ):
            text_snippets = [item_info["translated_text"] for item_info in image_info]
            json_snippets = json.dumps(text_snippets, indent=4)
            contextualized_snippets = contextualize_text_snippets(json_snippets)
            formatted_contextualized_snippets = contextualized_snippets.replace(
                r"\n", "\n"
            )
            context[file_name] = formatted_contextualized_snippets
        return context

    def correct_text(self, text: str) -> str:
        spell_checked_text = TextBlob(text).correct()
        grammar_checked_text = langtool.utils.correct(
            spell_checked_text, self.grammar_checker.check(str(spell_checked_text))
        )
        return grammar_checked_text

    def draw_translated_text(self, file_name: str, image_info: List[ImageInfo]) -> None:
        image_path = os.path.join(ORIGINAL_IMAGE_PATH, file_name)
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        for info in tqdm(image_info, desc="Drawing translated text"):
            bbox = info["bbox"]
            translated_text = info["translated_text"]

            top_left = tuple(bbox[0])
            bottom_right = tuple(bbox[2])
            draw.rectangle([top_left, bottom_right], fill="white")

            box_width = bottom_right[0] - top_left[0]
            box_height = bottom_right[1] - top_left[1]

            if self.is_dynamic_font_size:
                self.font_size = self.calculate_font_size(
                    box_width, box_height, translated_text
                )

            font = ImageFont.truetype(self.font, self.font_size)

            text_width, text_height = self.get_text_size(font, translated_text)
            text_x = top_left[0] + (box_width - text_width) // 2
            text_y = top_left[1] + (box_height - text_height) // 2

            draw.text((text_x, text_y), translated_text, fill="black", font=font)

        base_name, ext = os.path.splitext(file_name)
        translated_file_name = f"{base_name}_translated{ext}"
        translated_image_path = os.path.join(
            TRANSLATED_IMAGE_PATH, translated_file_name
        )
        image.save(translated_image_path)

    def calculate_font_size(self, box_width, box_height, text):
        font_size = min(box_height, box_width)
        font = ImageFont.truetype(self.font, font_size)
        text_width, text_height = self.get_text_size(font, text)

        while text_width > box_width or text_height > box_height:
            font_size -= 1
            font = ImageFont.truetype(self.font, font_size)
            text_width, text_height = self.get_text_size(font, text)

        return font_size

    def get_text_size(self, font: FreeTypeFont, text: str) -> Tuple[float, float]:
        font_bbox = font.getbbox(text)
        text_width = font_bbox[2] - font_bbox[0]
        text_height = font_bbox[3] - font_bbox[1]
        return text_width, text_height


if __name__ == "__main__":
    translatOCR = TranslatOCR()
    image_info = [
        ("english_meme.jpg", Language.ENGLISH, Language.VIETNAMESE),
        ("spanish_bible_1.png", Language.SPANISH, Language.ENGLISH),
        ("spanish_bible_2.png", Language.SPANISH, Language.ENGLISH),
        ("french_menu_1.png", Language.FRENCH, Language.ENGLISH),
        ("french_menu_2.png", Language.FRENCH, Language.ENGLISH),
        ("french_traffic_sign.webp", Language.FRENCH, Language.ENGLISH),
    ]

    for file_name, lang_src, lang_dst in tqdm(image_info, desc="Processing images"):
        translatOCR.set_language_settings(lang_src, lang_dst)
        translatOCR.process_images(file_name)
        translatOCR.update_images()

    file_context = translatOCR.contexualize_files()
    output_file_name = "context.txt"
    with open(output_file_name, "a") as file:
        for file_name, context in file_context.items():
            file.write(f"Context for file: {file_name}:\n")
            file.write(context + "\n\n")
