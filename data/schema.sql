-- src_run_id is the eight digit identifier used by speedrun.com
-- elapsed_time is formatted as "mm:ss.ttt" as normal, the other timing information is at it sounds
CREATE TABLE run(
    id                          INTEGER PRIMARY KEY,
    src_run_id                  TEXT UNIQUE NOT NULL,
    runner_alias                TEXT NOT NULL,
    elapsed_time                TEXT NOT NULL,
    platform_fps                FLOAT NOT NULL,
    elapsed_frames              INTEGER
);

-- The splits on a per level basis, as frame counts, and using my convention for splitting location (which can be different than runners normally use).
-- split_0 is the frame the 400 appears, split_8_4 is the frame the axe is touched.
CREATE TABLE splits(
    id                          INTEGER PRIMARY KEY,
    run_id                      INTEGER REFERENCES run(id) ON DELETE CASCADE NOT NULL,
    split_0                     INTEGER,
    split_1_1                   INTEGER,
    split_1_2                   INTEGER,
    split_4_1                   INTEGER,
    split_4_2                   INTEGER,
    split_8_1                   INTEGER,
    split_8_2                   INTEGER,
    split_8_3                   INTEGER,
    split_8_4                   INTEGER
);

-- Inputs are recreated for the normal smb rom (even if runner played on combo cart), each byte is one frame of input.
-- input bits are: RLDUTSBA (where T is start, S is select).
-- These inputs are not necessarily accurate to what the runner pressed, but at least mostly accurate to the outcome seen on video.
CREATE TABLE tas_recreation(
    id                          INTEGER PRIMARY KEY,
    run_id                      INTEGER REFERENCES run(id) ON DELETE CASCADE NOT NULL,
    recreator_alias             TEXT NOT NULL,
    inputs                      BLOB
);

-- 0x20 in size, each frame references a frame_palette
CREATE TABLE frame_palette(
    id                          INTEGER PRIMARY KEY,
    palette                     BLOB
);

CREATE TABLE tas_frame(
    id                          INTEGER PRIMARY KEY,
    run_id                      INTEGER REFERENCES run(id) ON DELETE CASCADE NOT NULL,
    frame_palette_id            INTEGER REFERENCES frame_palette(id) ON DELETE CASCADE NOT NULL,
    tas_frame_index             INTEGER,
    frame_from_four_hundred     INTEGER,
    world                       INTEGER,
    level                       INTEGER,
    area_pointer                INTEGER,
    area_pointer_x              INTEGER
);

CREATE TABLE oam(
    id                          INTEGER PRIMARY KEY,
    tas_frame_id                INTEGER REFERENCES tas_frame(id) ON DELETE CASCADE NOT NULL,
    y                           INTEGER,
    tile_index                  INTEGER,
    attributes                  INTEGER,
    x                           INTEGER,
    is_mario                    INTEGER GENERATED ALWAYS AS 
        ((tile_index >= 0x00 AND tile_index <= 0x4f) OR 
         (tile_index >= 0x58 AND tile_index <= 0x5a) OR 
         (tile_index >= 0x5c AND tile_index <= 0x5f) OR 
         (tile_index >= 0x90 AND tile_index <= 0x93) OR 
         (tile_index == 0x9e) OR (tile_index == 0x9f)) VIRTUAL
);

CREATE TABLE ntdiff(
    id                          INTEGER PRIMARY KEY,
    tas_frame_id                INTEGER REFERENCES tas_frame(id) ON DELETE CASCADE NOT NULL,
    ntpage                      INTEGER,
    offset                      INTEGER,
    value                       INTEGER
);

CREATE TABLE frame_info(
    id                          INTEGER PRIMARY KEY,
    frame_from_four_hundred     INTEGER,
    world                       INTEGER,
    level                       INTEGER,
    area_pointer                INTEGER,
    area_pointer_x              INTEGER,
    frame_palette_id            INTEGER REFERENCES frame_palette(id) ON DELETE CASCADE NOT NULL,
    minimap_left                INTEGER
);

CREATE INDEX tas_frame_run_id_idx ON tas_frame (run_id);
CREATE INDEX tas_frame_frame_from_four_hundred_idx ON tas_frame (frame_from_four_hundred);
CREATE INDEX oam_tas_frame_id_idx ON oam (tas_frame_id);
CREATE INDEX splits_run_id ON splits (run_id);
CREATE INDEX tas_frame_area_pointer_ids ON tas_frame (area_pointer);
CREATE INDEX ntdiff_tas_frame_id_idx on ntdiff (tas_frame_id);

