from logging import Logger
from sqlalchemy import text
from src.domain.repositories.demo_repository_interface import DemoRepositoryInterface
from src.infraestructure.database.sqlalchemy import SqlAlchemyDatabase


class DemoRepository(DemoRepositoryInterface):

    database: SqlAlchemyDatabase

    def __init__(self, database: SqlAlchemyDatabase, logger: Logger) -> None:
        super().__init__()
        self.database = database
        self.logger = logger

    async def list_demo(self):
        await self.database.basedb.connect()

        query = text(""" 
            SELECT *
            FROM public.Demo
            WHERE record_status = 'A';
        """)

        response = await self.database.basedb.fetch_all(query)

        await self.database.basedb.disconnect()
        return response

    async def get_demo(self, params):
        await self.database.basedb.connect()

        get_query = text("""
            SELECT *
            FROM public.Demo
            WHERE
                id = :id
                AND record_status = 'A';
        """)

        response = await self.database.basedb.fetch_one(get_query, params)

        await self.database.basedb.disconnect()
        return response

    async def create_demo(self, params):
        await self.database.basedb.connect()

        query = text("""                
            INSERT INTO public.Demo (
                id,
                value,
                record_creation_user
            ) VALUES (
                :id,
                :value,
                :current_user
            );
        """)
        response = await self.database.basedb.execute(query, params)

        await self.database.basedb.disconnect()
        return response

    async def update_demo(self, params):
        await self.database.basedb.connect()

        update_query = text("""
            DO
            $do$
            BEGIN
                SET timezone = 'America/Lima';

                UPDATE public.Demo
                SET
                    value = :value
                    ,record_edit_user = :current_user
                    ,record_edit_date = CURRENT_TIMESTAMP
                WHERE
                    id = :id
                    AND record_status = 'A';
            END
            $do$
        """)
        response = await self.database.basedb.execute(update_query, params)

        await self.database.basedb.disconnect()
        return response

    async def delete_demo(self, params):
        await self.database.basedb.connect()

        delete_query = text("""
            DO
            $do$
            BEGIN
                SET timezone = 'America/Lima';

                UPDATE public.Demo
                SET
                    record_edit_user = :current_user
                    ,record_edit_date = CURRENT_TIMESTAMP
                    ,record_status = 'I'
                WHERE id = :id;
            END
            $do$
        """)
        response = await self.database.basedb.execute(delete_query, params)

        await self.database.basedb.disconnect()
        return response

    async def validate_exist_demo(self, params):
        await self.database.basedb.connect()

        get_query = text("""
            SELECT *
            FROM public.Demo
            WHERE
                id = :id;
        """)

        response = await self.database.basedb.fetch_one(get_query, params)

        await self.database.basedb.disconnect()
        return response
