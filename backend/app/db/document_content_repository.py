from uuid import UUID
from app.db.database import pool
from app.models.document_content import DocumentContent


def insert_document_content(document_id: UUID, raw_text: str) -> DocumentContent:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO document_contents (document_id, raw_text)
                VALUES (%s, %s)
                RETURNING document_id, raw_text, created_at, updated_at
                """,
                (document_id, raw_text),
            )
            row = cursor.fetchone()

    return DocumentContent(
        document_id=row[0],
        raw_text=row[1],
        created_at=row[2],
        updated_at=row[3],
    )


def get_document_content(document_id: UUID) -> DocumentContent | None:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT document_id, raw_text, created_at, updated_at
                FROM document_contents
                WHERE document_id = %s
                """,
                (document_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return DocumentContent(
                document_id=row[0],
                raw_text=row[1],
                created_at=row[2],
                updated_at=row[3],
            )