from datetime import datetime
import pytest


def test_add_and_get(repo, make_test):
    test = make_test()
    new_id = repo.add_test(test)

    saved = repo.get_test(new_id)

    assert saved is not None
    assert saved.id == new_id
    assert saved.examiner == "Dr. Smith"
    assert saved.customer_id == 1
    assert saved.r_rH == 7.80


def test_list_tests_for_customer(repo, make_test):
    t1 = make_test()
    t2 = make_test(exam_date=datetime(2025, 5, 1))

    repo.add_test(t1)
    repo.add_test(t2)

    items = repo.list_tests_for_customer(1)

    assert len(items) == 2
    assert items[0].exam_date == t2.exam_date.isoformat()
    assert items[1].exam_date == t1.exam_date.isoformat()


def test_list_tests_for_customer_validation(repo):
    with pytest.raises(ValueError):
        repo.list_tests_for_customer(None)

    with pytest.raises(TypeError):
        repo.list_tests_for_customer("x")

    with pytest.raises(ValueError):
        repo.list_tests_for_customer(0)

    with pytest.raises(ValueError):
        repo.list_tests_for_customer(-10)


def test_update(repo, make_test):
    test = make_test()
    test_id = repo.add_test(test)

    saved = repo.get_test(test_id)
    saved.examiner = "Updated Doctor"

    ok = repo.update_test(saved)
    assert ok is True

    updated = repo.get_test(test_id)
    assert updated.examiner == "Updated Doctor"


def test_update_missing_id(repo, make_test):
    test = make_test()
    test.id = None

    with pytest.raises(ValueError):
        repo.update_test(test)


def test_delete(repo, make_test):
    test_id = repo.add_test(make_test())
    deleted = repo.delete_test(test_id)

    assert deleted is True
    assert repo.get_test(test_id) is None


def test_delete_nonexistent(repo):
    deleted = repo.delete_test(9999)
    assert deleted is False
