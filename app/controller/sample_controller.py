from app.model.sample import Sample
from app.model.sample_repository import SampleRepository
from app.view.sample_view import format_sample_table


class SampleController:
    def __init__(self, repository: SampleRepository):
        self._repository = repository

    def register_sample(self, sample: Sample) -> str:
        try:
            self._repository.create(sample)
        except ValueError as e:
            return f"등록 실패: {e}"
        return f"시료 '{sample.name}' 등록 완료."

    def list_samples(self) -> str:
        return format_sample_table(self._repository.find_all())

    def search_samples(self, keyword: str) -> str:
        return format_sample_table(self._repository.search_by_name(keyword))
