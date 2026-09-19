from app.core.repository import BaseRepository
from app.modules.user.models import User


class UserRepository(BaseRepository[User]):
    model = User
    default_order_by = (User.created_at,)

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_by(email=email)
