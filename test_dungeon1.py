from dungeon1 import load_map, find_start

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
