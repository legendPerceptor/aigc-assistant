import daft
import base64
from pathlib import Path
from typing import Optional, Iterator
from openai import OpenAI
from config import get_settings
import concurrent.futures
import numpy as np
from numpy.typing import NDArray

settings = get_settings()
client = OpenAI(api_key=settings.openai_api_key)


class ImageProcessor:
    def __init__(self):
        self.vision_model = settings.openai_vision_model
        self.embedding_model = settings.openai_embedding_model

    def encode_image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def analyze_image(self, image_path: str) -> dict:
        base64_image = self.encode_image_to_base64(image_path)

        response = client.chat.completions.create(
            model=self.vision_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请详细描述这张图片的内容，包括：主体对象、场景、色彩、风格、情感氛围等。用中文回答，简洁明了。",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            max_tokens=500,
        )

        description = response.choices[0].message.content
        return {
            "description": description,
            "model": self.vision_model,
        }

    def generate_embedding(self, text: str) -> list[float]:
        response = client.embeddings.create(model=self.embedding_model, input=text)
        return response.data[0].embedding

    def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        response = client.embeddings.create(model=self.embedding_model, input=texts)
        return [item.embedding for item in response.data]

    def process_single_image(self, image_path: str) -> dict:
        analysis = self.analyze_image(image_path)
        embedding = self.generate_embedding(analysis["description"])

        return {
            "description": analysis["description"],
            "embedding": embedding,
            "model": analysis["model"],
        }


class BatchImageProcessor:
    def __init__(self, max_workers: int = 4):
        self.image_processor = ImageProcessor()
        self.max_workers = max_workers

    def create_image_dataframe(self, image_paths: list[str]) -> daft.DataFrame:
        df = daft.from_pydict({"image_path": image_paths})
        return df

    def process_single_with_path(self, image_path: str) -> dict:
        try:
            result = self.image_processor.process_single_image(image_path)
            result["image_path"] = image_path
            result["status"] = "success"
        except Exception as e:
            result = {
                "image_path": image_path,
                "status": "error",
                "error": str(e),
                "description": None,
                "embedding": None,
            }
        return result

    def process_batch_with_daft(self, image_paths: list[str]) -> Iterator[dict]:
        for path in image_paths:
            yield self.process_single_with_path(path)

    def process_batch_parallel(self, image_paths: list[str]) -> list[dict]:
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_path = {
                executor.submit(self.process_single_with_path, path): path
                for path in image_paths
            }
            for future in concurrent.futures.as_completed(future_to_path):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    path = future_to_path[future]
                    results.append({
                        "image_path": path,
                        "status": "error",
                        "error": str(e),
                        "description": None,
                        "embedding": None,
                    })
        return results

    def process_directory(
        self, directory_path: str, extensions: Optional[list[str]] = None, parallel: bool = True
    ) -> list[dict]:
        if extensions is None:
            extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]

        directory = Path(directory_path)
        image_paths = []
        for ext in extensions:
            image_paths.extend(directory.glob(f"*{ext}"))
            image_paths.extend(directory.glob(f"*{ext.upper()}"))

        image_paths = [str(p) for p in image_paths]

        if parallel:
            return self.process_batch_parallel(image_paths)
        return list(self.process_batch_with_daft(image_paths))

    def create_analysis_dataframe(self, results: list[dict]) -> daft.DataFrame:
        data = {
            "image_path": [],
            "description": [],
            "embedding": [],
            "status": [],
        }
        for r in results:
            data["image_path"].append(r.get("image_path"))
            data["description"].append(r.get("description"))
            data["embedding"].append(r.get("embedding"))
            data["status"].append(r.get("status"))

        return daft.from_pydict(data)


class SemanticSearch:
    def __init__(self):
        self.embedding_model = settings.openai_embedding_model

    def text_to_embedding(self, query: str) -> list[float]:
        response = client.embeddings.create(model=self.embedding_model, input=query)
        return response.data[0].embedding

    def cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        arr1: NDArray = np.array(vec1)
        arr2: NDArray = np.array(vec2)
        return float(np.dot(arr1, arr2) / (np.linalg.norm(arr1) * np.linalg.norm(arr2)))

    def cosine_similarity_batch(
        self, query_vec: list[float], embeddings: list[list[float]]
    ) -> list[float]:
        query: NDArray = np.array(query_vec)
        emb_matrix: NDArray = np.array(embeddings)
        norms = np.linalg.norm(emb_matrix, axis=1)
        similarities = np.dot(emb_matrix, query) / (norms * np.linalg.norm(query))
        return similarities.tolist()

    def search_by_text(
        self, query: str, images_with_embeddings: list[dict], top_k: int = 10
    ) -> list[dict]:
        query_embedding = self.text_to_embedding(query)

        valid_images = [img for img in images_with_embeddings if img.get("embedding")]
        if not valid_images:
            return []

        embeddings = [img["embedding"] for img in valid_images]
        similarities = self.cosine_similarity_batch(query_embedding, embeddings)

        results = []
        for img, sim in zip(valid_images, similarities):
            results.append({**img, "similarity": sim})

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def search_by_image(
        self, image_path: str, images_with_embeddings: list[dict], top_k: int = 10
    ) -> list[dict]:
        processor = ImageProcessor()
        analysis = processor.analyze_image(image_path)
        query_embedding = processor.generate_embedding(analysis["description"])

        valid_images = [
            img
            for img in images_with_embeddings
            if img.get("embedding") and img.get("image_path") != image_path
        ]
        if not valid_images:
            return []

        embeddings = [img["embedding"] for img in valid_images]
        similarities = self.cosine_similarity_batch(query_embedding, embeddings)

        results = []
        for img, sim in zip(valid_images, similarities):
            results.append({**img, "similarity": sim})

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def create_search_index(self, images_with_embeddings: list[dict]) -> daft.DataFrame:
        data = {
            "id": [],
            "image_path": [],
            "description": [],
            "embedding": [],
        }
        for img in images_with_embeddings:
            if img.get("embedding"):
                data["id"].append(img.get("id"))
                data["image_path"].append(img.get("image_path"))
                data["description"].append(img.get("description"))
                data["embedding"].append(img.get("embedding"))

        return daft.from_pydict(data)
