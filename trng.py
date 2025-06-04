import os
import numpy as np
from PIL import Image
import random
from typing import List

class ChaosTRNG:
    def __init__(self, lambda_val: float = 4.0, L: int = 250, threshold: float = 0.5,
                 image_folder: str = "images", buffer_size_bytes: int = 1024 * 64):
        self.lambda_val = lambda_val
        self.L = L
        self.threshold = threshold
        self.image_folder = image_folder
        self.buffer_size_bits = buffer_size_bytes * 8
        self._bit_buffer: List[int] = []

        self.files = [f for f in os.listdir(self.image_folder)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
        if not self.files:
            raise RuntimeError(f"No images found in folder: {self.image_folder}")

        self._fill_buffer()

    def logistic_map(self, x0: float, length: int) -> np.ndarray:
        seq = np.empty(length + self.L, dtype=np.float32)
        seq[0] = x0
        for i in range(1, length + self.L):
            seq[i] = self.lambda_val * seq[i - 1] * (1 - seq[i - 1])
        return seq[self.L:]

    def generate_chaotic_sequences(self, length: int) -> np.ndarray:
        return np.array([self.logistic_map(iv, length) for iv in self.initial_values[1:9]], dtype=np.float32)

    def chaotic_sequence_to_bits(self, sequence: np.ndarray) -> np.ndarray:
        return (sequence >= self.threshold).astype(np.uint8)

    def process_image(self, image_path: str) -> np.ndarray:
        img = Image.open(image_path).convert('L').resize((128, 128))
        arr = np.array(img, dtype=np.uint8)
        M, N = arr.shape
        total_pixels = M * N

        seq0 = self.logistic_map(self.initial_values[0], total_pixels)
        idx = np.argsort(seq0)
        permuted = arr.flatten()[idx].reshape(M, N)

        flat_perm = permuted.flatten()
        bit_planes = ((flat_perm[:, None] >> np.arange(8)) & 1).T

        chaotic = self.generate_chaotic_sequences(total_pixels)
        chaotic_bits = (chaotic >= self.threshold).astype(np.uint8)

        mixed = np.bitwise_xor(bit_planes, chaotic_bits)
        return mixed.T.flatten()

    def _fill_buffer(self):
        self.initial_values = [random.uniform(0.35, 0.37) for _ in range(9)]

        self._bit_buffer.clear()
        random.shuffle(self.files)

        total_bits_needed = self.buffer_size_bits

        for fn in self.files:
            try:
                path = os.path.join(self.image_folder, fn)
                bits = self.process_image(path)
                self._bit_buffer.extend(bits)
                if len(self._bit_buffer) >= total_bits_needed:
                    break
            except Exception as e:
                print(f"Error processing image {fn}: {e}")
                continue

        if len(self._bit_buffer) < total_bits_needed:
            raise RuntimeError(f"Insufficient bits in buffer: {len(self._bit_buffer)} < {total_bits_needed}")

    def randbytes(self, n: int) -> bytes:
        needed_bits = n * 8
        if len(self._bit_buffer) < needed_bits:
            self._fill_buffer()
        bits = self._bit_buffer[:needed_bits]
        del self._bit_buffer[:needed_bits]
        return np.packbits(np.array(bits, dtype=np.uint8)).tobytes()
