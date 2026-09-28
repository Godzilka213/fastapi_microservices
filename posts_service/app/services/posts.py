from app.repositories.posts import PostRepository

from app.repositories.categories import CategoryRepository
from app.schemas.post import Post as PostSchema, PostBase


class PostService:
    def __init__(self, post_repo: PostRepository, category_repo: CategoryRepository):
        self.post_repo = post_repo
        self.category_repo = category_repo

    async def get_all_posts(self, skip: int = 0, limit: int = 100) -> list[PostSchema]:
        db_posts = await self.post_repo.get_all(skip=skip, limit=limit)
        # Преобразуем список SQLAlchemy-моделей в список Pydantic-моделей
        return [PostSchema.model_validate(post) for post in db_posts]

    async def get_post_by_id(self, post_id: int) -> PostSchema | None:
        db_post = await self.post_repo.get_by_id(post_id)
        if db_post is None:
            return None
        return PostSchema.model_validate(db_post)

    # Если например хотим возвращать посты по категории
    async def get_posts_by_category(
        self, category_id: int, skip: int = 0, limit: int = 100
    ) -> list[PostSchema] | None:
        category = await self.category_repo.get_by_id(category_id)
        if category is None:
            return None
        db_posts = await self.post_repo.get_by_category_id(category_id, skip=skip, limit=limit)
        return [PostSchema.model_validate(post) for post in db_posts]

    async def create_post(self, post: PostBase) -> PostSchema | None:
        # Если вернёшь проверку категории - тут можно вернуть None при невалидной category_id
        db_post = await self.post_repo.create(
            title=post.title,
            content=post.content,
            category_id=post.category_id,
        )
        return PostSchema.model_validate(db_post)
