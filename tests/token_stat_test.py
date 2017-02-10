import pytest
from datetime import date
from analyzers.token_stat import AnalyzeToken
import os

pytestmark = pytest.mark.usefixtures("spark")


def test_token_stat(spark):
    path = os.getcwd() + "/tests/fixtures/token_stat"
    start_date = date(2017, 1, 15)
    end_date = date(2017, 1, 16)

    tokenstat = AnalyzeToken(storage_path=path,
                             start_date=start_date,
                             end_date=end_date,
                             spark_context=spark, database=None)

    files = tokenstat.get_files_to_analyze()

    expected_files = [path + '/2017/01/15/token_stat.json.log', path + '/2017/01/16/token_stat.json.log']

    assert len(files) == len(expected_files)
    assert len(set(files) - set(expected_files)) == 0

    results = tokenstat.get_data()
    expected_results = [(u'token:2', date(2017, 1, 15), 1),
                        (u'token:2', date(2017, 1, 16), 1),
                        (u'token:3', date(2017, 1, 15), 6),
                        (u'token:1', date(2017, 1, 15), 2),
                        (u'token:1', date(2017, 1, 16), 2)]
    assert len(results) == len(expected_results)
    assert results == expected_results
