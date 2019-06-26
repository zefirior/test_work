from parse_data.manager import Manager


def test__empty_run():
    m = Manager(5)
    m.run()
    assert not m.alive


def test__some_tasks():
    buffer = []
    num_task = 10
    num_runner = 3

    def task():
        buffer.append(None)

    m = Manager(num_runner, interval=0)
    for _ in range(num_task):
        m.queue.append(task)
    m.run()
    assert not m.alive
    assert len(buffer) == num_task


def test__produce_task():
    buffer = []
    num_task = 10
    num_produce = 3
    num_runner = 3

    def simple_task():
        buffer.append(None)

    def produce_task():
        for _ in range(num_produce):
            m.queue.append(simple_task)

    m = Manager(num_runner, interval=0)
    for _ in range(num_task):
        m.queue.append(produce_task)
    m.run()
    assert not m.alive
    assert len(buffer) == num_task * num_produce
