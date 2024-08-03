from dungeon2 import load_map, find_start, get_grid_size, is_inside_grid, look_around

TEST_MAP_1 = """--S--
--*--
--**F"""

TEST_MAP_2 = """FS"""

TEST_MAP_3 = """*****
*---*
*-S-*
*---*
****F"""

TEST_MAP_4 = """*****
*---*
**S**
*---*
****F"""


def create_map_file(tmp_path, map_contents=TEST_MAP_1):
    map_file = tmp_path / "map.txt"
    map_file.write_text(map_contents)
    return map_file


def test_load_map_1(tmp_path):
    # TEST_MAP_1
    map_file = create_map_file(tmp_path, TEST_MAP_1)
    grid = load_map(map_file)
    assert len(grid) == 3
    assert len(grid[0]) == 5
    assert grid[0] == ['-', '-', 'S', '-', '-']
    assert grid[1] == ['-', '-', '*', '-', '-']
    assert grid[2] == ['-', '-', '*', '*', 'F']


def test_load_map_2(tmp_path):
    # TEST_MAP_2
    map_file = create_map_file(tmp_path, TEST_MAP_2)
    grid = load_map(map_file)
    assert len(grid) == 1
    assert len(grid[0]) == 2
    assert grid[0] == ['F', 'S']


def test_load_map_3(tmp_path):
    # TEST_MAP_3
    map_file = create_map_file(tmp_path, TEST_MAP_3)
    grid = load_map(map_file)
    assert len(grid) == 5
    assert len(grid[0]) == 5
    assert grid[0] == ['*', '*', '*', '*', '*']
    assert grid[1] == ['*', '-', '-', '-', '*']
    assert grid[2] == ['*', '-', 'S', '-', '*']
    assert grid[3] == ['*', '-', '-', '-', '*']
    assert grid[4] == ['*', '*', '*', '*', 'F']


def test_load_map_4(tmp_path):
    # TEST_MAP_4
    map_file = create_map_file(tmp_path, TEST_MAP_4)
    grid = load_map(map_file)
    assert len(grid) == 5
    assert len(grid[0]) == 5
    assert grid[0] == ['*', '*', '*', '*', '*']
    assert grid[1] == ['*', '-', '-', '-', '*']
    assert grid[2] == ['*', '*', 'S', '*', '*']
    assert grid[3] == ['*', '-', '-', '-', '*']
    assert grid[4] == ['*', '*', '*', '*', 'F']


def test_find_start_1(tmp_path):
    # TEST_MAP_1
    map_file = create_map_file(tmp_path, TEST_MAP_1)
    grid = load_map(map_file)
    position = find_start(grid)
    assert position[0] == 0
    assert position[1] == 2


def test_find_start_2(tmp_path):
    # TEST_MAP_2
    map_file = create_map_file(tmp_path, TEST_MAP_2)
    grid = load_map(map_file)
    position = find_start(grid)
    assert position[0] == 0
    assert position[1] == 1


def test_find_start_3(tmp_path):
    # TEST_MAP_3
    map_file = create_map_file(tmp_path, TEST_MAP_3)
    grid = load_map(map_file)
    position = find_start(grid)
    assert position[0] == 2
    assert position[1] == 2


def test_find_start_4(tmp_path):
    # TEST_MAP_4
    map_file = create_map_file(tmp_path, TEST_MAP_4)
    grid = load_map(map_file)
    position = find_start(grid)
    assert position[0] == 2
    assert position[1] == 2


def test_look_around_1(tmp_path):
    # TEST_MAP_1
    map_file = create_map_file(tmp_path, TEST_MAP_1)
    grid = load_map(map_file)
    position = find_start(grid)
    directions = look_around(grid, position)
    assert directions == ['south']


def test_look_around_2(tmp_path):
    # TEST_MAP_2
    map_file = create_map_file(tmp_path, TEST_MAP_2)
    grid = load_map(map_file)
    position = find_start(grid)
    directions = look_around(grid, position)
    assert directions == ['west']


def test_look_around_3(tmp_path):
    # TEST_MAP_3
    map_file = create_map_file(tmp_path, TEST_MAP_3)
    grid = load_map(map_file)
    position = find_start(grid)
    directions = look_around(grid, position)
    assert directions == []


def test_look_around_4(tmp_path):
    # TEST_MAP_4
    map_file = create_map_file(tmp_path, TEST_MAP_4)
    grid = load_map(map_file)
    position = find_start(grid)
    directions = look_around(grid, position)
    assert set(directions) == set(['west', 'east'])


def test_get_grid_size_1(tmp_path):
    # TEST_MAP_1
    map_file = create_map_file(tmp_path, TEST_MAP_1)
    grid = load_map(map_file)
    size = get_grid_size(grid)
    assert size == [3, 5]


def test_get_grid_size_2(tmp_path):
    # TEST_MAP_2
    map_file = create_map_file(tmp_path, TEST_MAP_2)
    grid = load_map(map_file)
    size = get_grid_size(grid)
    assert size == [1, 2]


def test_get_grid_size_3(tmp_path):
    # TEST_MAP_3
    map_file = create_map_file(tmp_path, TEST_MAP_3)
    grid = load_map(map_file)
    size = get_grid_size(grid)
    assert size == [5, 5]


def test_get_grid_size_4(tmp_path):
    # TEST_MAP_4
    map_file = create_map_file(tmp_path, TEST_MAP_4)
    grid = load_map(map_file)
    size = get_grid_size(grid)
    assert size == [5, 5]


def test_is_inside_grid_1_inside(tmp_path):
    # TEST_MAP_1
    map_file = create_map_file(tmp_path, TEST_MAP_1)
    grid = load_map(map_file)
    position = [1, 1]
    assert is_inside_grid(grid, position) is True


def test_is_inside_grid_1_outside(tmp_path):
    # TEST_MAP_1
    map_file = create_map_file(tmp_path, TEST_MAP_1)
    grid = load_map(map_file)
    position = [4, 4]
    assert is_inside_grid(grid, position) is False
