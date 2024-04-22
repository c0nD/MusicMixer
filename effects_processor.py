# effects_processor.py

import os
import zipfile
from pydub import AudioSegment
import shutil
import numpy as np
from fx import apply_random_effects

def audiosegment_to_float_array(segment):
    if segment.channels != 1:
        segment = segment.set_channels(1)
    raw_data = segment.raw_data
    array_type = np.float32 if segment.sample_width == 4 else np.int16
    audio_array = np.frombuffer(raw_data, dtype=array_type)
    if array_type == np.int16:
        audio_array = audio_array.astype(np.float32) / 32768.0
    return audio_array


def float_array_to_audiosegment(array, sample_rate):
    int_array = (array * 32768).astype(np.int16)
    audio_segment = AudioSegment(
        int_array.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )
    return audio_segment

class EffectsProcessor:
    def __init__(self, zip_path: str, output_folder: str, output_format: str = 'wav', num_variants: int = 5):
        self.zip_path = zip_path
        self.output_folder = output_folder
        self.output_format = output_format.lower().lstrip('.')
        self.temp_folder = 'temp_audio_files'
        self.num_variants = num_variants

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

    def extract_audio(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_folder)
            print(f'Extracted audio to {self.temp_folder}')

    def convert_audio_files(self):
        for filename in os.listdir(self.temp_folder):
            if not filename.endswith(self.output_format):
                original_path = os.path.join(self.temp_folder, filename)
                try:
                    sound = AudioSegment.from_file(original_path)
                    new_file = os.path.splitext(original_path)[0] + '.' + self.output_format
                    new_path = os.path.join(self.temp_folder, new_file)
                    sound.export(new_path, format=self.output_format)
                    os.remove(original_path)
                    print(f'Converted {filename} to {self.output_format}')
                except Exception as e:
                    print(f'Error converting {filename}: {e}')

    def apply_effects_and_save(self):
        for filename in os.listdir(self.temp_folder):
            if filename.lower().endswith(self.output_format):
                for variant in range(self.num_variants):
                    try:
                        sound = AudioSegment.from_file(os.path.join(self.temp_folder, filename))
                        sr = sound.frame_rate
                        audio_array = audiosegment_to_float_array(sound)
                        processed_audio_array = apply_random_effects(audio_array, sr)
                        processed_sound = float_array_to_audiosegment(processed_audio_array, sr)
                        variant_filename = os.path.splitext(filename)[0] + f'_variant{variant}.' + self.output_format
                        variant_path = os.path.join(self.output_folder, variant_filename)
                        processed_sound.export(variant_path, format=self.output_format)
                        print(f'Processed and saved {variant_filename}')
                    except Exception as e:
                        print(f"Error processing {filename}: {e}")


    def cleanup(self):
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)
            print(f'Cleaned up temporary folder: {self.temp_folder}')


    def process(self):
        self.extract_audio()
        self.convert_audio_files()
        self.apply_effects_and_save()
        self.cleanup()

if __name__ == '__main__':
    zip_path = 'test_set.zip'
    output_folder = 'processed_audio'
    processor = EffectsProcessor(zip_path, output_folder, num_variants=10)
    processor.process()
