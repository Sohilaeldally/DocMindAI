CREATE TABLE documents (
    id UUID PRIMARY KEY,

    original_name TEXT NOT NULL,
    stored_name TEXT NOT NULL,

    content_type TEXT NOT NULL,
    file_size BIGINT NOT NULL,

    status TEXT NOT NULL
        CHECK (
            status IN (
                'uploaded',
                'parsing',
                'parsed',
                'chunking',
                'chunked',
                'embedding',
                'completed',
                'failed'
            )
        ),

    error_message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE document_contents (
    document_id UUID PRIMARY KEY
        REFERENCES documents(id)
        ON DELETE CASCADE,

    raw_text TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);