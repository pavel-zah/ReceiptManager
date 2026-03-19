CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    user_public_name VARCHAR(255) NULL,
    registered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE receipts (
    id SERIAL PRIMARY KEY,
    paid_at TIMESTAMP NOT NULL,
    tip DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    service DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    place_name VARCHAR(255) NULL
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    public_key VARCHAR(6) UNIQUE NOT NULL,
    creator_id INTEGER NOT NULL,
    receipt_id INTEGER NULL, -- Nullable, так как в Python "str | None"
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_rooms_creator
        FOREIGN KEY (creator_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_rooms_receipt
        FOREIGN KEY (receipt_id)
        REFERENCES receipts(id)
        ON DELETE SET NULL -- Если чек удален, комната остается, но поле очищается
        ON UPDATE CASCADE
);

CREATE TABLE room_participants (
    room_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (room_id, user_id), -- Уникальная пара

    CONSTRAINT fk_participant_room
        FOREIGN KEY (room_id)
        REFERENCES rooms(id)
        ON DELETE CASCADE -- Если комнату удаляют, список участников чистится
        ON UPDATE CASCADE,

    CONSTRAINT fk_participant_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE receipt_items (
    id SERIAL PRIMARY KEY,
    receipt_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity DECIMAL(10, 3) NOT NULL DEFAULT 1.000, -- 3 знака, если вдруг вес (кг)

    CONSTRAINT fk_items_receipt
        FOREIGN KEY (receipt_id)
        REFERENCES receipts(id)
        ON DELETE CASCADE -- Удаляем чек -> удаляются позиции
        ON UPDATE CASCADE
);

CREATE TABLE item_assignments (
    item_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,

    PRIMARY KEY (item_id, user_id),

    CONSTRAINT fk_assignment_item
        FOREIGN KEY (item_id)
        REFERENCES receipt_items(id)
        ON DELETE CASCADE -- Если позиция удалена, назначение пропадает
        ON UPDATE CASCADE,

    CONSTRAINT fk_assignment_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE -- Если юзер удален, он убирается из позиций
        ON UPDATE CASCADE
);