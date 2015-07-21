drop table if exists games;
create table games (
    game_id text primary key,
    board_state blob not null
);
