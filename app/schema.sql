drop table if exists games;
create table games (
    game_id text primary key,
    current_player text not null,
    red_pieces integer not null,
    blue_pieces integer not null,
    board_state blob not null
);